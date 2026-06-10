from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseDbModel


class User(BaseDbModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str | None] = mapped_column(sa.String, unique=True)
    password: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    user_name: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    first_name: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    activated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=True)
    is_admin: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    token: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    token_send_time: Mapped[datetime | None] = mapped_column(sa.DateTime, nullable=True)
