from typing import List, Tuple, Dict, Callable
from prettytable import PrettyTable
from time import sleep
from rich import print
import pyfiglet
import sys

from hierarchical_menus import *

tree = HierarchicalMenus()
main_menu = tree.get_root_menu()


def start_screen(duration: int = 0.5):
    clear_screen()
    title = pyfiglet.figlet_format('CodeForces', font='big')
    print(f'[blue]{title}[/blue]')
    sleep(duration / 2)
    title2 = pyfiglet.figlet_format('Wizard', font='larry3d')
    print(f'[red]{title2}[/red]')
    sleep(duration / 2)
    title3 = pyfiglet.figlet_format('Author:  OjjOj', font='standard')
    print(f'[yellow]{title3}[/yellow]')
    sleep(duration)


def end_screen(duration: int = 0.5):
    clear_screen()
    title = pyfiglet.figlet_format('GoodBye', font='big')
    print(f'[green]{title}[/green]')
    sleep(duration)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt(options: list, prompt_string: str = "Choose your option number: ", data_type: str = "int"):
    while True:
        try:
            if data_type == "int":
                choice = input(prompt_string).strip()
                if choice == "r":
                    return -2
                if -1 <= int(choice) <= len(options):
                    return int(choice) - 1
            elif data_type == "string":
                choice = input(prompt_string).strip()
                return choice
        except ValueError:
            pass


def show_menu(options: List[str], width: int):
    for i, option in enumerate(options):
        print("{} - {}".format(i + 1, option))


def show_table(headers: List[str], rows: List[List[str]], width: int):
    headers.insert(0, "")
    table = PrettyTable()
    table.field_names = headers
    for i, row in enumerate(rows):
        row.insert(0, str(i + 1))
        table.add_row(row)
    print(table)
    print(f"| [yellow]{len(rows)} records[/yellow]")


def show_input(action: Callable, width: int):
    result = action()
    if not result:
        return
    if len(result) == 2:
        headers, rows = result
        show_table(headers=headers, rows=rows, width=width)


def create_screen(menu: Menu, width: int):
    title = tree.get_full_title(menu)
    action = menu.action
    category = menu.category
    options_titles = menu.get_options_titles()

    print(f"{title:-^{width}}")
    print("- " * (width // 2))

    if category == "menu":
        show_menu(options=options_titles, width=width)
    elif category == "table":
        print()
        data = action()
        if data:
            headers, rows = data
            show_table(headers=headers, rows=rows, width=width)
        print()
    elif category == "input":
        show_input(action=action, width=width)

    print("- " * (width // 2))
    print("r - Repeat")
    print("0 - Exit")
    print("-" * width)


def goto(choice: int, menu: Menu):
    if choice >= 0:
        return menu.options[choice]
    elif choice == -2:
        return menu
    else:
        if menu.has_parent():
            return menu.parent
        end_screen()
        sys.exit()


def window(menu: Menu = main_menu, width: int = 50):
    while True:
        clear_screen()
        create_screen(menu, width=width)
        choice = prompt(options=menu.options)
        menu = goto(choice, menu)
