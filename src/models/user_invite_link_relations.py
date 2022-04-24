from copy import deepcopy

from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers

user_invite_link_model = Table(
    "user_invite_link_relations",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("user_uuid", UUID, ForeignKey("public.users.uuid", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, unique=True, comment="User UUID"),
    Column("invite_link_uuid", UUID, ForeignKey("public.invite_links.uuid", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, comment="Invite link UUID"),
    UniqueConstraint("user_uuid", "invite_link_uuid", name="user_invite_link_constraint"),
    schema="public",
    comment="User invite link relations"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(
    model=user_invite_link_model
)

__all__ = ["user_invite_link_model", "create_datetime_trigger", "drop_datetime_trigger"]
