"""file with database access methods for super admin role"""

from sqlalchemy import select
from sqlalchemy.orm import Session
import pydantic

from src.db.database_setup import get_engine
from src.db.models.admins import Admins
from src.db.models.departments import Departments
from src.db.methods.admin_db_methods import AdminDB


class SuperAdminDB(AdminDB):
    @staticmethod
    @pydantic.validate_call
    def add_admin(name: str, patronymic: str, last_name: str, login: str, password: bytes, salt: bytes) -> int:
        """
        :return: id_added_admin: int
        """
        with Session(get_engine()) as session:
            with session.begin():
                new_admin = Admins(name=name, last_name=last_name, patronymic=patronymic, active=True, login=login,
                                   password=password, salt=salt)

                session.add(new_admin)
                session.commit()
            return new_admin.id

    @staticmethod
    @pydantic.validate_call
    def add_department(name_department: str, number_department: int) -> None:
        with Session(get_engine()) as session:
            with session.begin():
                new_department = Departments(name_department=name_department, number_department=number_department)
                session.add(new_department)
                session.commit()
