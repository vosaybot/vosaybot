import enum
from copy import deepcopy

from sqlalchemy import VARCHAR, Column, Table, UniqueConstraint

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers

subcategory_model = Table(
    "subcategories",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("title", VARCHAR(length=50), nullable=False, unique=True, comment="Title"),
    Column("slug", VARCHAR(length=255), nullable=False, unique=True, comment="Slug"),
    schema="public",
    comment="Subcategories"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(
    model=subcategory_model
)

__all__ = ["subcategory_model"]
