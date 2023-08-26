"""admins_data model file"""

from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy.orm import mapped_column
from .base import Base


class AdminsData(Base):
    __tablename__ = 'admins_data'

    name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    patronymic = mapped_column(String, nullable=False)
    date_creating = mapped_column(DateTime, nullable=False)

    __table_args__ = (UniqueConstraint('last_name', 'name', 'patronymic', name='_uq_admin_name'),)
