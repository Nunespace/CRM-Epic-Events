from models import repository
from controllers.permissions import Permissions
from views.menu import Menu
from views.display import Display
from views.get_datas import GetDatas


class CrudManager:
    def __init__(self, staff_user, token):
        self.staff_user = staff_user
        self.token = token
        self.menu = Menu()
        self.display = Display()
        self.permissions = Permissions()
        self.get_datas = GetDatas()

    def create(self, table):
        if self.permissions.permission_create(self.token, table):
            datas = self.get_datas.get_create_datas(table)

            if table == "client":
                client_repository = repository.ClientRepository()
                try:
                    client_repository.create_client(datas, self.staff_user.id)
                    return "creation_ok"
                except:
                    return False

            elif table == "event":
                client_repository = repository.ClientRepository()
                fullname = self.get_datas.get_fullname()
                client = client_repository.find_by_fullname(fullname)
                if client is not None and self.permissions.is_own_client(self.staff_user.id, client.id):
                    event_repository = repository.EventRepository()
                    try:
                        event_repository.create_event(datas, client.id)
                        return "creation_ok"
                    except:
                        return "unknown_client"

            elif table == "contract":
                contract_repository = repository.ContractRepository()
                try:
                    contract_repository.create_contract(datas)
                    return "creation_ok"
                except:
                    return "unknown_client"

            elif table == "staff":
                staff_repository = repository.StaffRepository()
                try:
                    staff_repository.create_staff(datas)
                    return "creation_ok"
                except:
                    print("DATASSSSS: ", datas)
                    print("Except : Erreur ds crudmanager")
                    return "error"
        print("icccccciiii")
        return "not_allowed"

    def read(self, table):
        option = self.menu.view_menu_read_only(table)
        if self.permissions.check_token_validity(self.token):
            if table == "client":
                client_repository = repository.ClientRepository()

                if option == 1:
                    client = client_repository.get_all()
                    self.display.display_all_table(client)
                    return True

                if option == 2:
                    fullname = self.get_datas.get_fullname()
                    client = client_repository.find_by_fullname(fullname)
                    if client is not None:
                        self.display.display_one_object(client)
                        return True
                    return False

                if option == 3:
                    id = self.get_datas.get_id(table)
                    client = client_repository.find_by_id(id)
                    if client is not None:
                        self.display.display_one_object(client)
                        return True
                    return False

            elif table == "event":
                event_repository = repository.EventRepository()
                if option == 1:
                    event = event_repository.get_all()
                    self.display.display_all_table(event)
                    return True

                elif option == 2:
                    name_event = self.get_datas.get_name_event()
                    event = event_repository.find_by_name(name_event)
                    if event is not None:
                        self.display.display_one_object(event)
                        return True
                    return False
                elif option == 3:
                    id = self.get_datas.get_id(table)
                    event = event_repository.find_by_id(id)
                    if event is not None:
                        self.display.display_one_object(event)
                        return True
                    return False

                elif option == 4:
                    fullname_client = self.get_datas.get_fullname()
                    client_repository = repository.ClientRepository()
                    client = client_repository.find_by_fullname(fullname_client)
                    event = event_repository.find_by_client(client.id)
                    if event is not None:
                        self.display.display_one_object(event)
                        return True
                    return False

            elif table == "contract":
                contract_repository = repository.ContractRepository()
                if option == 1:
                    contract = contract_repository.get_all()
                    self.display.display_all_table(contract)
                    return True

                elif option == 2:
                    # Recherche d'un contrat avec le nom du client concerné
                    fullname_client = self.get_datas.get_fullname()
                    client_repository = repository.ClientRepository()
                    client = client_repository.find_by_fullname(fullname_client)
                    contract = contract_repository.find_by_client(client.id)
                    if contract is not None:
                        self.display.display_one_object(contract)
                        return True
                    return False

                elif option == 3:
                    id = self.get_datas.get_id(table)
                    contract = contract_repository.find_by_id(id)
                    if contract is not None:
                        self.display.display_one_object(contract)
                        return True
                    return False

                elif option == 4:
                    # Recherche d'un contrat avec le nom d'un évènement
                    name_event = self.get_datas.get_name_event()
                    event_repository = repository.EventRepository()
                    event = event_repository.find_by_name(name_event)
                    contract = contract_repository.find_by_event(event.id)
                    if contract is not None:
                        self.display.display_one_object(contract)
                        return True
                    return False

            elif table == "staff":
                staff_repository = repository.StaffRepository()
                if option == 1:
                    staff = staff_repository.get_all()
                    self.display.display_all_table(staff)
                    return True

                if option == 2:
                    id = self.get_datas.get_id(table)
                    staff_member = staff_repository.find_by_id(id)
                    if staff_member is not None:
                        self.display.display_one_object(staff_member)
                        return True
                    return False

                if option == 3:
                    name, first_name = self.get_datas.get_name_and_first_name_staff()
                    staff_member = staff_repository.find_by_name_and_firstname(name, first_name)
                    if staff_member is not None:
                        self.display.display_one_object(staff_member)
                        return True
                    return False

                if option == 4:
                    email = self.get_datas.get_email()
                    staff_member = staff_repository.find_by_email(email)
                    if staff_member is not None:
                        self.display.display_one_object(staff_member)
                        return True
                    return False

    def update(self, table):
        if table == "client":
            fullname = self.get_datas.get_fullname()
            client_repository = repository.ClientRepository()
            client = client_repository.find_by_fullname(fullname)
            if client is not None:
                if self.permissions.permission_update(self.staff_user.id, client.id, self.token, table):
                    column_to_update = self.menu.choice_column_to_update(table)
                    new_value = self.get_datas.get_new_value(column_to_update)
                    client_repository.update_client(client.id, column_to_update, new_value)
                    return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_client"

        elif table == "event":
            event_id = self.get_datas.get_id(table)
            event_repository = repository.EventRepository()
            event = event_repository.find_by_id(event_id)
            print("event : ", event)
            print("event_id = ", event_id)
            if event is not None:
                if self.permissions.permission_update(self.staff_user.id, event.id, self.token, table):
                    if self.staff_user.department.value == "support":
                        column_to_update = self.menu.choice_column_to_update(table)
                        print("column_to_update : ", column_to_update)
                        new_value = self.get_datas.get_new_value(column_to_update)
                        event_repository.update_event(event_id, column_to_update, new_value)
                        return "update_ok"
                    elif self.staff_user.department.value == "management":
                        # l'utilisateur management a le chois entre taper le nom du collaborateur ou son id
                        new_value = self.get_datas.get_support_contact()
                        # input = id (int)
                        try:
                            support_contact_id = int(new_value)
                            event_repository.update_event(event_id, support_contact_id, new_value)
                            return "update_ok"
                        # input = str
                        except ValueError:
                            staff_repository = repository.StaffRepository()
                            support_contact = staff_repository.find_by_name(new_value)
                            event_repository.update_event(event_id, "support_contact_id", support_contact.id)
                            return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_client"

        elif table == "contract":
            contract_id = self.get_datas.get_id(table)
            contract_repository = repository.ContractRepository()
            contract = contract_repository.find_by_id(contract_id)
            client_id = contract.client_id
            print("contract : ", contract)
            print("contract_id = ", contract_id)
            if contract is not None:
                if self.permissions.permission_update(self.staff_user.id, client_id, self.token, table):
                    column_to_update = self.menu.choice_column_to_update(table)
                    new_value = self.get_datas.get_new_value(column_to_update)
                    contract_repository.update_contract(contract.id, column_to_update, new_value)
                    return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_client"

        elif table == "staff":
            name, first_name = self.get_datas.get_name_and_first_name_staff()
            staff_repository = repository.StaffRepository()
            staff_member = staff_repository.find_by_name_and_firstname(name, first_name)
            if staff_member is not None:
                if self.permissions.permission_update(self.staff_user.id, staff_member.id, self.token, table):
                    column_to_update = self.menu.choice_column_to_update(table)
                    new_value = self.get_datas.get_new_value(column_to_update)
                    staff_repository.update_staff(staff_member.id, column_to_update, new_value)
                    return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_client"
