from actions import *
from typing import Callable


class Menu:
    def __init__(self, title: str, options=None, action: Callable = None, parent=None, category: str = "menu"):
        if options is None:
            options = []
        self.title = title
        self.options = options
        self.action = action
        self.parent = parent
        self.category = category

    def set_parent(self, parent):
        self.parent = parent

    def set_action(self, action):
        self.action = action

    def set_category(self, category):
        if category in ("menu", "table", "input"):
            self.category = category

    def add_option(self, option):
        self.options.append(option)

    def run(self):
        if self.action:
            self.action()

    def get_options_titles(self):
        if self.options:
            return [option.title for option in self.options]

    def has_parent(self):
        return bool(self.parent)


class HierarchicalMenus:
    __tree = None

    @staticmethod
    def create_tree():
        if HierarchicalMenus.__tree is None:
            HierarchicalMenus()
        return HierarchicalMenus.__tree

    def __init__(self):
        HierarchicalMenus.__instance = self

        # creating menus
        show_all_names_menu = Menu("Show All")
        show_all_names_menu.set_action(show_all_names)
        show_all_names_menu.set_category("table")

        search_names_menu = Menu("Search")
        search_names_menu.set_action(search_names)
        search_names_menu.set_category("input")

        show_all_ratings_menu = Menu("Show All")
        show_all_ratings_menu.set_action(show_all_ratings)
        show_all_ratings_menu.set_category("table")

        search_ratings_menu = Menu("Search")
        search_ratings_menu.set_action(search_ratings)
        search_ratings_menu.set_category("input")

        show_all_solved_problems_menu = Menu("Show All")
        show_all_solved_problems_menu.set_action(show_all_solved_problems)
        show_all_solved_problems_menu.set_category("table")

        search_solved_problems_menu = Menu("Search")
        search_solved_problems_menu.set_action(search_solved_problems)
        search_solved_problems_menu.set_category("input")

        names_menu = Menu("Names")
        names_menu.add_option(show_all_names_menu)
        names_menu.add_option(search_names_menu)

        ratings_menu = Menu("Ratings")
        ratings_menu.add_option(show_all_ratings_menu)
        ratings_menu.add_option(search_ratings_menu)

        solved_problems_menu = Menu("Solved Problems")
        solved_problems_menu.add_option(show_all_solved_problems_menu)
        solved_problems_menu.add_option(search_solved_problems_menu)

        add_user_menu = Menu("Add User")
        add_user_menu.set_action(add_user)
        add_user_menu.set_category("input")

        remove_user_menu = Menu("Remove User")
        remove_user_menu.set_action(remove_user)
        remove_user_menu.set_category("input")

        main_menu = Menu("Codeforces Wizard")
        main_menu.add_option(names_menu)
        main_menu.add_option(ratings_menu)
        main_menu.add_option(solved_problems_menu)
        main_menu.add_option(add_user_menu)
        main_menu.add_option(remove_user_menu)

        # Set parents
        main_menu.set_parent(None)
        names_menu.set_parent(main_menu)
        ratings_menu.set_parent(main_menu)
        solved_problems_menu.set_parent(main_menu)
        add_user_menu.set_parent(main_menu)
        remove_user_menu.set_parent(main_menu)

        show_all_names_menu.set_parent(names_menu)
        search_names_menu.set_parent(names_menu)

        show_all_ratings_menu.set_parent(ratings_menu)
        search_ratings_menu.set_parent(ratings_menu)

        show_all_solved_problems_menu.set_parent(solved_problems_menu)
        search_solved_problems_menu.set_parent(solved_problems_menu)

        self.root = main_menu

    def get_root_menu(self):
        return self.root

    def get_full_title(self, menu):
        if self.root == menu:
            return self.root.title
        return self.get_full_title(menu.parent) + " > " + menu.title
