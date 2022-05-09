import enum
from copy import deepcopy

from sqlalchemy import VARCHAR, Column, Enum, Table

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers


class available_categories(enum.Enum):
    games = "games"
    films = "films"
    other = "other"
    politicians = "politicians"


category_model = Table(
    "categories",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("title", VARCHAR(length=50), nullable=False, unique=True, comment="Title"),
    Column("slug", Enum(available_categories), nullable=False, unique=True, comment="Slug"),
    schema="public",
    comment="Categories"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(model=category_model)

__all__ = ["category_model", "available_categories"]
