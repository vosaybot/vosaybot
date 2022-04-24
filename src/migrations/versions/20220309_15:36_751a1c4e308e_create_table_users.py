"""create table users

Revision ID: 751a1c4e308e
Revises: 4419770493ca
Create Date: 2022-03-09 15:36:25.370416

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.users import create_datetime_trigger, drop_datetime_trigger

revision = "751a1c4e308e"
down_revision = "4419770493ca"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "users",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("telegram_id", sa.BIGINT(), nullable=False, comment="Telegram ID"),
        sa.Column("is_manager", sa.BOOLEAN(), server_default=sa.text("false"), nullable=False, comment="Manager status"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("telegram_id"),
        schema="public",
        comment="Users"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("users", schema="public")
