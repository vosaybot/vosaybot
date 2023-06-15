from loguru import logger
from sqlalchemy.exc import IntegrityError
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.users.show_voices import show_my_voices
from bot.utils import check_user, update_voice_inline_button
from models import user_model, user_voice_model
from settings import database


@check_user
async def delete_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query.data.startswith("d_m"):
        voice_uuid = update.callback_query.data[5:]
        await _delete_voice(update=update, context=context, voice_uuid=voice_uuid)
        await show_my_voices(update=update, context=context)
    else:
        voice_uuid = update.callback_query.data[2:]
        await _delete_voice(update=update, context=context, voice_uuid=voice_uuid)
        reply_markup = update.callback_query.message.reply_markup
        update_voice_inline_button(
            reply_markup=reply_markup, data=update.callback_query.data, voice_uuid=voice_uuid
        )
        await update.callback_query.message.edit_reply_markup(reply_markup=reply_markup)


async def _delete_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE, voice_uuid: str
) -> None:
    user_uuid_subq = (
        user_model.select()
        .with_only_columns(user_model.c.uuid)
        .where(user_model.c.telegram_id == update.effective_user.id)
        .scalar_subquery()
    )
    try:
        await database.execute(
            user_voice_model.delete().where(
                user_voice_model.c.user_uuid == user_uuid_subq,
                user_voice_model.c.voice_uuid == voice_uuid,
            )
        )
    except IntegrityError as err:
        logger.error(err)
