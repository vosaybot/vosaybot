import enum
from copy import deepcopy

from sqlalchemy import VARCHAR, Column, Enum, Table

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers


class available_emotions(enum.Enum):
    me = "me"
    happy = "happy"
    joy = "joy"
    sadness = "sadness"
    anger = "anger"
    question = "question"
    gloat = "gloat"
    agreement = "agreement"
    threat = "threat"
    jealousy = "jealousy"
    inspiration = "inspiration"
    disappointment = "disappointment"
    command = "command"
    greetings = "greetings"
    answer = "answer"
    sarcasm = "sarcasm"
    other = "other"
    contempt = "contempt"


emotion_model = Table(
    "emotions",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("title", VARCHAR(length=50), nullable=False, unique=True, comment="Title"),
    Column("slug", Enum(available_emotions), nullable=False, unique=True, comment="Slug"),
    schema="public",
    comment="Emotions"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(model=emotion_model)

__all__ = ["emotion_model", "available_emotions"]
