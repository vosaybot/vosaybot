from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.text import cdp, ct, mt
from models import category_model, subcategory_model, voice_model
from settings import database


@check_user
@delete_previous_messages
async def show_subcategory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    category_slug = update.callback_query.data.replace(cdp.show_subcategory, "")
    subcategories = (
        voice_model.select()
        .distinct()
        .select_from(voice_model)
        .with_only_columns(subcategory_model.c.title, subcategory_model.c.slug)
        .where(category_model.c.slug == category_slug)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
    )

    keyboard = [
        [
            InlineKeyboardButton(
                row.title, callback_data=f"{cdp.show_voice}{category_slug}_{row['slug']}_1"
            )
        ]
        for row in await database.fetch_all(subcategories)
    ]
    keyboard.append([InlineKeyboardButton(ct.back, callback_data=cdp.show_categories)])

    res = await update.callback_query.message.reply_text(
        text=mt.select_category if len(keyboard) > 1 else mt.voices_not_found,
        reply_markup=InlineKeyboardMarkup(keyboard),
        quote=False,
    )

    context.user_data["voices_message_id"] = [res.message_id]


__all__ = ["show_subcategory"]
