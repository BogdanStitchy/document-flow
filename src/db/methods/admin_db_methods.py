"""file with database access methods for admin role"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import engine
from src.db.models.admins_login import AdminsLogin
from src.db.models.admins_data import AdminsData


class AdminDB:
    @staticmethod
    def check_password(login: str) -> {}:
        with Session(engine) as session:
            with session.begin():
                result = session.execute(
                    select(
                        AdminsData.id,
                        AdminsData.last_name,
                        AdminsData.name,
                        AdminsData.patronymic,
                        AdminsLogin.active,
                        AdminsLogin.password,
                        AdminsLogin.salt,
                        AdminsLogin.super_admin_flag,
                        AdminsLogin.date_last_changes_password
                    ).
                        join_from(AdminsData, AdminsLogin).
                        where(AdminsLogin.login == login))
            result = result.mappings().fetchone()
            return result
