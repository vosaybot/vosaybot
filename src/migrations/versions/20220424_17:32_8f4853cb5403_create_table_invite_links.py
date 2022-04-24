"""create table invite_links

Revision ID: 8f4853cb5403
Revises: 7c60ed9fe75c
Create Date: 2022-04-24 17:32:27.613753

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.invite_links import create_datetime_trigger, drop_datetime_trigger

revision = "8f4853cb5403"
down_revision = "7c60ed9fe75c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "invite_links",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("title", sa.VARCHAR(length=255), nullable=False, comment="Title"),
        sa.Column("description", sa.VARCHAR(length=1024), nullable=True, comment="Description"),
        sa.PrimaryKeyConstraint("uuid"),
        schema="public",
        comment="Invite links"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("invite_links", schema="public")
