from typing import Tuple

from sqlalchemy import DDL, Table, event
from sqlalchemy.sql.ddl import DDLElement

create_datetime_trigger_sql = """
    CREATE TRIGGER modified_at BEFORE INSERT OR UPDATE
    ON {} FOR EACH ROW EXECUTE PROCEDURE update_datetime()
"""
drop_datetime_trigger_sql = """
    DROP TRIGGER IF EXISTS modified_at ON {}
"""


def _create_datetime_trigger(model: Table) -> DDLElement:
    trigger = DDL(create_datetime_trigger_sql.format(model.fullname)).execute_if(
        dialect="postgresql"
    )
    event.listen(model, "after_create", trigger)
    return trigger


def _drop_datetime_trigger(model: Table) -> DDLElement:
    trigger = DDL(drop_datetime_trigger_sql.format(model.fullname)).execute_if(
        dialect="postgresql"
    )
    event.listen(model, "before_drop", trigger)
    return trigger


# more details about triggers can be found here:
# https://gist.github.com/jasco/5f742709088f80f07eb2e0d6a141d3f2
# https://stackoverflow.com/questions/16629037/how-do-i-get-alembic-to-emit-custom-ddl-on-after-create
def initialize_datetime_triggers(model: Table) -> Tuple[DDLElement, DDLElement]:
    return _create_datetime_trigger(model=model), _drop_datetime_trigger(model=model)


__all__ = ["initialize_datetime_triggers"]
