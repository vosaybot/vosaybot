from loguru import logger
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.inline_keyboard import update_voice_inline_button
from bot.utils.text import cdp
from models import user_model, user_voice_model
from settings import database


async def save_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.callback_query.data
    voice_uuid = data.replace(cdp.save_voice, "")

    user_uuid_subq = (
        user_model.select()
        .with_only_columns(user_model.c.uuid)
        .where(user_model.c.telegram_id == update.effective_user.id)
        .scalar_subquery()
    )

    try:
        await database.execute(
            insert(user_voice_model).values(user_uuid=user_uuid_subq, voice_uuid=voice_uuid)
        )
    except IntegrityError as err:
        logger.error(err)

    reply_markup = update_voice_inline_button(
        reply_markup=update.callback_query.message.reply_markup,
        data=data,
        voice_uuid=voice_uuid,
        is_delete_button=True,
    )
    await update.callback_query.message.edit_reply_markup(reply_markup=reply_markup)


__all__ = ["save_voice"]
