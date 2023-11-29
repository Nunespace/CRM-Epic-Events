import jwt
from settings import SECRET, SESSION
from views.messages import Messages
from models.models import Staff


class Permissions:
    def __init__(self):
        self.messages = Messages()

    def check_token_validity(self, token):
        try:
            return jwt.decode(token, SECRET, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            self.messages.message_error(message_number=2)
            return False

    def permission_create(self, token, table):
        if self.check_token_validity(token) is not False:
            token_decode = self.check_token_validity(token)
            department = token_decode["department"]
            if table == "client" or table == "event":
                if department == "COMMERCIAL":
                    return True
                else:
                    return False
            
            elif (table == "contract" or table == "staff") and department == "MANAGEMENT":
                print("table :", table, "department :", department)
                return True
            else:
                print("table :", table, "department :", department)
                print("1111111")
                return False
        else:
            return False

    def permission_update(self, staff_id, object_id, token, table):
        if self.check_token_validity(token):
            token_decode = self.check_token_validity(token)
            department = token_decode["department"]
            print("department : ", department)
            if table == "client":
                return department == "COMMERCIAL" and self.is_own_client(staff_id, object_id)
            elif table == "event" and department == "SUPPORT":
                return self.is_their_event(staff_id, event_id=object_id)
            elif (table == "event" or table == "contract" or table == "staff") and department == "MANAGEMENT":
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
