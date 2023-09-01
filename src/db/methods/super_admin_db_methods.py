"""file with database access methods for super admin role"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database_setup import engine
from src.db.models.admins_login import AdminsLogin
from src.db.models.admins_data import AdminsData
from src.db.methods.admin_db_methods import AdminDB


class SuperAdminDB(AdminDB):
    pass
