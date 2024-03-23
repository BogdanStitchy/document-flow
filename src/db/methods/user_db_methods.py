"""file with database access methods for user role"""
import os
from typing import Optional

import pydantic
import datetime
from sqlalchemy import select, and_, or_, update
from sqlalchemy.orm import Session

from src.db.database_setup import get_engine
from src.db.models import DataAboutDocuments, FilesDocuments, DepartmentsHierarchy, Departments
from src.db.models.users import Users


class UserDB:
    # _________________________________GET_______________________________________________________
    @staticmethod
    def check_password(login: str) -> {}:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(
                        Users.id,
                        Users.last_name,
                        Users.name,
                        Users.patronymic,
                        Users.active,
                        Users.password,
                        Users.salt,
                        Users.date_last_changes_password,
                        Users.id_department,
                        Departments.number_department
                    ).join(Departments).where(Users.login == login))
            result = result.mappings().fetchone()
            return result

    @staticmethod
    @pydantic.validate_call
    def get_data_about_documents(id_current_department: int):
        with Session(get_engine()) as session:
            execute_id_available_departments = (select(DepartmentsHierarchy.department_id).where(
                DepartmentsHierarchy.parent_id == id_current_department))
            id_available_departments = session.execute(execute_id_available_departments).scalars().all()
            id_available_departments.append(id_current_department)  # list
            access_condition = Users.id_department.in_(id_available_departments)
            stmt = (
                select(
                    DataAboutDocuments.inner_number,
                    DataAboutDocuments.output_number,
                    DataAboutDocuments.output_date,
                    DataAboutDocuments.type_document,
                    DataAboutDocuments.name,
                    DataAboutDocuments.date_creating,
                    DataAboutDocuments.id,
                    (Users.last_name + ' ' + Users.name).label('creator')
                ).join(Users).where(access_condition)
            )
            result = session.execute(stmt)
            documents = result.mappings().fetchall()
            return documents

    @staticmethod
    @pydantic.validate_call
    def find_document_period(start_output_date: datetime.date, end_output_date: datetime.date,
                             start_create_date: datetime.date, end_create_date: datetime.date) -> [{}, {}]:
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(
                    select(DataAboutDocuments.__table__).where(and_(
                        DataAboutDocuments.date_creating.between(start_create_date, end_create_date),
                        DataAboutDocuments.output_date.between(start_output_date, end_output_date)
                    ))
                )
                admins = result.mappings().fetchall()
                return admins

    @staticmethod
    @pydantic.validate_call
    def find_document_word(id_current_department: int, search_string: str):
        with Session(get_engine()) as session:
            with session.begin():
                execute_id_available_departments = (select(DepartmentsHierarchy.department_id).where(
                    DepartmentsHierarchy.parent_id == id_current_department))
                id_available_departments = session.execute(execute_id_available_departments).scalars().all()
                id_available_departments.append(id_current_department)  # list
                access_condition = Users.id_department.in_(id_available_departments)

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
                        and_(access_condition, (or_(DataAboutDocuments.inner_number.ilike(f"%{search_string}%"),
                                                    DataAboutDocuments.output_number.ilike(f"%{search_string}%"),
                                                    DataAboutDocuments.type_document.ilike(f"%{search_string}%"),
                                                    DataAboutDocuments.name.ilike(f"%{search_string}%"),
                                                    Users.last_name.ilike(f"%{search_string}%"),
                                                    Users.name.ilike(f"%{search_string}%"))
                                                )
                             )
                    ).join(Users, DataAboutDocuments.id_creator == Users.id)
                )
                documents = result.mappings().fetchall()
                return documents

    @staticmethod
    @pydantic.validate_call
    def get_file(id_document: int):
        with Session(get_engine()) as session:
            with session.begin():
                result = session.execute(select(FilesDocuments.file).where(FilesDocuments.id == id_document))
                file = result.mappings().fetchone()
                return file

    # _________________________________ADD______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def add_document(id_user: int, file: bytes, name_document: str, inner_number: str, output_number: str,
                     output_date, type_document: str) -> None:
        with Session(get_engine()) as session:
            with session.begin():
                document_data = DataAboutDocuments(
                    inner_number=inner_number,
                    output_number=output_number,
                    output_date=output_date,
                    type_document=type_document,
                    name=name_document,
                    id_creator=id_user,
                    date_creating=datetime.datetime.now()
                )
                session.add(document_data)
                session.flush()  # Получаем автоматически сгенерированный ID
                file_data = FilesDocuments(
                    id=document_data.id,
                    file=file
                )
                session.add(file_data)
                session.commit()

    # ________________________________UPDATE_____________________________________________________
    @staticmethod
    @pydantic.validate_call
    def changes_password(id_user: int, password: bytes, salt: bytes, date_change) -> None:
        with Session(get_engine()) as session:
            with session.begin():
                session.execute(
                    update(Users).where(Users.id == id_user).values(
                        salt=salt,
                        password=password,
                        date_last_changes_password=date_change))
                session.commit()
