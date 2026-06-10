from datetime import datetime, timezone
from typing import Type, TypeVar

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import current_timestamp

MODEL = TypeVar("MODEL", bound="BaseDbModel")


class BaseDbModel(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=current_timestamp(),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=current_timestamp(),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def update_orm(self: Type[MODEL], data: dict):
        for key, item in data.items():
            setattr(self, key, item)
