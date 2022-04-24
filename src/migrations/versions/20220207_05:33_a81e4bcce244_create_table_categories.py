"""create table categories

Revision ID: a81e4bcce244
Revises: 9e94a2a827f6
Create Date: 2022-02-07 05:33:51.981886

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.categories import create_datetime_trigger, drop_datetime_trigger

revision = "a81e4bcce244"
down_revision = "9e94a2a827f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "categories",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("title", sa.VARCHAR(length=50), nullable=False, comment="Title"),
        sa.Column("slug", sa.Enum("games", "films", "other", name="available_categories"), nullable=False, comment="Slug"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("title"),
        schema="public",
        comment="Categories"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("categories", schema="public")
