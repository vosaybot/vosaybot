"""table users

Revision ID: 3a0adde3c300
Revises: 0e918334a3fa
Create Date: 2023-06-19 14:19:15.114481

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as pl

from models.user_voice_relations import create_datetime_trigger as cdtuvr
from models.user_voice_relations import drop_datetime_trigger as ddtuvr
from models.users import create_datetime_trigger as cdtu
from models.users import drop_datetime_trigger as ddtu

revision = "3a0adde3c300"
down_revision = "0e918334a3fa"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "users",
        sa.Column("uuid",       pl.UUID(),                   server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="UUID ресурса"),
        sa.Column("created_at", pl.TIMESTAMP(timezone=True), server_default=sa.text("now()"),              nullable=False, comment="Дата создания"),
        sa.Column("updated_at", pl.TIMESTAMP(timezone=True),                                               nullable=False, comment="Дата обновления"),
        sa.Column("is_active",  sa.BOOLEAN(),                server_default=sa.text("true"),               nullable=False, comment="Статус активности"),

        sa.Column("telegram_id", sa.BIGINT(),                                   nullable=False, comment="Telegram ID"),
        sa.Column("is_manager",  sa.BOOLEAN(), server_default=sa.text("false"), nullable=False, comment="Статус менеджера"),

        sa.PrimaryKeyConstraint("uuid"),

        sa.UniqueConstraint("telegram_id"),

        schema="public",
        comment="Пользователи"
    )
    cdtu(target=None, bind=op.get_bind())

    op.create_table(
        # fmt: off
        "user_voice_relations",
        sa.Column("uuid",       pl.UUID(),                   server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="UUID ресурса"),
        sa.Column("created_at", pl.TIMESTAMP(timezone=True), server_default=sa.text("now()"),              nullable=False, comment="Дата создания"),
        sa.Column("updated_at", pl.TIMESTAMP(timezone=True),                                               nullable=False, comment="Дата обновления"),
        sa.Column("is_active",  sa.BOOLEAN(),                server_default=sa.text("true"),               nullable=False, comment="Статус активности"),

        sa.Column("user_uuid",  pl.UUID(), nullable=False, comment="UUID пользователя"),
        sa.Column("voice_uuid", pl.UUID(), nullable=False, comment="UUID голосового сообщения"),

        sa.ForeignKeyConstraint(["user_uuid"],  ["public.users.uuid"],  onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["voice_uuid"], ["public.voices.uuid"], onupdate="CASCADE", ondelete="CASCADE"),

        sa.PrimaryKeyConstraint("uuid"),

        sa.UniqueConstraint("user_uuid", "voice_uuid", name="uc_user_voice"),

        schema="public",
        comment="Отношение пользователей и голосовых сообщений"
    )
    cdtuvr(target=None, bind=op.get_bind())


def downgrade():
    ddtuvr(target=None, bind=op.get_bind())
    ddtu(target=None, bind=op.get_bind())
    op.drop_table("user_voice_relations", schema="public")
    op.drop_table("users", schema="public")
