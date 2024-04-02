"""file with database access methods for super admin role"""
import datetime
from typing import Optional

from sqlalchemy import select, update, delete, or_
import pydantic

from src.db.database_setup import session_factory
from src.db.models.admins import Admins
from src.db.models.users import Users
from src.db.models.departments import Departments
from src.db.models.departments_hierarhcy import DepartmentsHierarchy

from src.db.methods.admin_db_methods import AdminMethodsDB


class SuperAdminMethodsDB(AdminMethodsDB):
    # _________________________________ADD______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def add_admin(name: str, patronymic: str, last_name: str, login: str, password: bytes, salt: bytes,
                  flag_super_admin: bool = False) -> int:
        """
        :return: id_added_admin: int
        """
        with session_factory() as session:
            new_admin = Admins(name=name, last_name=last_name, patronymic=patronymic, active=True, login=login,
                               password=password, salt=salt, super_admin_flag=flag_super_admin)

            session.add(new_admin)
            session.commit()
            return new_admin.id

    @staticmethod
    @pydantic.validate_call
    def add_department(name_department: str, number_department: int or None) -> int:
        with session_factory() as session:
            new_department = Departments(name_department=name_department, number_department=number_department)
            session.add(new_department)
            session.commit()
            return new_department.id

    @staticmethod
    @pydantic.validate_call
    def add_one_hierarchy_department(id_department: int, parent_id: Optional[int]) -> None:
        if id_department == parent_id:
            raise ValueError("id подчиняемого отдела не может ровняться id руководящего отдела")
        with session_factory() as session:
            new_hierarchy = DepartmentsHierarchy(department_id=id_department, parent_id=parent_id, level=1)
            session.add(new_hierarchy)
            session.commit()

    @staticmethod
    @pydantic.validate_call
    def create_full_hierarchy(list_hierarchy: list) -> None:
        with session_factory() as session:
            session.execute(delete(DepartmentsHierarchy))
            session.bulk_insert_mappings(DepartmentsHierarchy, list_hierarchy)
            session.commit()

    # _________________________________GET_______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def get_all_admins() -> [{}, {}]:
        with session_factory() as session:
            result = session.execute(select(Admins.__table__))
            admins = result.mappings().fetchall()
            return admins

    @staticmethod
    @pydantic.validate_call
    def get_one_admin(id_admin: int) -> {}:
        with session_factory() as session:
            result = session.execute(
                select(Admins.__table__).where(Admins.__table__.c.id == id_admin))
            admin = result.mappings().fetchone()
            return admin

    @staticmethod
    @pydantic.validate_call
    def find_admins_words(search_string: str) -> [{}, {}]:
        with session_factory() as session:
            result = session.execute(
                select(Admins.__table__).where(
                    or_(Admins.last_name.ilike(f"%{search_string}%"),
                        Admins.name.ilike(f"%{search_string}%"),
                        Admins.patronymic.ilike(f"%{search_string}%"),
                        Admins.login.ilike(f"%{search_string}%"))
                )
            )
            admins = result.mappings().fetchall()
            return admins

    @staticmethod
    @pydantic.validate_call
    def find_admins_period(start_date: datetime.date, end_date: datetime.date) -> [{}, {}]:
        with session_factory() as session:
            result = session.execute(
                select(Admins.__table__).where(Admins.date_creating.between(start_date, end_date))
            )
            admins = result.mappings().fetchall()
            return admins

    @staticmethod
    @pydantic.validate_call
    def get_all_departments() -> [{}, {}]:
        with session_factory() as session:
            result = session.execute(select(Departments.id,
                                            Departments.number_department, Departments.name_department))
            departments = result.mappings().fetchall()
            return departments

    @staticmethod
    @pydantic.validate_call
    def get_all_departments_without_one(id_exempt_department: int) -> [{}, {}]:
        with session_factory() as session:
            stmt = select(Departments.id, Departments.number_department, Departments.name_department
                          ).where(Departments.id != id_exempt_department)
            result = session.execute(stmt)
            departments = result.mappings().fetchall()
            return departments

    @staticmethod
    @pydantic.validate_call
    def get_full_hierarchy_departments() -> [{}, {}]:
        with session_factory() as session:
            result = session.execute(
                select(DepartmentsHierarchy.__table__).where(DepartmentsHierarchy.level == 1).order_by(
                    DepartmentsHierarchy.department_id))
            hierarchy_departments = result.mappings().fetchall()
            return hierarchy_departments

    # ________________________________UPDATE_____________________________________________________
    @staticmethod
    @pydantic.validate_call
    def change_admin_activity_status(id_admin: int) -> None:
        with session_factory() as session:
            admin = session.query(Admins).filter_by(id=id_admin).first()
            if admin:
                admin.active = not admin.active
                session.commit()
            else:
                raise ValueError(f"Администратор с id {id_admin} не найден.")

    @staticmethod
    @pydantic.validate_call
    def edit_admin(id_admin: int, **kwargs) -> None:
        with session_factory() as session:
            admin = session.query(Admins).filter_by(id=id_admin).first()

            if not admin:
                raise ValueError(f"Администратор с id {id_admin} не найден.")

            # Обновить только переданные атрибуты
            for key, value in kwargs.items():
                if value is not None and value != "":
                    setattr(admin, key, value)
            session.commit()

    @staticmethod
    @pydantic.validate_call
    def update_all_departments(list_departments: list) -> None:
        with session_factory() as session:
            for row in list_departments:
                stmt = update(Departments).where(Departments.id == row['id']).values(
                    number_department=row['number_department'],
                    name_department=row['name_department'])
                session.execute(stmt)
            session.commit()

    @staticmethod
    @pydantic.validate_call
    def update_user_departments(list_replacement_departments: list) -> None:
        with session_factory() as session:
            for row in list_replacement_departments:
                stmt = update(Users).where(Users.id_department == row[1]).values(id_department=row[0])
                session.execute(stmt)
            session.commit()

    # ________________________________DELETE_____________________________________________________
    @staticmethod
    @pydantic.validate_call()
    def delete_departments(id_departments_for_delete: list) -> None:
        with session_factory() as session:
            condition = Departments.id.in_(id_departments_for_delete)
            delete_stmt = delete(Departments).where(condition)
            session.execute(delete_stmt)
            session.commit()
