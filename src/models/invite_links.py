from copy import deepcopy

from sqlalchemy import VARCHAR, Column, Table

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers

invite_link_model = Table(
    "invite_links",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("title", VARCHAR(length=255), nullable=False, comment="Title"),
    Column("description", VARCHAR(length=1024), nullable=True, comment="Description"),
    schema="public",
    comment="Invite links"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(
    model=invite_link_model
)

__all__ = ["invite_link_model"]
