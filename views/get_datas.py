import os
import platform
import getpass
import re
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich import print
from passlib.hash import argon2
from views.menu import Menu
from models.models import Department
from rich.console import Console

blue_console = Console(style="white on blue")
red_console = Console(style="white on blue")
# exemple : blue_console.print("I'm blue. Da ba dee da ba di.")


class GetDatas:
    def __init__(self):
        self.menu = Menu()
        self.console = Console()

    def get_credentials(self):
        print()
        self.console.print("Veuillez taper vos identifiants.", style="blue")
        email = Prompt.ask("🆔 Email")
        password = Prompt.ask("🔑 Mot de passe", password=True)
        return email, password

    def get_id(self, table):
        if table == "client":
            id = IntPrompt.ask("N° (id) du client")
        elif table == "event":
            id = IntPrompt.ask("N° (id) de l'évènement ")
        elif table == "contract":
            id = IntPrompt.ask("N° (id) du contrat")
        elif table == "staff":
            id = IntPrompt.ask("N° (id) du collaborateur")
        # id = self.chek_id(id_str)
        return id

    def get_fullname(self):
        blue_console.print("Veuillez taper le nom complet du client.")
        name = input("Nom : ").capitalize()
        firstname = input("Prénom : ").capitalize()
        fullname = firstname + " " + name
        return fullname

    def get_name_event(self):
        blue_console.print("Veuillez taper le nom de l'évènement.")
        name_event = input("Nom : ").capitalize()
        return name_event

    def get_name_and_first_name_staff(self):
        blue_console.print(
            "Veuillez taper le nom et le prénom du collaborateur."
        )
        name = input("Nom : ").capitalize()
        firstname = input("Prénom : ").capitalize()
        return name, firstname

    def get_email(self):
        email = input("Veuillez taper l'email : ")
        email = self.chek_email(email)
        return email

    def hash_password(self, password):
        hash = argon2.hash(f"{password}")
        return hash

    def get_password(self):
        password = getpass.getpass(prompt="Veuillez créer un mot de passe : ")
        while (
            re.fullmatch(
                r"^(?=.{8,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$",
                password,
            )
            is None
        ):
            print(
                "Le mot de passe doit être formé d'un minimum de 8 caractères, "
                "au moins une lettre majuscule, "
                "au moins une lettre minuscule, "
                "au moins un chiffre, "
                "au moins un caractère spécial."
            )
            password = getpass.getpass("Mot de passe : ")
        password_hashed = self.hash_password(password)
        return password_hashed

    def get_create_datas(self, table):
        if table == "client":
            blue_console.print("Veuillez taper les données suivantes.")
            fullname = self.get_fullname()
            email_input = input("Email : ")
            email = self.chek_email(email_input)
            phone_input = int(input("Téléphone : "))
            phone = self.check_phone(phone_input)
            name_company = input("Nom de l'entreprise : ")
            datas = {
                "fullname": fullname,
                "email": email,
                "phone": phone,
                "name_company": name_company,
            }
            return datas
        elif table == "event":
            blue_console.print("Veuillez taper les données suivantes.")
            name = input("Nom de l'évènement : ").capitalize()
            contract_id = input("numéro (id) du contrat : ")
            blue_console.print(
                "Indiquer la date et l'heure du début de l'évènement :"
            )
            event_date_start = self.get_datetime()
            blue_console.print(
                "Indiquer la date et l'heure de la fin de l'évènement :"
            )
            event_date_end = self.get_datetime()
            location = input("lieu : ")
            attendees = input("Nombre de personnes estimé : ")
            notes = input("Notes : ")
            datas = {
                "name": name,
                "contract_id": contract_id,
                "event_date_start": event_date_start,
                "event_date_end": event_date_end,
                "location": location,
                "attendees": attendees,
                "notes": notes,
            }
            return datas

        elif table == "contract":
            blue_console.print("Veuillez taper les données suivantes.")
            client_id = input("N° (id) du client : ")
            total_amount = input("Montant total : ")
            total_amount = self.chek_number(total_amount)
            balance_due = input("Montant restant à payer : ")
            balance_due = self.chek_number(balance_due)
            status_input = input(
                "Contrat signé? Taper 1 pour OUI, 2 pour NON : "
            )
            status = self.check_status(status_input)
            datas = {
                "client_id": client_id,
                "total_amount": total_amount,
                "balance_due": balance_due,
                "status": status,
            }
            return datas

        elif table == "staff":
            blue_console.print("Veuillez taper les données suivantes.")
            name, first_name = self.get_name_and_first_name_staff()
            email = self.get_email()
            password_hashed = self.get_password()
            department = self.get_department()
            datas = {
                "name": name.capitalize(),
                "first_name": first_name,
                "email": email,
                "password": password_hashed,
                "department": department,
            }
            return datas

    def get_datetime(self):
        year = input("année (ex : 2023) : ")
        month = input("mois (ex : 01): ")
        day = input("jour (ex : 04): ")
        hour = input("heure (ex : 14): ")
        date_time = f"{year}-{month}-{day} {hour}:00"
        return date_time

    def chek_email(self, email):
        while (
            re.fullmatch(r"[a-z0-9._-]+@[a-z0-9._-]+\.[a-z0-9._-]+", email)
            is None
        ):
            red_console.print(
                "Veuillez taper un email valide. Exemple : alice@gmail.com"
            )
            email = input("Email : ")
        return email

    """
    def chek_id(self, id):
        while re.fullmatch(r"[0-9]", id) is None:
            print("Veuillez taper un nombre entre 0 et 9")
            id = input("id : ")
        return int(id)
    """

    def chek_phone(self, phone):
        while re.fullmatch(r"[0-9]+", phone) is None:
            red_console.print(
                "Le n° de téléphone doit être composé uniquement de chiffres, sans espaces."
            )
            phone = input("N° de téléphone : ")
        return int(phone)

    def chek_number(self, number_input):
        while re.fullmatch(r"[0-9]+", number_input) is None:
            red_console.printrint(
                "Le montant doit être composé uniquement de chiffres, sans espaces."
            )
            number_input = input("Montant : ")
        return int(number_input)

    def check_status(self, status_input):
        while re.fullmatch(r"[1-2]", status_input) is None:
            print()
            status_input = input(
                "Contrat signé? Merci de taper 1 pour OUI ou 2 pour NON : "
            )
        if status_input == "1":
            return True
        elif status_input == "2":
            return False

    def get_new_value(self, column):
        new_value = input("Veuillez entrer la nouvelle valeur : ")
        if column == "email":
            email = self.chek_email(new_value)
            return email
        if column == "phone":
            phone = self.chek_phone(new_value)
            return phone
        else:
            return new_value

    def get_support_contact(self):
        support_contact = input(
            "Veuillez taper le nom ou l'id du collaborateur support de l'évènement : "
        )
        return support_contact.capitalize()

    def get_department(self):
        print("Liste des départements : ")
        for department in Department:
            print(f"{department.name} : {department.value}")
        department_number = input(
            "Veuillez entrer le n° du département choisi : "
        )
        department = Department(int(department_number))
        return department.name

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
