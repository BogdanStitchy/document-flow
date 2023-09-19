"""file with database access methods for user role"""
import pydantic
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import get_engine
from src.db.models import DataAboutDocuments, FilesDocuments
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
