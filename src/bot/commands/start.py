from loguru import logger
from sqlalchemy.exc import IntegrityError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.utils import check_user, mt
from bot.utils.decorators import delete_previous_messages
from models import category_model, invite_link_model, user_invite_link_model, user_model
from settings import database


@check_user
@delete_previous_messages
def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(row["title"], callback_data=row["slug"].value)]
            for row in database.execute(category_model.select())
        ]
    )
    _start_answer(update=update, text=mt.select_category, reply_markup=reply_markup)


def _start_answer(update: Update, text: str, reply_markup=None) -> None:
    if update.message:
        update.message.reply_text(text, reply_markup=reply_markup)
        if len(update.message.text) > 6:
            invite_link_title = update.message.text.replace("/start ", "")
            user_uuid_subq = (
                user_model.select()
                .with_only_columns(user_model.c.uuid)
                .where(user_model.c.telegram_id == update.effective_user.id)
                .scalar_subquery()
            )
            invite_link_uuid_subq = (
                invite_link_model.select()
                .with_only_columns(invite_link_model.c.uuid)
                .where(invite_link_model.c.title == invite_link_title)
                .scalar_subquery()
            )
            try:
                database.execute(
                    user_invite_link_model.insert().values(
                        user_uuid=user_uuid_subq, invite_link_uuid=invite_link_uuid_subq
                    )
                )
            except IntegrityError:
                pass
    else:
        update.callback_query.message.reply_text(text, reply_markup=reply_markup)


__all__ = ["start"]
