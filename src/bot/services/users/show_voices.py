from urllib.parse import quote

from sqlalchemy.sql.functions import count
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from bot.utils.constants import MAX_PAGES, MAX_VOICES
from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.inline_keyboard import build_page_buttons
from bot.utils.text import cdp, ct, mt
from models import user_model, user_voice_model, voice_model
from settings import database, settings


@check_user
@delete_previous_messages
async def show_my_voices(
    update: Update, context: CallbackContext, callback_data: str | None = None
) -> None:
    current_page = 1

    if update.callback_query:
        callback_data = callback_data or update.callback_query.data
        if callback_data.startswith(cdp.show_my_voices):
            current_page = int(callback_data.replace(f"{cdp.show_my_voices}_", ""))
        elif callback_data.startswith(cdp.delete_voice):
            current_page = int(callback_data.split("_")[1])

    user_uuid_subq = (
        user_model.select()
        .with_only_columns(user_model.c.uuid)
        .where(user_model.c.telegram_id == update.effective_user.id)
        .scalar_subquery()
    )
    count_voices = await database.fetch_one(
        voice_model.select()
        .select_from(voice_model)
        .with_only_columns(count().label("count"))
        .join(user_voice_model, voice_model.c.uuid == user_voice_model.c.voice_uuid, isouter=True)
        .where(user_voice_model.c.user_uuid == user_uuid_subq)
    )
    count_voices = count_voices["count"]

    voices_query = (
        voice_model.select()
        .with_only_columns(
            voice_model.c.uuid, voice_model.c.path, voice_model.c.title, voice_model.c.performer
        )
        .join(user_voice_model, voice_model.c.uuid == user_voice_model.c.voice_uuid, isouter=True)
        .where(user_voice_model.c.user_uuid == user_uuid_subq)
        .order_by(voice_model.c.created_at)
        .offset((MAX_PAGES * current_page) - MAX_PAGES)
        .limit(MAX_VOICES)
    )

    page_buttons = build_page_buttons(
        prefix=cdp.show_my_voices,
        current_page=current_page,
        count_voices=count_voices,
    )

    if voices := await database.fetch_all(voices_query):
        voices_message_id, delete_voices_buttons = [], []
        for index, voice in enumerate(voices, start=1):
            delete_voices_buttons.append(
                InlineKeyboardButton(
                    ct.delete_voice_button,
                    callback_data=f"{cdp.delete_voice}{current_page}_{voice['uuid']}",
                )
            )
            if index == len(voices):
                reply_markup = InlineKeyboardMarkup(
                    [
                        page_buttons,
                        delete_voices_buttons,
                        [InlineKeyboardButton(ct.menu, callback_data=cdp.show_categories)],
                    ],
                )
            else:
                reply_markup = None

            if update.message:
                res = await update.message.reply_voice(
                    f"{settings.voice_url_path}/{quote(voice['path'])}",
                    reply_markup=reply_markup,
                    quote=False,
                )
            else:
                res = await update.callback_query.message.reply_voice(
                    f"{settings.voice_url_path}/{quote(voice['path'])}",
                    reply_markup=reply_markup,
                    quote=False,
                )
            voices_message_id.append(res.message_id)

        context.user_data["voices_message_id"] = voices_message_id
    else:
        if update.message:
            await update.message.reply_text(mt.my_voices_not_found)
        else:
            if current_page > 1:
                callback_data = f"{cdp.show_my_voices}_{current_page - 1}"
                await show_my_voices(update=update, context=context, callback_data=callback_data)
            else:
                await update.callback_query.message.reply_text(mt.my_voices_not_found)


__all__ = ["show_my_voices"]
