from loguru import logger
from telegram import Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext

from bot.utils.text import message_text
from models import user_model
from settings import database


def check_user(f):
    def wrapper(update: Update, *args: object) -> None:
        try:
            if update.effective_user.is_bot:
                logger.warning(
                    "Attempt to login from bot with id: {} and name: {}".format(
                        args[0].effective_user.bot.id, args[0].effective_user.bot.name
                    )
                )
                update.message.reply_text(message_text.bots_are_not_allowed)
                return
            elif not database.execute(
                (user_model.select().where(user_model.c.telegram_id == update.effective_user.id))
            ).first():
                database.execute(user_model.insert().values(telegram_id=update.effective_user.id))

            f(update, *args)

        except Unauthorized as err:
            logger.error("Error: {}\nUser: {}".format(err, args[0].effective_user.id))

    return wrapper


def delete_previous_messages(f):
    def wrapper(update: Update, context: CallbackContext, *args: object, **kwargs) -> None:
        try:
            for voices_message_id in context.user_data.get("voices_message_id", []):
                try:
                    context.bot.delete_message(
                        chat_id=update.effective_chat.id, message_id=voices_message_id
                    )
                except BadRequest:
                    pass
            context.user_data["voices_message_id"] = []
            f(update, context, *args, **kwargs)

        except Unauthorized as err:
            logger.error("Error: {}\nUser: {}".format(err, args[0].effective_user.id))

    return wrapper


__all__ = ["check_user", "delete_previous_messages"]
