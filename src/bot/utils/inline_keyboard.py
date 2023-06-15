import math

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils.constants import MAX_PAGES, MAX_VOICES
from bot.utils.text import cdp, ct


def update_voice_inline_button(
    reply_markup: InlineKeyboardMarkup, data: str, voice_uuid: str, is_delete_button: bool = False
):
    keyboard = []
    for buttons in reply_markup.inline_keyboard:
        row = []
        for button in buttons:
            text, callback_data = button.text, button.callback_data
            if button.callback_data == data:
                if is_delete_button:
                    text, callback_data = ct.delete_voice_button, f"{cdp.delete_voice}{voice_uuid}"
                else:
                    text, callback_data = ct.save_voice_button, f"{cdp.save_voice}{voice_uuid}"
            row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def build_page_buttons(
    prefix: str, current_page: int, count_voices: int
) -> list[InlineKeyboardButton]:
    if count_voices <= MAX_VOICES:
        return []

    real_count_pages, pages_buttons = math.ceil(count_voices / MAX_VOICES), []
    start_page, end_page = _get_pages_info(
        current_page=current_page, real_count_pages=real_count_pages
    )

    if current_page + 2 > MAX_PAGES:
        pages_buttons.append(
            InlineKeyboardButton("<", callback_data=f"{prefix}_{current_page - 1}")
        )

    for page_idx in range(start_page, end_page + 1):
        if current_page == page_idx:
            page_idx = "*"
        pages_buttons.append(
            InlineKeyboardButton(f"{page_idx}", callback_data=f"{prefix}_{page_idx}")
        )

    if current_page + 2 < real_count_pages and real_count_pages > MAX_PAGES:
        pages_buttons.append(
            InlineKeyboardButton(">", callback_data=f"{prefix}_{current_page + 1}")
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
