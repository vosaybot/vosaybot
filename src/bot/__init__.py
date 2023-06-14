from telegram.ext import CallbackQueryHandler, CommandHandler, InlineQueryHandler, ApplicationBuilder, Application

from bot.services.base import start
from bot.services.voices import show_voices
from bot.services.users import delete_account_step_two, delete_account_step_one, delete_voice, show_my_voices
from settings import settings, database
from loguru import logger

async def post_init(app: Application) -> None:
    if not database.is_connected:
        logger.info("Подключение к базе данных...")
        await database.connect()
        logger.info("Успешно подключено!")


app = ApplicationBuilder().token(token=settings.telegram_token).post_init(post_init)
if settings.telegram_base_url:
    app.base_url(settings.telegram_base_url).build()
app = app.build()


# base
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(start, pattern="show_menu"))

# users
app.add_handler(CommandHandler("my_voices", show_my_voices))
app.add_handler(CallbackQueryHandler(show_my_voices, pattern="my_voices"))
app.add_handler(CallbackQueryHandler(delete_voice, pattern="d_"))
app.add_handler(
    CommandHandler("delete_account", delete_account_step_one)
)
app.add_handler(
    CallbackQueryHandler(delete_account_step_two, pattern="delete_account")
)

# voices
app.add_handler(CallbackQueryHandler(show_voices, pattern=""))


# lnlines
#app.add_handler(InlineQueryHandler(search))
