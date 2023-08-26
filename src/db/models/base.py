"""admins_data model file"""
from sqlalchemy import Integer
from sqlalchemy.orm import as_declarative, mapped_column


@as_declarative()
class Base():
    id = mapped_column(Integer, autoincrement=True, primary_key=True)
