"""file with database access methods for admin role"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import engine
from src.db.models.admins import Admins


class AdminDB:
    @staticmethod
    def check_password(login: str) -> {}:
        with Session(engine) as session:
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
