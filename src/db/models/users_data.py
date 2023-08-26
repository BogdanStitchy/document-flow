"""users_data model file"""

from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column
from .base import Base

# Base = declarative_base()


class UsersData(Base):
    __tablename__ = 'users_data'

    name = mapped_column(String(40), nullable=False)
    last_name = mapped_column(String(40), nullable=False)
    patronymic = mapped_column(String(40), nullable=False)
    date_creating = mapped_column(DateTime, nullable=False)
    id_department = mapped_column(Integer, ForeignKey("departments.id", ondelete="RESTRICT"))
    creator_id = mapped_column(Integer, ForeignKey("admins_data.id", ondelete="SET NULL"))

    __table_args__ = (UniqueConstraint('last_name', 'name', 'patronymic', name='_uq_user_name'),)
