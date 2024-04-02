"""file with database access methods for user role"""

import pydantic
import datetime
from sqlalchemy import select, and_, or_, update

from src.db.database_setup import session_factory
from src.db.models import DataAboutDocuments, FilesDocuments, DepartmentsHierarchy, Departments
from src.db.models.users import Users

_necessary_fields_for_documents = (DataAboutDocuments.inner_number,
                                   DataAboutDocuments.output_number,
                                   DataAboutDocuments.output_date,
                                   DataAboutDocuments.type_document,
                                   DataAboutDocuments.name,
                                   DataAboutDocuments.date_creating,
                                   DataAboutDocuments.id,
                                   DataAboutDocuments.note,
                                   (Users.last_name + ' ' + Users.name).label('creator'))


class UserDB:
    # _________________________________GET_______________________________________________________
    @staticmethod
    def check_password(login: str) -> {}:
        with session_factory() as session:
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
        with session_factory() as session:
            execute_id_available_departments = (select(DepartmentsHierarchy.department_id).where(
                DepartmentsHierarchy.parent_id == id_current_department))
            id_available_departments = session.execute(execute_id_available_departments).scalars().all()
            id_available_departments.append(id_current_department)  # list
            access_condition = Users.id_department.in_(id_available_departments)
            stmt = (
                select(
                    *_necessary_fields_for_documents
                ).join(Users).where(access_condition)
            )
            result = session.execute(stmt)
            documents = result.mappings().fetchall()
            return documents

    @staticmethod
    @pydantic.validate_call
    def find_document_period(id_current_department: int, flag_date_output: bool, flag_date_download: bool,
                             start_output_date: datetime.date, end_output_date: datetime.date,
                             start_create_date: datetime.date, end_create_date: datetime.date) -> [{}, {}]:
        def get_query_with_conditions():
            if flag_date_download and flag_date_output:
                query_with_conditions = basic_query_without_conditions.where(
                    and_(access_condition, DataAboutDocuments.date_creating.between(start_create_date, end_create_date),
                         DataAboutDocuments.output_date.between(start_output_date, end_output_date)))

            elif flag_date_download:
                query_with_conditions = basic_query_without_conditions.where(
                    access_condition, DataAboutDocuments.date_creating.between(start_create_date, end_create_date)
                )

            elif flag_date_output:
                query_with_conditions = basic_query_without_conditions.where(
                    access_condition, DataAboutDocuments.output_date.between(start_output_date, end_output_date)
                )

            elif not flag_date_output and not flag_date_download:
                raise ValueError("Ошибка задания периода, необходимо выбрать по каким полям задавать периоды")

            return query_with_conditions

        with session_factory() as session:
            execute_id_available_departments = (select(DepartmentsHierarchy.department_id).where(
                DepartmentsHierarchy.parent_id == id_current_department))
            id_available_departments = session.execute(execute_id_available_departments).scalars().all()
            id_available_departments.append(id_current_department)  # list
            access_condition = Users.id_department.in_(id_available_departments)

            basic_query_without_conditions = select(
                *_necessary_fields_for_documents
            ).join(Users)

            result = session.execute(get_query_with_conditions())
            documents = result.mappings().fetchall()
            return documents

    @staticmethod
    @pydantic.validate_call
    def find_document_word(id_current_department: int, search_string: str):
        with session_factory() as session:
            execute_id_available_departments = (select(DepartmentsHierarchy.department_id).where(
                DepartmentsHierarchy.parent_id == id_current_department))
            id_available_departments = session.execute(execute_id_available_departments).scalars().all()
            id_available_departments.append(id_current_department)  # list
            access_condition = Users.id_department.in_(id_available_departments)

            result = session.execute(
                select(
                    *_necessary_fields_for_documents
                ).where(
                    and_(access_condition, (or_(DataAboutDocuments.inner_number.ilike(f"%{search_string}%"),
                                                DataAboutDocuments.output_number.ilike(f"%{search_string}%"),
                                                DataAboutDocuments.type_document.ilike(f"%{search_string}%"),
                                                DataAboutDocuments.note.ilike(f"%{search_string}%"),
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
        with session_factory() as session:
            result = session.execute(select(FilesDocuments.file).where(FilesDocuments.id == id_document))
            file = result.mappings().fetchone()
            return file

    # _________________________________ADD______________________________________________________
    @staticmethod
    @pydantic.validate_call
    def add_document(id_user: int, file: bytes, name_document: str, inner_number: str, output_number: str,
                     output_date, type_document: str, note: str) -> None:
        with session_factory() as session:
            document_data = DataAboutDocuments(
                inner_number=inner_number,
                output_number=output_number,
                output_date=output_date,
                type_document=type_document,
                name=name_document,
                id_creator=id_user,
                date_creating=datetime.datetime.now().date(),
                note=note
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
        with session_factory() as session:
            session.execute(
                update(Users).where(Users.id == id_user).values(
                    salt=salt,
                    password=password,
                    date_last_changes_password=date_change))
            session.commit()
