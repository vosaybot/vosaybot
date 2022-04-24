"""create table subcategories

Revision ID: cf07579a9d1a
Revises: 7db2705b1b0e
Create Date: 2022-02-07 05:36:55.122781

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.subcategories import create_datetime_trigger, drop_datetime_trigger

revision = "cf07579a9d1a"
down_revision = "7db2705b1b0e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "subcategories",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("title", sa.VARCHAR(length=50), nullable=False, comment="Title"),
        sa.Column("slug", sa.VARCHAR(length=255), nullable=False, comment="Slug"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("title"),
        schema="public",
        comment="Subcategories"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("subcategories", schema="public")
