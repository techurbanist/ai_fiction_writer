from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text
from src.base import Base


class Book_Config(Base):
    def __init__(self):
        super().__init__()

        self.GENRE_FILE = "development/config/genre.txt"
        self.BOOK_STYLE_FILE = "development/config/book_style.txt"
        self.AUTHOR_STYLE_FILE = "development/config/author_style.txt"
        self.THEMES_FILE = "development/config/themes.txt"

 
    def menu(self):
        print_formatted_text("\nSelect a config to edit:")
        submenu_items = {
            "1": {"name": "Genre", "action": lambda: self.edit_text("Genre", self.GENRE_FILE)},
            "2": {"name": "Book style", "action": lambda: self.edit_text("Book style", self.BOOK_STYLE_FILE)},
            "3": {"name": "Author style", "action": lambda: self.edit_text("Author style", self.AUTHOR_STYLE_FILE)},
            "4": {"name": "Themes", "action": lambda: self.edit_text("Themes", self.THEMES_FILE)},
            "5": {"name": "Back (x)", "action": lambda: None},
        }

        while True:
            user_input = self.output_menu_with_prompt(submenu_items)

            if user_input == "x":
                break

            if user_input in submenu_items:
                submenu_items[user_input]["action"]()
                if user_input == "5":
                    break
            else:
                print("Invalid option. Please try again.")


    