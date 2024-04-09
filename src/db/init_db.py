import os
import sys

sys.path.append(os.getcwd())

from src.db.methods.super_admin_db_methods import SuperAdminMethodsDB
from src.model.utils.tools import create_hash_password
from src.config.config import NAME_DB


def create_super_admin():
    if SuperAdminMethodsDB.get_super_admin() is not None:
        print(f"Супер админ уже существует в базе!")
        return
    login = input("Введите логин: ")
    name = "super_admin"  # input("Введите имя: ")
    patronymic = "super_admin"  # input("Введите отчество: ")
    last_name = "super_admin"  # input("Введите фамилию: ")
    password = input("Введите пароль: ")
    salt = os.urandom(16)
    password = create_hash_password(password, salt)
    SuperAdminMethodsDB.add_admin(name, patronymic, last_name, login, password, salt, flag_super_admin=True)


def create_main_department():
    if len(SuperAdminMethodsDB.get_all_departments()) > 0:
        print("Главный отдел уже существует")
        return
    id_dep = SuperAdminMethodsDB.add_department("Главный отдел", 100)
    SuperAdminMethodsDB.add_one_hierarchy_department(id_dep, None)


def create_initial_data():
    answer = input(f"Вы уверены, что хотите создать супер админа в базе '{NAME_DB}' и добавить главный отдел?\n"
                   f"(Необходимо при первоначальной настройке приложения)\n(Y/N): ")
    if "y" not in answer.lower():
        return
    create_super_admin()
    create_main_department()


if __name__ == "__main__":
    create_initial_data()
