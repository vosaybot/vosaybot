import enum
from copy import deepcopy

from sqlalchemy import VARCHAR, Column, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers


class categories(enum.Enum):
    games = "Игры"
    films = "Фильмы"
    politicians = "Политики"
    other = "Другое"


class subcategories(enum.Enum):
    # Игры
    hearthstoneblackmount = "Hearthstone: Blackrock Mountain"
    warcraft3 = "Warcraft III"
    kuzya = "Кузя"

    # Фильмы
    twelve_chairs = "12 стульев"
    brother = "Брат и Брат2"
    loveandpigeons = "Любовь и голуби"
    matrix = "Матрица"

    # Политики
    alexanderlukashenko = "Александр Лукашенко"
    alexeinavalny = "Алексей Навальный"
    vladimirzhirinovsky = "Владимир Жириновский"
    volodymyrzelenskyy = "Владимир Зеленский"
    vladimirputin = "Владимир Путин"

    # Другое
    mems = "Мемы"


class emotions(enum.Enum):
    me = "Обо мне"
    joy = "Радость"
    sadness = "Грусть"
    anger = "Злость"
    question = "Вопрос"
    gloat = "Злорадство"
    agreement = "Согласие"
    threat = "Угроза"
    jealousy = "Ревность"
    inspiration = "Воодушевление"
    disappointment = "Разочарование"
    command = "Приказ"
    greetings = "Приветствие"
    answer = "Ответ"
    sarcasm = "Сарказм"
    other = "Другое"
    contempt = "Презрение"


CATEGORIES_ENUM = ENUM(
    categories, values_callable=lambda categories: [e.value for e in categories]
)
SUBCATEGORIES_ENUM = ENUM(
    subcategories, values_callable=lambda subcategories: [e.value for e in subcategories]
)
EMOTIONS_ENUM = ENUM(emotions, values_callable=lambda emotions: [e.value for e in emotions])

voice_model = Table(
    "voices",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    # more information on the maximum file name and url sizes can be found here:
    # https://serverfault.com/questions/9546/filename-length-limits-on-linux
    # https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    Column("title",       VARCHAR(length=255),  nullable=False, unique=False, comment="Название"),
    Column("performer",   VARCHAR(length=255),  nullable=False, unique=False, comment="Исполнитель"),
    Column("path",        VARCHAR(length=2000), nullable=False, unique=True,  comment="Путь"),
    Column("category",    CATEGORIES_ENUM,      nullable=False, unique=False, comment="Категория"),
    

    Column("subcategory", SUBCATEGORIES_ENUM,   nullable=False, unique=False, comment="Подкатегории"),
    Column("emotion",     EMOTIONS_ENUM,        nullable=False, unique=False, comment="Эмоции"),

    UniqueConstraint("title", "performer", "category", "subcategory", "emotion", name="uc_all"),
    
    schema="public",
    comment="Голосовые сообщения"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(model=voice_model)

__all__ = ["categories", "subcategories", "emotions", "voice_model"]
