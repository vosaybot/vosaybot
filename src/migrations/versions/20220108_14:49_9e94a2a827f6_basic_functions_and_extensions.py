"""basic functions and extensions

Revision ID: 9e94a2a827f6
Revises: 
Create Date: 2022-01-08 14:49:11.519790

"""
from alembic import op

revision = "9e94a2a827f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # more details about extensions and functions can be found here:
    # https://postgrespro.com/docs/postgresql/14/sql-createextension
    # https://postgrespro.com/docs/postgresql/14/sql-createfunction
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_datetime()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now(); 
            RETURN NEW;
        END;
        $$ language 'plpgsql'
        """
    )


def downgrade():
    op.execute("DROP FUNCTION update_datetime()")
    op.execute('DROP EXTENSION "uuid-ossp"')
