"""create table emotions

Revision ID: 7db2705b1b0e
Revises: a81e4bcce244
Create Date: 2022-02-07 05:35:44.549855

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.emotions import create_datetime_trigger, drop_datetime_trigger

revision = "7db2705b1b0e"
down_revision = "a81e4bcce244"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "emotions",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("title", sa.VARCHAR(length=50), nullable=False, comment="Title"),
        sa.Column("slug", sa.Enum("me", "happy", "joy", "sadness", "anger", "question", "gloat", "agreement", "threat", "jealousy", "inspiration", "disappointment", "command", "greetings", "answer", "sarcasm", "other", "contempt", name="available_emotions"), nullable=False, comment="Slug"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("title"),
        schema="public",
        comment="Emotions"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("emotions", schema="public")
