import logging

from loguru import logger

from settings.base import database, development_mode, production_mode, root_dir, settings


def configure_logger():
    """Configuring a logger for the entire project."""

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level="NOTSET")
    logger.add(
        sink=root_dir.joinpath("logs/bot.log"),
        level="INFO",
        format="uptime:{elapsed} | time:{time} | {level} | {name}:{line} | {message}",
        rotation="1 month",
        compression="gz",
    )
    # show project settings before launch
    logger.info("Project settings:\n{}".format(settings.json(indent=4)))


__all__ = [
    "database",
    "development_mode",
    "production_mode",
    "root_dir",
    "settings",
    "configure_logger",
]
