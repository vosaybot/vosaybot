from urllib.parse import quote

from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.functions import count
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils.constants import MAX_PAGES, MAX_VOICES
from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.inline_keyboard import build_page_buttons
from bot.utils.text import cdp, ct, mt
from models import user_model, user_voice_model, voice_model
from settings import database, settings


@check_user
@delete_previous_messages
async def show_popular(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_page = 1
    if update.callback_query:
        current_page = int(update.callback_query.data.replace(f"{cdp.show_popular}_", ""))

    user_uuid_subq = (
        user_model.select()
        .with_only_columns(user_model.c.uuid)
        .where(user_model.c.telegram_id == update.effective_user.id)
        .scalar_subquery()
    )
    popular_voices_subq = (
        user_voice_model.select()
        .select_from(user_voice_model)
        .with_only_columns(count(user_voice_model.c.voice_uuid), user_voice_model.c.voice_uuid)
        .group_by(user_voice_model.c.voice_uuid)
    )

    voices_query = (
        popular_voices_subq.select()
        .select_from(popular_voices_subq)
        .with_only_columns(
            popular_voices_subq.c.count,
            popular_voices_subq.c.voice_uuid,
            voice_model.c.path,
            user_voice_model.c.user_uuid,
        )
        .join(voice_model, popular_voices_subq.c.voice_uuid == voice_model.c.uuid)
        .join(
            user_voice_model,
            and_(
                popular_voices_subq.c.voice_uuid == user_voice_model.c.voice_uuid,
                user_voice_model.c.user_uuid == user_uuid_subq,
            ),
            isouter=True,
        )
        .order_by(popular_voices_subq.c.count.desc())
    )

    count_voices = await database.fetch_one(
        voices_query.select().select_from(voices_query).with_only_columns(count().label("count"))
    )
    count_voices = count_voices["count"]

    voices_query = voices_query.offset((MAX_PAGES * current_page) - MAX_PAGES).limit(MAX_VOICES)

    page_buttons = build_page_buttons(
        prefix=cdp.show_popular,
        current_page=current_page,
        count_voices=count_voices,
    )

    if voices := await database.fetch_all(voices_query):
        voices_message_id, voice_buttons = [], []
        for index, voice in enumerate(voices, start=1):
            if voice[user_voice_model.c.user_uuid]:
                voice_button = InlineKeyboardButton(
                    text=ct.delete_voice_button,
                    callback_data=f"{cdp.delete_voice}{voice['voice_uuid']}",
                )
            else:
                voice_button = InlineKeyboardButton(
                    text=ct.save_voice_button,
                    callback_data=f"{cdp.save_voice}{voice['voice_uuid']}",
                )

            voice_buttons.append(voice_button)

            if index == len(voices):
                reply_markup = InlineKeyboardMarkup(
                    [
                        page_buttons,
                        voice_buttons,
                        [
                            InlineKeyboardButton(ct.menu, callback_data=cdp.show_categories),
                        ],
                    ]
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
            await update.message.reply_text(mt.popular_not_found)


__all__ = ["show_popular"]
