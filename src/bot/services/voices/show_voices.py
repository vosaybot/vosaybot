from urllib.parse import quote

from loguru import logger
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils import (
    MAX_PAGES,
    MAX_VOICES,
    build_page_buttons,
    check_user,
    ct,
    delete_previous_messages,
    mt,
    update_voice_inline_button
)
from models import (
    available_categories,
    category_model,
    subcategory_model,
    user_model,
    user_voice_model,
    voice_model
)
from settings import database, settings


@check_user
async def show_voices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    callback_data = update.callback_query.data

    if not callback_data or callback_data.endswith("*"):
        return

    if callback_data in [c.value for c in available_categories]:
        await _show_subcategories(update=update, context=context, data=callback_data)
        return

    if callback_data.startswith("s_"):
        await _save_voice(update=update, context=context, data=callback_data)
        return

    await _show_voices(update=update, context=context, data=callback_data)


@delete_previous_messages
async def _show_subcategories(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
) -> None:
    subcategories = (
        voice_model.select()
        .distinct()
        .select_from(voice_model)
        .with_only_columns(subcategory_model.c.title, subcategory_model.c.slug)
        .where(category_model.c.slug == data)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
    )

    keyboard = [
        [InlineKeyboardButton(row.title, callback_data=f"{data}_{row['slug']}_1")]
        for row in await database.fetch_all(subcategories)
    ]
    keyboard.append([InlineKeyboardButton(ct.back, callback_data="show_menu")])

    res = await update.callback_query.message.reply_text(
        text=mt.select_category if len(keyboard) > 1 else mt.voices_not_found,
        reply_markup=InlineKeyboardMarkup(keyboard),
        quote=False,
    )

    context.user_data["voices_message_id"] = [res.message_id]


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
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
        .where(category_model.c.slug == category, subcategory_model.c.slug == subcategory)
    )
    count_voices = count_voices["count"]

    voices_query = (
        voice_model.select()
        .with_only_columns(voice_model.c.uuid, voice_model.c.path, user_voice_subq.c.uuid)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
        .join(user_voice_subq, voice_model.c.uuid == user_voice_subq.c.voice_uuid, full=True)
        .where(category_model.c.slug == category, subcategory_model.c.slug == subcategory)
        .offset((MAX_PAGES * current_page) - MAX_PAGES)
        .limit(MAX_VOICES)
    )

    page_buttons = build_page_buttons(
        current_page=current_page,
        count_voices=count_voices,
        category=category,
        subcategory=subcategory,
    )

    if voices := await database.fetch_all(voices_query):
        voices_message_id, voice_buttons = [], []
        for index, voice in enumerate(voices, start=1):
            if voice[user_voice_subq.c.uuid]:
                voice_button = InlineKeyboardButton(
                    ct.delete_voice_button, callback_data=f"d_{voice['uuid']}"
                )

            else:
                voice_button = InlineKeyboardButton(
                    ct.save_voice_button, callback_data=f"s_{voice['uuid']}"
                )

            voice_buttons.append(voice_button)

            if index == len(voices):
                reply_markup = InlineKeyboardMarkup(
                    [
                        page_buttons,
                        voice_buttons,
                        [
                            InlineKeyboardButton(ct.menu, callback_data="show_menu"),
                            InlineKeyboardButton(ct.back, callback_data=category),
                        ],
                    ]
                )
            else:
                reply_markup = None

            res = await update.callback_query.message.reply_voice(
                f"{settings.voice_url}/{settings.telegram_token}/assets/{quote(voice['path'])}",
                reply_markup=reply_markup,
                quote=False,
            )

            voices_message_id.append(res.message_id)

        context.user_data["voices_message_id"] = voices_message_id


async def _save_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    voice_uuid = data.replace("s_", "")

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

    reply_markup = update.callback_query.message.reply_markup
    update_voice_inline_button(
        reply_markup=reply_markup, data=data, voice_uuid=voice_uuid, is_delete_button=True
    )
    await update.callback_query.message.edit_reply_markup(reply_markup=reply_markup)


__all__ = ["show_voices"]
