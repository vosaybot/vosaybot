from sqlalchemy import BOOLEAN, Column, FetchedValue, MetaData, func, true
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

metadata = MetaData()
# more details about DATETIME / TIMESTAMP fields can be found here:
# https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
base_fields = (
    # fmt: off
    Column("uuid", UUID, primary_key=True, server_default=func.uuid_generate_v4(), comment="Resource UUID"),
    Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment="Resource creation date"),
    Column("modified_at", TIMESTAMP(timezone=True), server_onupdate=FetchedValue(), nullable=False, comment="Resource modification date"),
    Column("is_active", BOOLEAN, server_default=true(), nullable=False, comment="Resource activity status"),
)


__all__ = ["base_fields", "metadata"]
