from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.utils import check_user, ct, delete_previous_messages, mt
from models import user_model
from settings import database


@check_user
@delete_previous_messages
async def delete_account_step_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        mt.delete_account_step_one,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(ct.delete_account, callback_data="delete_account")]]
        ),
    )


@check_user
@delete_previous_messages
async def delete_account_step_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await database.execute(
        user_model.delete().where(user_model.c.telegram_id == update.effective_user.id)
    )
    await update.callback_query.message.edit_text(
        mt.delete_account_step_two, parse_mode=ParseMode.MARKDOWN
    )


__all__ = ["delete_account_step_one", "delete_account_step_two"]
