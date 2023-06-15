from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.utils import check_user, mt
from bot.utils.decorators import delete_previous_messages
from models import category_model
from settings import database


@check_user
@delete_previous_messages
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(row["title"], callback_data=row["slug"].value)]
            for row in await database.fetch_all(
                category_model.select().with_only_columns(
                    category_model.c.title, category_model.c.slug
                )
            )
        ]
    )
    await _make_answer(
        update=update, context=context, text=mt.select_category, reply_markup=reply_markup
    )


async def _make_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    reply_markup: InlineKeyboardMarkup,
) -> None:
    if update.message:
        res = await update.message.reply_text(text, reply_markup=reply_markup, quote=False)
    else:
        res = await update.callback_query.message.reply_text(
            text, reply_markup=reply_markup, quote=False
        )

    context.user_data["voices_message_id"] = [res.message_id]


__all__ = ["start"]
