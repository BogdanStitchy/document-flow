"""file with database access methods for user role"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import engine
from src.db.models.users import Users


class UserDB:
    @staticmethod
    def check_password(login: str) -> {}:
        with Session(engine) as session:
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
