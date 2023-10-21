"""file with database access methods for admin role"""
import pydantic
from sqlalchemy import select, or_, update
from sqlalchemy.orm import Session

from src.db.database_setup import get_engine
from src.db.models.admins import Admins
from src.db.models.users import Users
from src.db.models.departments import Departments
from src.db.models.data_about_documents import DataAboutDocuments


class AdminMethodsDB:
    # _________________________________ADD______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def add_user(last_name: str, name: str, patronymic: str, login: str, password: bytes, salt: bytes,
                 id_department: int, id_creator: int) -> int:
        with Session(get_engine()) as session:
            with session.begin():
                new_user = Users(name=name, last_name=last_name, patronymic=patronymic, login=login,
                                 password=password, salt=salt, creator_id=id_creator, id_department=id_department)

                session.add(new_user)
                session.commit()
            return new_user.id

    # _________________________________GET_______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def check_password(login: str) -> {}:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(
                        Admins.id,
                        Admins.last_name,
                        Admins.name,
                        Admins.patronymic,
                        Admins.active,
                        Admins.password,
                        Admins.salt,
                        Admins.super_admin_flag,
                        Admins.date_last_changes_password
                    ).where(Admins.login == login))
            result = result.mappings().fetchone()
            return result

    @staticmethod
    @pydantic.validate_call
    def get_last_change_password_admin(id_admin: int):
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(Admins.date_last_changes_password).where(Admins.id == id_admin)
                )
            result = result.fetchone()
            return result[0]

    @staticmethod
    @pydantic.validate_call
    def get_all_users() -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(select(
                    Users.id,
                    Users.login,
                    Users.name,
                    Users.last_name,
                    Users.patronymic,
                    Users.active,
                    Users.password,
                    Users.salt,
                    Users.date_last_changes_password,
                    Users.date_creating,
                    Departments.number_department,
                    (Admins.last_name + ' ' + Admins.name).label("creator")
                ).join_from(Users, Departments).join_from(Users, Admins)
                                         )
                users = result.mappings().fetchall()
                return users

    @staticmethod
    @pydantic.validate_call
    def find_users(search_string: str) -> [{}, {}]:
        def try_convert_to_int(string: str):
            try:
                return int(string)
            except ValueError:
                return -99999

        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(select(
                    Users.id,
                    Users.login,
                    Users.name,
                    Users.last_name,
                    Users.patronymic,
                    Users.active,
                    Users.password,
                    Users.salt,
                    Users.date_last_changes_password,
                    Users.date_creating,
                    Departments.number_department,
                    (Admins.last_name + ' ' + Admins.name).label("creator")
                ).where(
                    or_(Users.login.ilike(f"%{search_string}%"),
                        Users.name.ilike(f"%{search_string}%"),
                        Users.last_name.ilike(f"%{search_string}%"),
                        Users.patronymic.ilike(f"%{search_string}%"),
                        Departments.number_department == try_convert_to_int(search_string),
                        Admins.last_name.ilike(f"%{search_string}%"),
                        Admins.name.ilike(f"%{search_string}%"))
                ).join_from(
                    Users, Departments).join_from(Users, Admins)
                                         )
                users = result.mappings().fetchall()
                return users

    @staticmethod
    @pydantic.validate_call
    def get_one_user(id_user: int) -> {}:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(Users.__table__).where(Users.__table__.c.id == id_user))
                user = result.mappings().fetchone()
                return user

    @staticmethod
    @pydantic.validate_call
    def get_all_documents() -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(select(
                    DataAboutDocuments.inner_number,
                    DataAboutDocuments.output_number,
                    DataAboutDocuments.output_date,
                    DataAboutDocuments.type_document,
                    DataAboutDocuments.name,
                    DataAboutDocuments.date_creating,
                    DataAboutDocuments.id,
                    (Users.last_name + ' ' + Users.name).label('creator')
                ).join_from(DataAboutDocuments, Users)
                                         )
                documents = result.mappings().fetchall()
                return documents

    @staticmethod
    @pydantic.validate_call
    def find_documents(search_string: str) -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(
                        DataAboutDocuments.inner_number,
                        DataAboutDocuments.output_number,
                        DataAboutDocuments.output_date,
                        DataAboutDocuments.type_document,
                        DataAboutDocuments.name,
                        DataAboutDocuments.date_creating,
                        DataAboutDocuments.id,
                        (Users.last_name + ' ' + Users.name).label('creator')
                    ).where(
                        or_(DataAboutDocuments.inner_number.ilike(f"%{search_string}%"),
                            DataAboutDocuments.output_number.ilike(f"%{search_string}%"),
                            DataAboutDocuments.type_document.ilike(f"%{search_string}%"),
                            DataAboutDocuments.name.ilike(f"%{search_string}%"),
                            Users.last_name.ilike(f"%{search_string}%"),
                            Users.name.ilike(f"%{search_string}%"))
                    ).join_from(DataAboutDocuments, Users)
                )
                documents = result.mappings().fetchall()
                return documents

    # ________________________________UPDATE_____________________________________________________
    @staticmethod
    @pydantic.validate_call
    def change_password(id_admin: int, password: bytes, salt: bytes, date_change):
        with Session(get_engine()) as session:
            with session.begin():
                session.execute(
                    update(Admins).where(Admins.id == id_admin).values(
                        salt=salt,
                        password=password,
                        date_last_changes_password=date_change
                    )
                )

    @staticmethod
    @pydantic.validate_call
    def update_user(id_user: int, **kwargs) -> None:
        # Найти запись по user_id
        with Session(get_engine()) as session:
            with session.begin():
                user = session.query(Users).filter_by(id=id_user).first()
                if user:
                    # Обновить только переданные атрибуты
                    for key, value in kwargs.items():
                        if value is not None and value != "":
                            setattr(user, key, value)
                    session.commit()
                else:
                    raise ValueError(f"Пользователь с id {id_user} не найден.")

    @staticmethod
    @pydantic.validate_call
    def update_document(id_document: int, **kwargs) -> None:
        # Найти запись по id_document
        with Session(get_engine()) as session:
            with session.begin():
                document = session.query(DataAboutDocuments).filter_by(id=id_document).first()
                if document:
                    # Обновить только переданные атрибуты
                    for key, value in kwargs.items():
                        if value is not None and value != "":
                            setattr(document, key, value)
                    session.commit()
                else:
                    raise ValueError(f"Документ с id {id_document} не найден.")

    @staticmethod
    @pydantic.validate_call
    def change_user_activity_status(id_user: int):
        with Session(get_engine()) as session:
            with session.begin():
                user = session.query(Users).filter_by(id=id_user).first()
                if user:
                    user.active = not user.active
                    session.commit()
                else:
                    raise ValueError(f"Пользователь с id {id_user} не найден.")
