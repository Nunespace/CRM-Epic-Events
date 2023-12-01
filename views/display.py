import os
import platform
import click
import time
from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding


class Display:

    def __init__(self):
        self.console = Console()

    def log(self):
        epic_events = Panel("[bold blue]CRM Epic Events", expand=False, border_style="blue", subtitle="Welcome", padding=(1,8))
        self.console.print(epic_events)
        print()

    def hello(self, firstname):
        self.console.print(f'Bonjour {firstname}!', style="blue")
        time.sleep(2)
        self.clean()

    def display_all_table(self, result):
        for row in result:
            print("row row:", row)

    def display_one_object(self, result):
        print("row :", result)

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")


"""

    def log_styled(self, msg_obj, style):
        self.console.print(msg_obj, style=style)

    def warning(self, msg_obj=None) -> None:
        self.console.print(msg_obj, style="bold yellow")

    def error(self, msg_obj=None) -> None:
        self.console.print(msg_obj, style="bold red")
"""