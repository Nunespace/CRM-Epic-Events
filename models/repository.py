from sqlalchemy import text
from settings import SESSION, ENGINE
from .models import Client, Event, Contract, Staff


class ClientRepository:
    def find_by_fullname(self, fullname):
        return SESSION.query(Client).filter(Client.fullname == fullname).first()

    def find_by_id(self, id):
        return SESSION.query(Client).filter(Client.id == id).first()

    def find_by_email(self, email):
        return SESSION.query(Client).filter_by(email=email).all()

    def get_all(self):
        with ENGINE.connect() as conn:
            result = conn.execute(text("SELECT * FROM client"))
        return result

    def create_client(self, datas, staff_id):
        client = Client(
            fullname=datas["fullname"],
            email=datas["email"],
            phone=datas["phone"],
            name_company=datas["name_company"],
            commercial_contact_id=staff_id,
        )
        # session.merge(client)
        SESSION.add(client)
        SESSION.commit()

    def update_client(self, client_id, column, new_value):
        client = SESSION.query(Client).filter_by(id=client_id).first()
        if column == "fullname":
            client.fullname = new_value
        if column == "email":
            client.email = new_value
        if column == "phone":
            client.phone = new_value
        if column == "name_company":
            client.name_company = new_value
        SESSION.commit()


class EventRepository:
    def find_by_name(self, name):
        return SESSION.query(Event).filter(Event.name == name).first()

    def find_by_id(self, id):
        return SESSION.query(Event).filter(Event.id == id).first()

    def find_by_client(self, client_id):
        return SESSION.query(Event).filter_by(client_id=client_id).all()

    def get_all(self):
        return SESSION.query(Event).all()

    def create_event(self, datas, client_id):
        event = Event(
            name=datas["name"],
            contract_id=datas["contract_id"],
            client_id=client_id,
            event_date_start=datas["event_date_start"],
            event_date_end=datas["event_date_end"],
            location=datas["location"],
            attendees=datas["attendees"],
            notes=datas["notes"],
        )
        SESSION.add(event)
        SESSION.commit()

    def update_event(self, event_id, column, new_value):
        event = SESSION.query(Event).filter_by(id=event_id).first()
        if column == "name":
            event.name = new_value
        elif column == "contract_id":
            event.contract_id = new_value
        elif column == "client_id":
            event.client_id = new_value
        elif column == "support_contact_id":
            event.support_contact_id = new_value
        elif column == "event_date_start":
            event.event_date_start = new_value
        elif column == "event_date_end":
            event.event_date_end = new_value
        elif column == "location":
            event.location = new_value
        elif column == "attendees":
            event.attendees = new_value
        elif column == "notes":
            event.notes = new_value

        SESSION.commit()


class ContractRepository:
    def find_by_id(self, id):
        return SESSION.query(Contract).filter(Contract.id == id).first()

    def find_by_client(self, client_id):
        return SESSION.query(Contract).filter_by(client_id=client_id).all()

    def find_by_event(self, event_id):
        return SESSION.query(Contract).filter_by(event_id=event_id).all()

    def get_all(self):
        return SESSION.query(Contract).all()

    def create_contract(self, datas):
        client = ClientRepository().find_by_id(datas["client_id"])
        commercial_contact_id = client.commercial_contact_id
        contract = Contract(
            client_id=datas["client_id"],
            commercial_contact_id=commercial_contact_id,
            total_amount=datas["total_amount"],
            balance_due=datas["balance_due"],
            status=datas["status"],
        )
        SESSION.add(contract)
        SESSION.commit()

    def update_contract(self, contract_id, column, new_value):
        contract = SESSION.query(Contract).filter_by(id=contract_id).first()
        if column == "client_id":
            client = ClientRepository().find_by_id(int(new_value))
            contract.client_id = new_value
            contract.commercial_contact_id = client.commercial_contact_id
        elif column == "total_amount":
            contract.total_amount = new_value
        elif column == "balance_due":
            contract.balance_due = new_value
        elif column == "status":
            contract.status = new_value
        SESSION.commit()


class StaffRepository:
    def get_all(self):
        return SESSION.query(Staff).all()

    def find_by_id(self, id):
        return SESSION.query(Staff).filter(Staff.id == id).first()

    def find_by_name_and_firstname(self, name, first_name):
        return SESSION.query(Staff).filter((Staff.name == name) & (Staff.first_name == first_name)).one_or_none()

    def find_by_email(self, email):
        return SESSION.query(Staff).filter_by(email=email).all()

    def create_staff(self, datas):
        staff = Staff(
            name=datas["name"],
            first_name=datas["first_name"],
            email=datas["email"],
            password=datas["password"],
            department=datas["department"],
        )
        SESSION.add(staff)
        SESSION.commit()

    def update_staff(self, staff_id, column, new_value):
        staff_member = SESSION.query(Staff).filter_by(id=staff_id).first()
        if column == "name":
            staff_member.name = new_value
        elif column == "first_name":
            staff_member.first_name = new_value
        elif column == "email":
            staff_member.email = new_value
        elif column == "department":
            staff_member.department == new_value
        SESSION.commit()

    def delete_staff(self, staff):
        SESSION.delete(staff)
        SESSION.commit()
