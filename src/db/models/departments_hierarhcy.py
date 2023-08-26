"""departments_hierarchy model file"""
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, declarative_base
from .base import Base


class DepartmentsHierarchy(Base):
    __tablename__ = "departments_hierarchy"

    department_id = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"))
    parent_id = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"))
    level = mapped_column(Integer, nullable=False)
