"""file with database access methods for super admin role"""

from sqlalchemy import select, update, insert, delete
from sqlalchemy.orm import Session
import pydantic

from src.db.database_setup import get_engine
from src.db.models.admins import Admins
from src.db.models.departments import Departments
from src.db.models.departments_hierarhcy import DepartmentsHierarchy

from src.db.methods.admin_db_methods import AdminDB


class SuperAdminMethodsDB(AdminDB):
    # _________________________________ADD______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def add_admin(name: str, patronymic: str, last_name: str, login: str, password: bytes, salt: bytes,
                  flag_super_admin: bool = True) -> int:
        """
        :return: id_added_admin: int
        """
        with Session(get_engine()) as session:
            with session.begin():
                new_admin = Admins(name=name, last_name=last_name, patronymic=patronymic, active=True, login=login,
                                   password=password, salt=salt, super_admin_flag=flag_super_admin)

                session.add(new_admin)
                session.commit()
            return new_admin.id

    @staticmethod
    @pydantic.validate_call
    def add_department(name_department: str, number_department: int) -> int:
        with Session(get_engine()) as session:
            with session.begin():
                new_department = Departments(name_department=name_department, number_department=number_department)
                session.add(new_department)
                session.commit()
            return new_department.id

    @staticmethod
    @pydantic.validate_call
    def add_one_hierarchy_department(id_department: int, parent_id: int) -> None:
        with Session(get_engine()) as session:
            with session.begin():
                session.execute(
                    insert(DepartmentsHierarchy).values(department_id=id_department, parent_id=parent_id, level=1))
                session.commit()

    @staticmethod
    @pydantic.validate_call
    def update_full_hierarchy(list_hierarchy: list):
        with Session(get_engine()) as session:
            with session.begin():
                for row in list_hierarchy:
                    stmt = update(DepartmentsHierarchy).where(
                        DepartmentsHierarchy.department_id == row['department_id']).values(parent_id=row['parent_id'])
                    session.execute(stmt)
                session.commit()

    # _________________________________GET_______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def get_all_admins() -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(select(Admins.__table__))
                admins = result.mappings().fetchall()
                return admins

    @staticmethod
    @pydantic.validate_call
    def get_one_admin(id_admin: int) -> {}:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(Admins.__table__).where(Admins.__table__.c.id == id_admin))
                admin = result.mappings().fetchone()
                return admin

    @staticmethod
    @pydantic.validate_call
    def get_all_departments() -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(select(Departments.__table__))
                departments = result.mappings().fetchall()
                return departments

    @staticmethod
    @pydantic.validate_call
    def get_full_hierarchy_departments() -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(DepartmentsHierarchy.__table__).where(DepartmentsHierarchy.__table__.c.level == 1))
                hierarchy_departments = result.mappings().fetchall()
                return hierarchy_departments

    # ________________________________UPDATE_____________________________________________________
    @staticmethod
    @pydantic.validate_call
    def change_admin_activity_status(id_admin: int):
        with Session(get_engine()) as session:
            with session.begin():
                admin = session.query(Admins).filter_by(id=id_admin).first()
                if admin:
                    admin.active = not admin.active
                    session.commit()
                else:
                    raise ValueError(f"Администратор с id {id_admin} не найден.")

    @staticmethod
    @pydantic.validate_call
    def update_all_departments(list_departments: list):
        with Session(get_engine()) as session:
            with session.begin():
                for row in list_departments:
                    stmt = update(Departments).where(Departments.id == row['id']).values(
                        number_department=row['number_department'],
                        name_department=row['name_department'])
                    session.execute(stmt)
                session.commit()

    # ________________________________DELETE_____________________________________________________
    @staticmethod
    @pydantic.validate_call()
    def delete_departments(id_departments_for_delete: list):
        with Session(get_engine()) as session:
            with session.begin():
                condition = Departments.id.in_(id_departments_for_delete)
                delete_stmt = delete(Departments).where(condition)
                session.execute(delete_stmt)
                session.commit()
