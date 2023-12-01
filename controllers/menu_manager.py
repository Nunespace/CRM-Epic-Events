from views.menu import Menu
from views.get_datas import GetDatas
from views.messages import Messages
from views.display import Display
from settings import SESSION
from controllers.permissions import Permissions
from controllers.crud_manager import CrudManager


class MenuManager:
    def __init__(self, staff_user, token):
        self.token = token
        self.menu = Menu()
        self.messages = Messages()
        self.display = Display()
        self.get_datas = GetDatas()
        self.permissions = Permissions()
        self.crud = CrudManager(staff_user, token)
        self.staff_id = staff_user

    def choice_main_menu(self):
        """
        Activation des méthodes selon le choix de l'utilisateur
        au menu principal
        """
        option = self.menu.main_menu()
        if option == 1:
            self.choice_submenu("client")
        elif option == 2:
            self.choice_submenu("event")
        elif option == 3:
            self.choice_submenu("contract")
        elif option == 4:
            self.choice_submenu("staff")
        elif option == 5:
            SESSION.close()
            exit()

    def choice_submenu(self, table):
        option = self.menu.submenu(table)
        # Option 1 = Consulter. Dans ce cas, seul la validité du token est vérifiée
        # car tous les collaborateurs authentifiés sont autorisées à lire les données

        if option == 1:
            if self.crud.read(table):
                return self.choice_main_menu()
            else:
                self.messages.message_error(table, 3)
                return self.choice_main_menu()

        elif option == 2 or option == 3:
            if option == 2:
                return_of_order = self.crud.create(table)
            elif option == 3:
                return_of_order = self.crud.update(table)

            if return_of_order == "creation_ok":
                self.messages.messages_ok(table, 1)
                return self.choice_main_menu()
            elif return_of_order == "update_ok":
                self.messages.messages_ok(table, 2)
                return self.choice_main_menu()
            elif return_of_order == "error":
                self.messages.message_error(table, 3)
                return self.choice_main_menu()
            elif return_of_order == "unknown_client":
                self.messages.message_error(table, 4)
                return self.choice_main_menu()
            elif return_of_order == "not_allowed":
                self.messages.message_error(table, 5)
                return self.choice_main_menu()

        elif option == 4:
            #from rich.prompt import Confirm
            #if Confirm.ask("Continue"):
            pass
        else:
            self.messages.message_error(3)
            return self.choice_main_menu()
