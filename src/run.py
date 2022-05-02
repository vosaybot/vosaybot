from loguru import logger
from telegram.error import InvalidToken, NetworkError, Unauthorized

from bot import app
from settings import configure_logger, development_mode, production_mode, settings


def run():
    configure_logger()
    try:
        logger.info("Run bot...")
        app.start_polling()
        app.idle()
    except (InvalidToken, Unauthorized) as err:
        logger.error("Invalid telegram token.")
    except NetworkError as err:
        logger.error("Failed to establish a connection to the server.")


if __name__ == "__main__" and settings.mode == production_mode:
    run()
elif __name__ == "__main__" and settings.mode == development_mode:
    if settings.debug:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
    run()
