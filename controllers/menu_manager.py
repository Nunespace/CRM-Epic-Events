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
            return_of_order = self.crud.read(table)
            if (
                return_of_order == "display_ok"
                or return_of_order == "back"
            ):
                return self.choice_submenu(table)
            elif return_of_order == "close":
                SESSION.close()
                exit()

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

        elif option == 4 and table != "staff":
            return self.choice_main_menu()

        elif option == 4 and table == "staff":
            return_of_order = self.crud.delete(table)
            if return_of_order == "delete_ok":
                self.messages_ok(table, 3)
                return self.choice_main_menu()
            elif return_of_order == "canceled":
                return self.choice_main_menu()

            elif return_of_order == "not_allowed":
                self.messages.message_error(table, 5)
                return self.choice_main_menu()
            else:
                self.messages.message_error(table, 3)
                return self.choice_main_menu()

        elif option == 5 and table != "staff":
            SESSION.close()
            exit()

        elif option == 5 and table == "staff":
            return self.choice_main_menu()

        elif option == 6 and table == "staff":
            SESSION.close()
            exit()
