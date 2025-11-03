from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
