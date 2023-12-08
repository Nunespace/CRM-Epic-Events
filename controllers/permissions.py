import jwt
import time
from settings import SECRET, SESSION, ALGORITHME
from views.messages import Messages
from views.menu import Menu
from models.models import Staff


class Permissions:
    def __init__(self):
        self.messages = Messages()
        self.menu = Menu()

    def check_token_validity(self, token):
        """
        Vérifie si le token est toujours valide. Si la durée est expirée,
        l'application se ferme.
        """
        try:
            return jwt.decode(token, SECRET, algorithms=ALGORITHME)
        except jwt.ExpiredSignatureError:
            self.menu.clean()
            self.messages.message_error(table=None, message_number=2)
            print()
            time.sleep(3)
            SESSION.close()
            exit()


    def permission_create(self, token, table):
        if self.check_token_validity(token) is not False:
            token_decode = self.check_token_validity(token)
            department = token_decode["department"]
            if table == "client" or table == "event":
                if department == "COMMERCIAL":
                    return True
                else:
                    return False

            elif (
                table == "contract" or table == "staff"
            ) and department == "MANAGEMENT":
                return True
            else:
                return False
        else:
            return False

    def permission_update(self, staff_id, object_id, token, table):
        if self.check_token_validity(token):
            token_decode = self.check_token_validity(token)
            department = token_decode["department"]
            print("department : ", department)
            if table == "client":
                return department == "COMMERCIAL" and self.is_own_client(
                    staff_id, object_id
                )
            elif table == "event" and department == "SUPPORT":
                return self.is_their_event(staff_id, event_id=object_id)
            elif (
                table == "event" or table == "contract" or table == "staff"
            ) and department == "MANAGEMENT":
                return True
            elif (
                table == "contract"
                and department == "COMMERCIAL"
                and self.is_own_client(staff_id, client_id=object_id)
            ):
                return True
            else:
                return False
        else:
            return False

    def is_own_client(self, staff_id, client_id):
        staff = SESSION.get(Staff, staff_id)
        clients = staff.clients
        for client in clients:
            if client.id == client_id:
                return True
        return False

    def is_their_event(self, staff_id, event_id):
        staff = SESSION.get(Staff, staff_id)
        events = staff.events
        for event in events:
            if event.id == event_id:
                return True
        return False
