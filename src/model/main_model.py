from src.model.user import User
from src.model.administrator import Administrator
from src.model.super_admin import SuperAdmin


class Client:
    def __init__(self, access_lvl: str):
        self.client: SuperAdmin

        if access_lvl == 'admin':
            self.client = SuperAdmin()
            # print(self.client.get_lvl_access())
        elif access_lvl == 'user':
            self.client = User()
