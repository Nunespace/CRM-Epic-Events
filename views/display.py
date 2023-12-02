import os
import platform
import click
import time
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.padding import Padding


class Display:
    def __init__(self):
        self.console = Console()

    def log(self):
        epic_events = Panel(
            "[bold blue]CRM Epic Events",
            expand=False,
            border_style="blue",
            subtitle="Welcome",
            padding=(1, 8),
        )
        self.console.print(epic_events)
        print()

    def hello(self, firstname):
        self.console.print(f"Bonjour {firstname}!", style="blue")
        time.sleep(2)
        self.clean()

    def display_table(self, result, table, all=False):
        if table == "client":
            table_display = self.table_client(result, all)
        if table == "contract":
            table_display = self.table_contract(result, all)
        print()
        self.console.print(table_display)
        print()
        time.sleep(4)

    def table_client(self, result, all):
        table_display = Table(
            title="Clients", show_lines=True, box=box.MINIMAL_DOUBLE_HEAD
        )
        table_display.add_column("Id", style="cyan", no_wrap=True)
        table_display.add_column("Nom complet", style="magenta", no_wrap=True)
        table_display.add_column("Email", style="green")
        table_display.add_column(
            "Téléphone",
            justify="right",
            style="cyan",
        )
        table_display.add_column("Entreprise", style="magenta")
        table_display.add_column("Création", style="green")
        table_display.add_column("Mise à jour", style="green")
        table_display.add_column(
            "Contact commercial", justify="right", style="cyan"
        )
        if all:
            for row in result:
                table_display.add_row(
                    f"{row.id}",
                    f"{row.fullname}",
                    f"{row.email}",
                    f"{row.phone}",
                    f"{row.name_company}",
                    f"{row.date_creation}",
                    f"{row.date_update}",
                    f"{row.commercial_contact_id}",
                )

            return table_display
        else:
            table_display.add_row(
                f"{result.id}",
                f"{result.fullname}",
                f"{result.email}",
                f"{result.phone}",
                f"{result.name_company}",
                f"{result.date_creation}",
                f"{result.date_update}",
                f"{result.commercial_contact_id}",
            )
            return table_display

    def table_contract(self, result, all):
        table_display = Table(
            title="Contrats", show_lines=True, box=box.MINIMAL_DOUBLE_HEAD
        )
        table_display.add_column("Id", style="cyan", no_wrap=True)
        table_display.add_column("Client (id)", style="magenta", no_wrap=True)
        table_display.add_column("Contact commercial (id)", style="green")
        table_display.add_column(
            "Total dû",
            justify="right",
            style="cyan",
        )
        table_display.add_column("Reste à payer", style="magenta")
        table_display.add_column("Création", style="green")
        table_display.add_column("Statut (signature)", style="green")

        if all:
            for row in result:
                table_display.add_row(
                    f"{row.id}",
                    f"{row.client_id}",
                    f"{row.commercial_contact_id}",
                    f"{row.total_amount}",
                    f"{row.balance_due}",
                    f"{row.date_creation}",
                    f"{row.status}",
                )

            return table_display
        else:
            table_display.add_row(
                f"{result.id}",
                f"{result.client_id}",
                f"{result.commercial_contact_id}",
                f"{result.total_amount}",
                f"{result.balance_due}",
                f"{result.date_creation}",
                f"{result.status}",
            )

            return table_display

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
