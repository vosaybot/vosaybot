from loguru import logger
from telegram.error import Forbidden, InvalidToken, NetworkError

from bot import app
from settings import configure_logger, development_mode, production_mode, settings


def run():
    configure_logger()
    try:
        logger.info("Запуск бота...")
        app.run_polling()
    except (InvalidToken, Forbidden):
        logger.error("Невалидный токен.")
    except NetworkError:
        logger.error("Ошибка при подключении к серверу.")


if __name__ == "__main__" and settings.mode == production_mode:
    run()
elif __name__ == "__main__" and settings.mode == development_mode:
    if settings.debug:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    run()
