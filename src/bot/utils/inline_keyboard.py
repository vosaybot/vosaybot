import math

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils.text import callback_text as ct

MAX_PAGES, MAX_VOICES = 5, 5


def update_voice_inline_button(
    reply_markup: InlineKeyboardMarkup, data: str, voice_uuid: str, is_delete_button: bool = False
):
    for buttons in reply_markup.inline_keyboard:
        for button in buttons:
            if button.callback_data == data:
                if is_delete_button:
                    button.text = ct.delete_voice_button
                    button.callback_data = f"d_{voice_uuid}"
                else:
                    button.text = ct.save_voice_button
                    button.callback_data = f"s_{voice_uuid}"
                return


def build_page_buttons(
    current_page: int, count_voices: int, category: str, subcategory: str
) -> list[InlineKeyboardButton]:
    if count_voices <= MAX_VOICES:
        return []

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
