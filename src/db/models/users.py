"""users model file"""

from sqlalchemy import Boolean, String, LargeBinary, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import mapped_column
from .base import Base


class Users(Base):
    __tablename__ = 'users'

    login = mapped_column(String(30), unique=True, nullable=False)
    name = mapped_column(String(40), nullable=False)
    last_name = mapped_column(String(40), nullable=False)
    patronymic = mapped_column(String(40), nullable=False)

    active = mapped_column(Boolean, server_default="True")

    password = mapped_column(LargeBinary, unique=True, nullable=False)
    salt = mapped_column(LargeBinary, unique=True, nullable=False)

    date_last_changes_password = mapped_column(DateTime)
    date_creating = mapped_column(DateTime, nullable=False, server_default=func.now())

    id_department = mapped_column(Integer, ForeignKey("departments.id", ondelete="RESTRICT"))
    creator_id = mapped_column(Integer, ForeignKey("admins_data.id", ondelete="SET NULL"))

    __table_args__ = (UniqueConstraint('last_name', 'name', 'patronymic', name='_uq_user_name'),)
