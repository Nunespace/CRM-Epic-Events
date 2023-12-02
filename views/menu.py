import os
import platform
import time
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

blue_console = Console(style="white on blue")

class Menu:
    def __init__(self):
        self.console = Console()

    def main_menu(self):
        """
        Affiche le menu principal
        retourne le choix de l'utilisateur
        """
        print()
        menu_options = {
            1: "Clients",
            2: "Evènements",
            3: "Contrats",
            4: "Collaborateurs: ",
            5: "Fermer",
        }
        self.console.rule("[bold blue]Menu principal")
        print()
        for key in menu_options:
            self.console.print(key, "--", menu_options[key], style="blue")
            print()

        option = IntPrompt.ask(
            "Entrer votre choix : ", choices=["1", "2", "3", "4", "5"]
        )
        self.clean()
        return option
    
    def table_name_translation(self, table):
        if table == "client":
            return "Clients"
        elif table == "contract":
            return "Contrats"
        elif table == "event":
            return "Evènements"
        elif table == "staff":
            return "Collaborateurs"

    def submenu(self, table):
        """
        Affiche le sous menu (client ou contrat ou évenènement ou
        collaborateur)
        retourne le choix de l'utilisateur
        """
        table_in_french = self.table_name_translation(table)
        print()
        self.console.rule(f"[bold blue]Menu {table_in_french}")
        print()
        if table != "staff":
            menu_options = {
                1: "Consulter",
                2: "Créer",
                3: "Modifier",
                4: "Retour au menu principal",
                5: "Fermer",
            }
        elif table == "staff":
            menu_options = {
                1: "Consulter",
                2: "Créer",
                3: "Modifier",
                4: "Supprimer un compte collaborateur",
                5: "Retour au menu principal",
                6: "Fermer",
            }

        for key in menu_options:
            self.console.print(key, "--", menu_options[key], style="blue")
            print()

        option = IntPrompt.ask(
            "Entrer votre choix : ", choices=["1", "2", "3", "4", "5"]
        )
        self.clean()
        return option

    def view_menu_read_only(self, table):
        """
        Affiche le sous menu (client ou contrat ou évenènement ou collaborateur)
        retourne le choix de l'utilisateur
        """
        while True:
            print()
            self.console.rule("[bold blue]Consulter")
            print()
            if table == "client":
                menu_options = {
                    1: "Afficher tous les clients",
                    2: "Trouver un client par son nom",
                    3: "Trouver un client par son numéro (id)",
                    4: "Retour au menu principal",
                    5: "Fermer",
                }
            elif table == "event":
                menu_options = {
                    1: "Afficher tous les évènements",
                    2: "Trouver un évènement par son nom",
                    3: "Trouver un évènement par son numéro (id)",
                    4: "Afficher tous les évènements d'un client",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }
            elif table == "contract":
                menu_options = {
                    1: "Afficher tous les contrats",
                    2: "Trouver un contrat avec le n° (id) du client",
                    3: "Trouver un contrat par son numéro (id)",
                    4: "Trouver un contrat avec le nom de l'évènement",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }
            elif table == "staff":
                menu_options = {
                    1: "Afficher tous les collaborateurs",
                    2: "Trouver un colloaborateur avec son n° (id)",
                    3: "Trouver un collaborateur avec son nom et prénom",
                    4: "Trouver un collaborateur avec son email",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }
            for key in menu_options:
                self.console.print(key, "--", menu_options[key], style="blue")
                print()

            if table == "client":
                option = IntPrompt.ask(
                    "Entrer votre choix : ", choices=["1", "2", "3", "4", "5"]
                )
            else:
                option = IntPrompt.ask(
                    "Entrer votre choix : ", choices=["1", "2", "3", "4", "5", "6"]
                )

            self.clean()
            return option

    def choice_column_to_update(self, table):
        while True:
            print()
            if table == "client":
                self.console.rule("[bold blue]Modifier un compte client")
                list_of_editable_update_columns = {
                    1: "fullname",
                    2: "email",
                    3: "phone",
                    4: "name_company",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }

            elif table == "event":
                self.console.rule("[bold blue]Modifier un èvènement")
                list_of_editable_update_columns = {
                    1: "name",
                    2: "contract_id",
                    3: "client_id",
                    4: "support_contact_id",
                    5: "event_date_start",
                    6: "event_date_end",
                    7: "location",
                    8: "attendees",
                    9: "notes",
                    10: "Retour au menu principal",
                    11: "Fermer",
                }

            elif table == "contract":
                self.console.rule("[bold blue]Modifier un contrat")
                list_of_editable_update_columns = {
                    1: "client_id",
                    2: "total_amount",
                    3: "balance_due",
                    4: "status",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }

            elif table == "staff":
                self.console.rule("[bold blue]Modifier un collaborateur")
                list_of_editable_update_columns = {
                    1: "name",
                    2: "first_name",
                    3: "email",
                    4: "password",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }
            blue_console.print("Liste des champs modifiables : ")
            for key in list_of_editable_update_columns:
                self.console.print(
                    key, list_of_editable_update_columns[key], style="blue"
                )
                print()
            if table == "event":
                number_column_to_update = IntPrompt.ask(
                    "Entrer votre choix : ",
                    choices=[
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                        "11",
                    ],
                )
            else:
                number_column_to_update = IntPrompt.ask(
                    "Entrer votre choix : ",
                    choices=["1", "2", "3", "4", "5", "6"],
                )

            self.clean()
            return list_of_editable_update_columns[number_column_to_update]

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
