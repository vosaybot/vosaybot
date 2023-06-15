from telegram import Update
from telegram.ext import ContextTypes

from bot.utils import check_user, mt
from bot.utils.decorators import delete_previous_messages


@check_user
@delete_previous_messages
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=mt.help)


__all__ = ["help"]
