from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.text import mt


@check_user
@delete_previous_messages
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=mt.start)


__all__ = ["start"]
