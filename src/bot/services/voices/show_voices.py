from urllib.parse import quote

from sqlalchemy.sql.functions import count
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils.constants import MAX_PAGES, MAX_VOICES
from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.inline_keyboard import build_page_buttons
from bot.utils.text import cdp, ct
from models import user_model, user_voice_model, voice_model
from settings import database, settings


@check_user
async def show_voices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.callback_query.data

    if not data or "*" in data:
        return

    data = data.replace(cdp.show_voice, "")
    await _show_voices(update=update, context=context, data=data)


@delete_previous_messages
async def _show_voices(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    category, subcategory, page = data.split("_")
    current_page = int(page)

    user_uuid_subq = (
        user_model.select()
        .with_only_columns(user_model.c.uuid)
        .where(user_model.c.telegram_id == update.effective_user.id)
        .scalar_subquery()
    )
    user_voice_subq = (
        user_voice_model.select().where(user_voice_model.c.user_uuid == user_uuid_subq).subquery()
    )

    count_voices = await database.fetch_one(
        voice_model.select()
        .select_from(voice_model)
        .with_only_columns(count().label("count"))
        .where(voice_model.c.category == category, voice_model.c.subcategory == subcategory)
    )
    count_voices = count_voices["count"]

    voices_query = (
        voice_model.select()
        .with_only_columns(voice_model.c.uuid, voice_model.c.path, user_voice_subq.c.uuid)
        .join(user_voice_subq, voice_model.c.uuid == user_voice_subq.c.voice_uuid, full=True)
        .where(voice_model.c.category == category, voice_model.c.subcategory == subcategory)
        .offset((MAX_PAGES * current_page) - MAX_PAGES)
        .limit(MAX_VOICES)
    )

    page_buttons = build_page_buttons(
        prefix=f"{cdp.show_voice}{category}_{subcategory}",
        current_page=current_page,
        count_voices=count_voices,
    )

    if voices := await database.fetch_all(voices_query):
        voices_message_id, voice_buttons = [], []
        for index, voice in enumerate(voices, start=1):
            if voice[user_voice_subq.c.uuid]:
                voice_button = InlineKeyboardButton(
                    text=ct.delete_voice_button, callback_data=f"{cdp.delete_voice}{voice['uuid']}"
                )
            else:
                voice_button = InlineKeyboardButton(
                    text=ct.save_voice_button, callback_data=f"{cdp.save_voice}{voice['uuid']}"
                )

            voice_buttons.append(voice_button)

            if index == len(voices):
                reply_markup = InlineKeyboardMarkup(
                    [
                        page_buttons,
                        voice_buttons,
                        [
                            InlineKeyboardButton(ct.menu, callback_data=cdp.show_categories),
                            InlineKeyboardButton(
                                ct.back, callback_data=f"{cdp.show_subcategory}{category}"
                            ),
                        ],
                    ]
                )
            else:
                reply_markup = None

            res = await update.callback_query.message.reply_voice(
                f"{settings.voice_url_path}/{quote(voice['path'])}",
                reply_markup=reply_markup,
                quote=False,
            )

            voices_message_id.append(res.message_id)

        context.user_data["voices_message_id"] = voices_message_id


__all__ = ["show_voices"]
