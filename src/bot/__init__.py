from telegram.ext import CallbackQueryHandler, CommandHandler, InlineQueryHandler, Updater

from bot.callbacks import delete_voice, show_voices
from bot.commands import delete_account_step_one, delete_account_step_two, show_my_voices, start
from bot.inlines import search
from settings import settings

if settings.telegram_base_url:
    app = Updater(token=settings.telegram_token, base_url=settings.telegram_base_url)
else:
    app = Updater(token=settings.telegram_token)

# callbacks
app.dispatcher.add_handler(CallbackQueryHandler(start, pattern="show_menu", run_async=True))
app.dispatcher.add_handler(
    CallbackQueryHandler(delete_account_step_two, pattern="delete_account", run_async=True)
)
app.dispatcher.add_handler(CallbackQueryHandler(delete_voice, pattern="d_", run_async=True))
app.dispatcher.add_handler(
    CallbackQueryHandler(show_my_voices, pattern="my_voices", run_async=True)
)
app.dispatcher.add_handler(CallbackQueryHandler(show_voices, pattern="", run_async=True))

# commands
app.dispatcher.add_handler(CommandHandler("start", start, run_async=True))
app.dispatcher.add_handler(CommandHandler("my_voices", show_my_voices, run_async=True))
app.dispatcher.add_handler(
    CommandHandler("delete_account", delete_account_step_one, run_async=True)
)

# lnlines
app.dispatcher.add_handler(InlineQueryHandler(search))
