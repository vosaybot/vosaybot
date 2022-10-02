from sqlalchemy import BOOLEAN, Column, FetchedValue, MetaData, func, true
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

metadata = MetaData()
# Подробнее о поле DATETIME/TIMESTAMP можно посмотреть тут:
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
base_fields = (
    # fmt: off
    Column("uuid", UUID, primary_key=True, server_default=func.uuid_generate_v4(), comment="UUID ресурса"),
    Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment="Дата создания"),
    Column("updated_at", TIMESTAMP(timezone=True), server_onupdate=FetchedValue(), nullable=False, comment="Дата обновления"),
    Column("is_active", BOOLEAN, server_default=true(), nullable=False, comment="Статус активности"),
)


__all__ = ["base_fields", "metadata"]
