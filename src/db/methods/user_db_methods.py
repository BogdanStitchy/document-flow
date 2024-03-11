"""file with database access methods for user role"""

import pydantic
import datetime
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from src.db.database_setup import get_engine
from src.db.models import DataAboutDocuments, FilesDocuments, DepartmentsHierarchy
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
                        Users.date_last_changes_password
                    ).where(Users.login == login))
            result = result.mappings().fetchone()
            return result

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
                        and_(or_(DepartmentsHierarchy.parent_id == id_current_department,
                                 DepartmentsHierarchy.department_id == id_current_department, )
                             (or_(DataAboutDocuments.inner_number.ilike(f"%{search_string}%"),
                                  DataAboutDocuments.output_number.ilike(f"%{search_string}%"),
                                  DataAboutDocuments.type_document.ilike(f"%{search_string}%"),
                                  DataAboutDocuments.name.ilike(f"%{search_string}%"),
                                  Users.last_name.ilike(f"%{search_string}%"),
                                  Users.name.ilike(f"%{search_string}%"))
                              )
                             )
                    ).join_from(DataAboutDocuments, Users, DepartmentsHierarchy)
                )
                documents = result.mappings().fetchall()
                return documents

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
                    id_creator=id_user
                )
                session.add(document_data)
                session.flush()  # Получаем автоматически сгенерированный ID
                file_data = FilesDocuments(
                    id=document_data.id,
                    file=file
                )
                session.add(file_data)
                session.commit()
