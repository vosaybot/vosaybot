"""create table voices

Revision ID: 4419770493ca
Revises: cf07579a9d1a
Create Date: 2022-02-09 13:20:24.018221

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.voices import create_datetime_trigger, drop_datetime_trigger

revision = "4419770493ca"
down_revision = "cf07579a9d1a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "voices",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="UUID ресурса"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Дата создания"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Статус активности"),
        sa.Column("updated_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Дата обновления"),
        sa.Column("title", sa.VARCHAR(length=255), nullable=False, comment="Title"),
        sa.Column("performer", sa.VARCHAR(length=255), nullable=False, comment="Performer"),
        sa.Column("path", sa.VARCHAR(length=2000), nullable=False, comment="Path"),
        sa.Column("category_uuid", postgresql.UUID(), nullable=False, comment="Category UUID"),
        sa.Column("subcategory_uuid", postgresql.UUID(), nullable=False, comment="Subcategory UUID"),
        sa.Column("emotion_uuid", postgresql.UUID(), nullable=False, comment="Emotion UUID"),
        sa.ForeignKeyConstraint(["category_uuid"], ["public.categories.uuid"], onupdate="CASCADE"),
        sa.ForeignKeyConstraint(["emotion_uuid"], ["public.emotions.uuid"], onupdate="CASCADE"),
        sa.ForeignKeyConstraint(["subcategory_uuid"], ["public.subcategories.uuid"], onupdate="CASCADE"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("path"),
        sa.UniqueConstraint("title", "performer", name="voice_constraint"),
        schema="public",
        comment="Voices"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("voices", schema="public")
