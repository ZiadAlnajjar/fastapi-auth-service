from sqlalchemy import MetaData, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from ulid import ULID

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata

    id: Mapped[str] = mapped_column(String(26), primary_key=True, default=lambda: str(ULID()))

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()

    def __repr__(self) -> str:
        attrs = [f"{k}={v!r}" for k, v in vars(self).items() if not k.startswith("_")]
        return f"<{self.__class__.__name__}({', '.join(attrs)})>"
