"""file with database access methods for super admin role"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import engine
from src.db.models.admins_login import AdminsLogin
from src.db.models.admins_data import AdminsData
from src.db.methods.admin_db_methods import AdminDB


class SuperAdminDB(AdminDB):
    def add_admin(self, name: str, patronymic: str, last_name: str, login: str, password: bytes, salt: bytes,
                  date_creating):
        with Session(engine) as session:
            with session.begin():
                # Создаем объекты для двух таблиц
                admins_data = AdminsData(name=name, last_name=last_name, patronymic=patronymic,
                                         date_creating=date_creating)
                admins_login = AdminsLogin(active=True, login=login, password=password, salt=salt)

                # Добавляем объекты в сессию
                session.add(admins_data)
                session.add(admins_login)

                # Фиксируем изменения в базе данных с помощью транзакции
                session.commit()
