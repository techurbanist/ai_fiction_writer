from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text
from src.book_setup import Book_Config
from src.outline import Outline
from src.settings import Settings
from src.characters import Characters
from src.chapter_selector import ChapterSelector

book_config = Book_Config()
outline = Outline()
settings = Settings()
characters = Characters()
chapter_selector = ChapterSelector()


def exit_app():
    print_formatted_text("Goodbye!")
    exit()

menu_items = {
    "1": {"name": "Novel config: voice, style, genre", "action": lambda: book_config.menu()},
    "2": {"name": "Novel outline", "action": lambda: outline.menu()},
    "3": {"name": "Develop Settings/location", "action": lambda: settings.menu()},
    "4": {"name": "Develop Characters", "action": lambda: characters.menu()},
    "5": {"name": "Work on chapter", "action": lambda: chapter_selector.menu()},
    "9": {"name": "Exit", "action": exit_app},
}


def main():
    while True:
        print_formatted_text("\nWhat would you like to do?")
        for item in menu_items:
            print_formatted_text(f"{item}. {menu_items[item]['name']}")

        user_input = prompt("> ")

        if user_input in menu_items:
            menu_items[user_input]["action"]()
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
