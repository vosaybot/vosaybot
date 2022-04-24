"""create table user_invite_link_relations

Revision ID: 81ee5fe803b4
Revises: 8f4853cb5403
Create Date: 2022-04-24 17:36:49.461479

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.user_invite_link_relations import create_datetime_trigger, drop_datetime_trigger

revision = "81ee5fe803b4"
down_revision = "8f4853cb5403"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "user_invite_link_relations",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("user_uuid", postgresql.UUID(), nullable=False, comment="User UUID"),
        sa.Column("invite_link_uuid", postgresql.UUID(), nullable=False, comment="Invite link UUID"),
        sa.ForeignKeyConstraint(["invite_link_uuid"], ["public.invite_links.uuid"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_uuid"], ["public.users.uuid"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("user_uuid"),
        sa.UniqueConstraint("user_uuid", "invite_link_uuid", name="user_invite_link_constraint"),
        schema="public",
        comment="User invite link relations"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("user_invite_link_relations", schema="public")
