from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.utils import check_user, mt
from bot.utils.decorators import delete_previous_messages


@check_user
@delete_previous_messages
async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=mt.donate, parse_mode=ParseMode.MARKDOWN)


__all__ = ["donate"]
