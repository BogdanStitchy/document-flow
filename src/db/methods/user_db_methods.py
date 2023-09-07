"""file with database access methods for user role"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import engine
from src.db.models.users_data import UsersData
from src.db.models.users_login import UsersLogin


class UserDB:
    @staticmethod
    def check_password(login: str) -> {}:
        with Session(engine) as session:
            with session.begin():
                result = session.execute(
                    select(
                        UsersData.id,
                        UsersData.last_name,
                        UsersData.name,
                        UsersData.patronymic,
                        UsersLogin.active,
                        UsersLogin.password,
                        UsersLogin.salt,
                        UsersLogin.date_last_changes_password
                    ).join_from(
                        UsersData, UsersLogin
                    ).where(UsersLogin.login == login))
            result = result.mappings().fetchone()
            return result
