from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.utils.decorators import check_user, delete_previous_messages
from bot.utils.text import mt


@check_user
@delete_previous_messages
async def help_advanced(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=mt.help_advanced, parse_mode=ParseMode.MARKDOWN)


__all__ = ["help_advanced"]
