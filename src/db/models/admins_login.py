"""admins_login model file"""

from sqlalchemy import Boolean, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column
from .base import Base


class AdminsLogin(Base):
    __tablename__ = 'admins_login'

    id = mapped_column(ForeignKey('admins_data.id', ondelete="CASCADE"), primary_key=True)
    active = mapped_column(Boolean, server_default="True")
    login = mapped_column(String(30), nullable=False)
    password = mapped_column(LargeBinary, unique=True, nullable=False)
    salt = mapped_column(LargeBinary, unique=True, nullable=False)
    super_admin_flag = mapped_column(Boolean, server_default="False")
    date_last_changes_password = mapped_column(DateTime)
