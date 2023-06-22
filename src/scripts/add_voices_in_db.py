import re
from pathlib import Path

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from models import categories, emotions, subcategories, voice_model
from settings import settings

assets_dir = Path("/bot/assets")

database = create_engine(settings.db_url)


def voice_is_valid(file_name: str) -> bool:
    return True if re.match("^.*\S-\S.*.ogg$", file_name) else False


def get_voices_from_dir(voice_dir: Path) -> list:
    return [voice for voice in voice_dir.iterdir() if voice.is_file()]


def add_voice(voice_title: Path, path: str, category: str, subcategory: str, emotion: str):
    database.execute(
        voice_model.insert().values(
            title=voice_title.name.split("-", maxsplit=1)[1].replace(".ogg", ""),
            performer=voice_title.name.split("-", maxsplit=1)[0],
            path=path,
            category=category,
            emotion=emotion,
            subcategory=subcategory,
        )
    )


def get_type(name: str, enum) -> str:
    for e in enum:
        if e.value == name:
            return e.name
    raise ValueError(f"Ошибка при парсинге: {name}!")


def parse_voices_dir(category: Path) -> None:
    category_name = get_type(name=category.name, enum=categories)

    for subcategory in [subcategory for subcategory in category.iterdir() if subcategory.is_dir()]:
        subcategory_name = get_type(name=subcategory.name, enum=subcategories)

        for emotion in [emotion for emotion in subcategory.iterdir() if emotion.is_dir()]:
            emotion_name = get_type(name=emotion.name, enum=emotions)
            voices = get_voices_from_dir(voice_dir=emotion)

            for voice in voices:
                if (
                    not voice_is_valid(file_name=voice.name)
                    or database.execute(
                        voice_model.select()
                        .with_only_columns(voice_model.c.uuid)
                        .where(
                            voice_model.c.title
                            == voice.name.split("-", maxsplit=1)[1].replace(".ogg", ""),
                            voice_model.c.category == category_name,
                            voice_model.c.subcategory == subcategory_name,
                            voice_model.c.emotion == emotion_name,
                            voice_model.c.performer == voice.name.split("-", maxsplit=1)[0],
                        )
                    ).first()
                ):
                    logger.error(f"Голосовое сообщение {voice} пропущено!")
                    continue

                try:
                    add_voice(
                        voice_title=voice,
                        path=f"{category.name}/{subcategory.name}/{emotion.name}/{voice.name}",
                        category=category_name,
                        subcategory=subcategory_name,
                        emotion=emotion_name,
                    )
                    logger.info(f"Голосовое сообщение {voice} добавлено.")
                except IntegrityError as err:
                    logger.error(str(err))


if __name__ == "__main__":
    for category in [category for category in assets_dir.iterdir() if category.is_dir()]:
        parse_voices_dir(category=category)
