from copy import deepcopy

from sqlalchemy import BIGINT, BOOLEAN, Column, Table, false

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers

user_model = Table(
    "users",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    Column("telegram_id", BIGINT,                          nullable=False, unique=True,  comment="Telegram ID"),
    Column("is_manager",  BOOLEAN, server_default=false(), nullable=False, unique=False, comment="Статус менеджера"),
    schema="public",
    comment="Пользователи"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(model=user_model)

__all__ = ["user_model", "create_datetime_trigger", "drop_datetime_trigger"]
