"""admins model file"""

from sqlalchemy import Boolean, String, LargeBinary, DateTime, UniqueConstraint, func
from sqlalchemy.orm import mapped_column
from .base import Base


class Admins(Base):
    __tablename__ = 'admins'

    login = mapped_column(String(30), unique=True, nullable=False)
    name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    patronymic = mapped_column(String, nullable=False)

    active = mapped_column(Boolean, server_default="True")
    super_admin_flag = mapped_column(Boolean, server_default="False")

    password = mapped_column(LargeBinary, unique=True, nullable=False)
    salt = mapped_column(LargeBinary, unique=True, nullable=False)

    date_creating = mapped_column(DateTime, nullable=False, server_default=func.now())
    date_last_changes_password = mapped_column(DateTime)

    __table_args__ = (UniqueConstraint('last_name', 'name', 'patronymic', name='_uq_admin_name'),)
