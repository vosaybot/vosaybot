"""table voices

Revision ID: 0e918334a3fa
Revises: 9e94a2a827f6
Create Date: 2023-06-19 14:02:50.924131

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as pl

from models.voices import create_datetime_trigger, drop_datetime_trigger

revision = "0e918334a3fa"
down_revision = "9e94a2a827f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "voices",
        sa.Column("uuid",       pl.UUID(),                   server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="UUID ресурса"),
        sa.Column("created_at", pl.TIMESTAMP(timezone=True), server_default=sa.text("now()"),              nullable=False, comment="Дата создания"),
        sa.Column("updated_at", pl.TIMESTAMP(timezone=True),                                               nullable=False, comment="Дата обновления"),
        sa.Column("is_active",  sa.BOOLEAN(), server_default=sa.text("true"),                              nullable=False, comment="Статус активности"),

        sa.Column("title",       sa.VARCHAR(length=255),  nullable=False, comment="Название"),
        sa.Column("performer",   sa.VARCHAR(length=255),  nullable=False, comment="Исполнитель"),
        sa.Column("path",        sa.VARCHAR(length=2000), nullable=False, comment="Путь"),

        sa.Column("category",    pl.ENUM("games", "films", "politicians", "other", name="categories"), nullable=False, comment="Категория"),
        sa.Column("subcategory", 
            pl.ENUM("hearthstoneblackmount", "warcraft3", "kuzya", "twelve_chairs", "brother", "loveandpigeons", "matrix", "alexanderlukashenko",
                    "alexeinavalny", "vladimirzhirinovsky", "volodymyrzelenskyy", "vladimirputin", "mems",
            name="subcategories"), nullable=False, comment="Подкатегории"),
        sa.Column("emotion",
            pl.ENUM("me", "joy", "sadness", "anger", "question", "gloat", "agreement", "threat", "jealousy", "inspiration",
                    "disappointment", "command", "greetings", "answer", "sarcasm", "other", "contempt",
            name="emotions"), nullable=False, comment="Эмоции"),

        sa.PrimaryKeyConstraint("uuid"),

        sa.UniqueConstraint("path"),
        sa.UniqueConstraint("title", "performer", "category", "subcategory", "emotion", name="uc_all"),

        schema="public",
        comment="Voices"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("voices", schema="public")
