from passlib.hash import argon2
from settings import SECRET, SESSION
import jwt
from datetime import datetime, timedelta, timezone
from controllers.menu_manager import MenuManager
from views.menu import Menu
from views.get_datas import GetDatas
from views.messages import Messages
from models.models import Staff


class AuthenticationAndPermissions:
    def __init__(self):
        self.menu = Menu()
        self.messages = Messages()
        self.get_datas = GetDatas()

    def create_token(self, department):
        encoded_jwt = jwt.encode(
            {"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=60), "department": department}, SECRET, algorithm="HS256"
        )
        return encoded_jwt
    
    def staff_user(self, email):
        return SESSION.query(Staff).filter(Staff.email == email).one_or_none()

    def check_password(self):
        get_datas = GetDatas()
        email, password = get_datas.get_credentials()
        staff_user = self.staff_user(email)
        if staff_user is not None:
            password_user_hashed = staff_user.password
            if argon2.verify(password, password_user_hashed):
                department = staff_user.department.name
                token = self.create_token(department)
                menu_manager = MenuManager(staff_user, token)
                print("token :", token)
                return menu_manager.choice_main_menu()
        self.messages.message_error(None, 1)
        return self.check_password()
