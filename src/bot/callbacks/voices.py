import math
from urllib.parse import quote

from sqlalchemy import bindparam, func, insert, select
from sqlalchemy.exc import IntegrityError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from bot.utils import check_user, ct, delete_previous_messages, mt
from models import (
    available_categories,
    category_model,
    subcategory_model,
    user_model,
    user_voice_model,
    voice_model
)
from settings import database, settings

MAX_PAGES, MAX_VOICES = 5, 5


@check_user
def show_voices(update: Update, context: CallbackContext) -> None:
    callback_data = update.callback_query.data

    if callback_data.endswith("*"):
        return

    if callback_data in [c.value for c in available_categories]:
        _show_categories(update=update, context=context, data=callback_data)
        return

    if callback_data.startswith("s_"):
        _save_voice(update=update, context=context, data=callback_data)
        return

    _show_voices(update=update, context=context, data=callback_data)


@delete_previous_messages
def _show_categories(update: Update, context: CallbackContext, data: str) -> None:
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
        [InlineKeyboardButton(row["title"], callback_data=f"{data}_{row['slug']}_1")]
        for row in database.execute(subcategories)
    ]
    keyboard.append([InlineKeyboardButton(ct.back, callback_data="show_menu")])

    if update.callback_query.message.text:
        res = update.callback_query.message.edit_text(
            mt.select_category if len(keyboard) > 1 else mt.voices_not_found,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        res = update.callback_query.message.reply_text(
            mt.select_category if len(keyboard) > 1 else mt.voices_not_found,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    context.user_data["voices_message_id"] = [res.message_id]


@delete_previous_messages
def _show_voices(update: Update, context: CallbackContext, data: str) -> None:
    category, subcategory, page = data.split("_")
    current_page = int(page)

    count_voices = database.execute(
        select(func.count("*"))
        .select_from(voice_model)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
        .where(category_model.c.slug == category)
        .where(subcategory_model.c.slug == subcategory)
    ).scalar()

    voices_query = (
        voice_model.select()
        .with_only_columns(voice_model.c.uuid, voice_model.c.path)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
        .where(category_model.c.slug == category, subcategory_model.c.slug == subcategory)
        .offset((MAX_PAGES * current_page) - MAX_PAGES)
        .limit(MAX_VOICES)
    )

    pages_buttons = _get_pages_buttons(
        current_page=current_page,
        count_voices=count_voices,
        category=category,
        subcategory=subcategory,
    )

    if voices := database.execute(voices_query):
        voices_message_id, save_voices_buttons = [], []
        for index, voice in enumerate(voices, start=1):
            save_voices_buttons.append(
                InlineKeyboardButton("💾", callback_data=f"s_{voice['uuid']}")
            )
            reply_markup = (
                InlineKeyboardMarkup(
                    [
                        pages_buttons,
                        save_voices_buttons,
                        [
                            InlineKeyboardButton(ct.menu, callback_data="show_menu"),
                            InlineKeyboardButton(ct.back, callback_data=category),
                        ],
                    ]
                )
                if index == voices.rowcount
                else None
            )

            res = update.callback_query.message.reply_voice(
                f"{settings.voice_url}/{settings.telegram_token}/assets/{quote(voice['path'])}",
                reply_markup=reply_markup,
            )

            voices_message_id.append(res.message_id)

        context.user_data["voices_message_id"] = voices_message_id


def _save_voice(update: Update, context: CallbackContext, data: str) -> None:
    user_telegram_id, voice_uuid = update.effective_user.id, data.replace("s_", "")

    voice_query = (
        voice_model.select()
        .where(voice_model.c.uuid == voice_uuid)
        .with_only_columns(voice_model.c.performer, voice_model.c.title)
    )
    user_uuid_subq = (
        select(user_model.c.uuid)
        .where(user_model.c.telegram_id == bindparam("user_telegram_id"))
        .scalar_subquery()
    )

    voice = "-".join(database.execute(voice_query).fetchone())
    try:
        database.execute(
            insert(user_voice_model).values(user_uuid=user_uuid_subq),
            [
                {"user_telegram_id": user_telegram_id, "voice_uuid": voice_uuid},
            ],
        )
        update.callback_query.message.reply_text(mt.voice_saved.format(voice))
    except IntegrityError:
        update.callback_query.message.reply_text(mt.voice_already_saved.format(voice))


def _get_pages_buttons(
    current_page: int, count_voices: int, category: str, subcategory: str
) -> list[InlineKeyboardButton]:
    real_count_pages, pages_buttons = math.ceil(count_voices / MAX_VOICES), []
    start_page, end_page = _get_pages_info(
        current_page=current_page, real_count_pages=real_count_pages
    )

    if current_page + 2 > MAX_PAGES:
        pages_buttons.append(
            InlineKeyboardButton("<", callback_data=f"{category}_{subcategory}_{current_page - 1}")
        )

    for page_idx in range(start_page, end_page + 1):
        if current_page == page_idx:
            page_idx = "*"
        pages_buttons.append(
            InlineKeyboardButton(
                f"{page_idx}", callback_data=f"{category}_{subcategory}_{page_idx}"
            )
        )

    if current_page + 2 < real_count_pages and real_count_pages > MAX_PAGES:
        pages_buttons.append(
            InlineKeyboardButton(">", callback_data=f"{category}_{subcategory}_{current_page + 1}")
        )

    return pages_buttons


def _get_pages_info(current_page: int, real_count_pages: int) -> tuple:
    if real_count_pages <= MAX_PAGES:
        return 1, real_count_pages
    else:
        if current_page in [1, 2]:
            return 1, MAX_PAGES if real_count_pages > MAX_PAGES else real_count_pages
        elif current_page + 2 < real_count_pages:
            return current_page - 2, current_page + 2
        else:
            return real_count_pages - (MAX_PAGES - 1), real_count_pages


__all__ = ["show_voices"]
