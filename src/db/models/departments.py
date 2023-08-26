"""departments model file"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from .base import Base


class Departments(Base):
    __tablename__ = "departments"

    name_department = mapped_column(String(100), nullable=False)
    number_department = mapped_column(Integer)
