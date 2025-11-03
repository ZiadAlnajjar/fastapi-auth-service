from datetime import datetime

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import with_loader_criteria, ORMExecuteState

from app.infrastructure.database.mixins import SoftDeleteMixin


def register_soft_delete_filter() -> None:
    @event.listens_for(AsyncSession.sync_session_class, "do_orm_execute", propagate=True)
    def _add_filter(execute_state: ORMExecuteState) -> None:
        if execute_state.is_select and not execute_state.execution_options.get("include_deleted", False):
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    SoftDeleteMixin,
                    lambda cls: cls.deleted_at.is_(None),
                    include_aliases=True
                )
            )

    @event.listens_for(AsyncSession.sync_session_class, "before_flush", propagate=True)
    def _soft_delete_before_flush(session, flush_context, instances):
        for obj in list(session.deleted):
            if isinstance(obj, SoftDeleteMixin):
                obj.deleted_at = datetime.now()
                session.add(obj)
                session.deleted.remove(obj)
