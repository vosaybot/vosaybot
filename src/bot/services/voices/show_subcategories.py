from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.text import cdp, ct, mt
from models import categories, subcategories

_sc_matching = {
    categories.games.name: [
        subcategories.hearthstoneblackmount,
        subcategories.warcraft3,
        subcategories.kuzya,
    ],
    categories.films.name: [
        subcategories.twelve_chairs,
        subcategories.brother,
        subcategories.loveandpigeons,
        subcategories.matrix,
    ],
    categories.politicians.name: [
        subcategories.alexanderlukashenko,
        subcategories.alexeinavalny,
        subcategories.vladimirzhirinovsky,
        subcategories.volodymyrzelenskyy,
        subcategories.vladimirputin,
    ],
    categories.other.name: [subcategories.mems],
}


@check_user
@delete_previous_messages
async def show_subcategory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    category_slug = update.callback_query.data.replace(cdp.show_subcategory, "")
    keyboard = [
        [
            InlineKeyboardButton(
                sc.value, callback_data=f"{cdp.show_voice}{category_slug}_{sc.name}_1"
            )
        ]
        for sc in _sc_matching[category_slug]
    ]
    keyboard.append([InlineKeyboardButton(ct.back, callback_data=cdp.show_categories)])

    res = await update.callback_query.message.reply_text(
        text=mt.select_category if len(keyboard) > 1 else mt.voices_not_found,
        reply_markup=InlineKeyboardMarkup(keyboard),
        quote=False,
    )

    context.user_data["voices_message_id"] = [res.message_id]


__all__ = ["show_subcategory"]
