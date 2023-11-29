import os
import platform
import time


class Menu:
    def main_menu(self):
        """
        Affiche le menu principal
        retourne le choix de l'utilisateur
        """

        print()
        while True:
            menu_options = {1: "Clients", 2: "Evènements", 3: "Contrats", 4: "collaborateurs: ", 5: "Fermer"}
            print("****Menu principal****")
            print()
            for key in menu_options:
                print(key, "--", menu_options[key])
                print()
            try:
                option = int(input("Entrer votre choix : "))
            except ValueError:
                print("Vous devez taper un nombre entre 1 et 5.")
                time.sleep(2)
                self.clean()
                print()
            else:
                if option < 1 or option > 5:
                    print("Vous devez taper un nombre entre 1 et 5.")
                    time.sleep(2)
                    self.clean()
                    print()
                else:
                    self.clean()
                    return option

    def submenu(self, table):
        """
        Affiche le sous menu (client ou contrat ou évenènement ou collaborateur)
        retourne le choix de l'utilisateur
        """
        while True:
            print()
            print(f"*****Menu {table}*****")
            print()
            menu_options = {
                1: "Consulter",
                2: "Créer",
                3: "Modifier",
                # 4: "Supprimer un compte collaborateur",
                4: "Retour au menu principal",
                5: "Fermer",
            }
            for key in menu_options:
                print(key, "--", menu_options[key])
                print()
            try:
                option = int(input("Entrer votre choix : "))
            except ValueError:
                print("Vous devez taper un nombre entre 1 et 5.")
                time.sleep(2)
                self.clean()
                print()
            else:
                if option < 1 or option > 5:
                    print("Vous devez taper un nombre entre 1 et 5.")
                    time.sleep(2)
                    self.clean()
                    print()
                else:
                    self.clean()
                    return option

    def view_menu_read_only(self, table):
        """
        Affiche le sous menu (client ou contrat ou évenènement ou collaborateur)
        retourne le choix de l'utilisateur
        """
        while True:
            print()
            print(f"*****Consulter*****")
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
                print(key, "--", menu_options[key])
                print()
            try:
                option = int(input("Entrer votre choix : "))
            except ValueError:
                print("Vous devez taper un nombre.")
                time.sleep(2)
                self.clean()
                print()
            else:
                if option < 1 or option > len(menu_options):
                    print("Vous devez taper un nombre correspondant au menu.")
                    time.sleep(2)
                    self.clean()
                    print()
                else:
                    self.clean()
                    return option

    def choice_column_to_update(self, table):
        while True:
            print()
            if table == "client":
                print("*****Modifier un compte client*****")
                print("Liste des champs modifiables : ")
                list_of_editable_update_columns = {
                    1: "fullname",
                    2: "email",
                    3: "phone",
                    4: "name_company",
                    5: "Retour au menu principal",
                    6: "Fermer",
                }
            elif table == "event":
                print("*****Modifier un évènement*****")
                print("Liste des champs modifiables : ")
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
                print("*****Modifier un contrat*****")
                print("Liste des champs modifiables : ")
                list_of_editable_update_columns = {
                    1: "client_id",
                    2: "total_amount",
                    3: "balance_due",
                    4: "status",
                }

            elif table == "staff":
                print("*****Modifier un collaborateur*****")
                print("Liste des champs modifiables : ")
                list_of_editable_update_columns = {
                    1: "name",
                    2: "first_name",
                    3: "email",
                    4: "password",
                }

            for key in list_of_editable_update_columns:
                print(key, "--", list_of_editable_update_columns[key])
                print()
            try:
                number_column_to_update = int(input("Entrer votre choix : "))

            except ValueError:
                print(f"Vous devez taper un nombre entre 1 et {len(list_of_editable_update_columns)}.")
                time.sleep(2)
                self.clean()
                print()
            else:
                if number_column_to_update < 1 or number_column_to_update > len(list_of_editable_update_columns):
                    print(f"Vous devez taper un nombre entre 1 et {len(list_of_editable_update_columns)}.")
                    time.sleep(2)
                    self.clean()
                    print()
                else:
                    self.clean()
                    return list_of_editable_update_columns[number_column_to_update]

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
