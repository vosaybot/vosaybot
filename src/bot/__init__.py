from loguru import logger
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    InlineQueryHandler
)

from bot.services.base import donate, help, help_advanced, search, start
from bot.services.users import (
    delete_account_step_one,
    delete_account_step_two,
    delete_voice,
    show_my_voices
)
from bot.services.voices import (
    save_voice,
    show_categories,
    show_popular,
    show_subcategory,
    show_voices
)
from bot.utils.text import cdp
from settings import database, settings


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
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("help_advanced", help_advanced))
app.add_handler(CommandHandler("donate", donate))
app.add_handler(InlineQueryHandler(search))

# users
app.add_handler(CommandHandler(cdp.show_my_voices, show_my_voices))
app.add_handler(CallbackQueryHandler(show_my_voices, pattern=cdp.show_my_voices))
app.add_handler(CallbackQueryHandler(delete_voice, pattern=cdp.delete_voice))
app.add_handler(CommandHandler("delete_account", delete_account_step_one))
app.add_handler(CallbackQueryHandler(delete_account_step_two, pattern="delete_account"))

# voices
app.add_handler(CommandHandler("voices", show_categories))
app.add_handler(CommandHandler(cdp.show_popular, show_popular))
app.add_handler(CallbackQueryHandler(show_popular, pattern=cdp.show_popular))
app.add_handler(CallbackQueryHandler(show_categories, pattern=cdp.show_categories))
app.add_handler(CallbackQueryHandler(show_subcategory, pattern=cdp.show_subcategory))
app.add_handler(CallbackQueryHandler(show_voices, pattern=cdp.show_voice))
app.add_handler(CallbackQueryHandler(save_voice, pattern=cdp.save_voice))
