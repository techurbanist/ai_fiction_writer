import fnmatch
import os
import retrying
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class Base:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__)) + "/.."

        self.MODEL_PROMPT_STYLE  = '#44ff00 italic'
        self.MODEL_RESPONSE_STYLE = '#00ff00'
        
    def get_config(self):
        return {
            "genre": self.get_text(self.path("development/config/genre.txt")),
            "book_style": self.get_text(self.path("development/config/book_style.txt")),
            "author_style": self.get_text(self.path("development/config/author_style.txt")),
            "themes": self.get_text(self.path("development/config/themes.txt")),
        }

    def path(self, *args):
        return os.path.join(self.root_dir, *args)
    
    def replace_prompts_in_template(self, template_text, prompts_obj):
        for key, value in prompts_obj.items():
            template_text = template_text.replace(f"[{key}]", value)
        return template_text
    
    def object_has_keys(self, obj, keys):
        for key in keys:
            if key not in obj:
                print("PLEASE MAKE SURE YOU HAVE FILE FOR EACH OF THE FOLLOWING:")
                print(keys)
                return False
        return True
    
    def output_menu_with_prompt(self, menu_items):
        print_formatted_text("\nSelect an option:")
        for item in menu_items:
            print_formatted_text(f"{item}. {menu_items[item]['name']}")
        user_input = prompt("> ")
        return user_input

    def get_text(self, path_name):
        path_name = self.path(path_name)
        if not os.path.exists(path_name):
            raise ValueError("WARNING: File does not exist: " + path_name)
        with open(path_name, 'r') as file:
            return file.read()
        
    def set_text(self, path_name, text):
        path_name = self.path(path_name)
        if not os.path.exists(path_name):
            os.makedirs(os.path.dirname(path_name), exist_ok=True)
        with open(path_name, 'w') as file:
            file.write(text)

    def edit_text(self, description, path_name):
        text = self.get_text(path_name)
        print_formatted_text(f"\n{description}:")
        print_formatted_text(text)

        new_text = prompt("Enter the new text or x to cancel the update: ")
        if new_text == "x":
            return
        
        confirmation = prompt(f"Replace the current text with the new text? (y/n): ")

        if confirmation.lower() == "y":
            self.set_text(path_name, new_text)
            print("Text updated.")
        elif confirmation.lower() == "n":
            return
        else:
            print("Invalid input. Please try again.")


    @retrying.retry(wait_fixed=5000, stop_max_attempt_number=3)
    def call_llm(self, prompt, temperature=0.7):
        print("LLM PROMPT:")
        print(style.GREEN + prompt + style.RESET)
        print("processing... please wait...")

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        result = completion.choices[0].message.content
        print("RESPONSE FROM LLM:")
        print(style.YELLOW + result + style.RESET)
        print(style.RED + "Prompt Tokens: " + str(completion.usage.prompt_tokens) + "  Completion Tokens: " + str(completion.usage.completion_tokens) + style.RESET + "\n")
        return result
    
    def get_menu_from_folder(self, folder: str, file_mask="*"):
        menu = {}
        counter = 1
        for f in sorted(os.listdir(folder)):
            if fnmatch.fnmatch(f, file_mask):
                menu[str(counter)] = {"name": f}
                counter += 1
        menu["x"] = {"name": "Back (x)"}
        return menu
    
    def get_menu_from_files(self, folder, file_mask):
        menu = {}
        counter = 1
        for f in sorted(os.listdir(folder)):
            if fnmatch.fnmatch(f, file_mask):
                menu[str(counter)] = {"name": f}
                counter += 1
        menu["x"] = {"name": "Back (x)"}
        return menu
    
    def get_list_of_files(self, folder, file_mask):
        files = []
        for f in sorted(os.listdir(folder)):
            if fnmatch.fnmatch(f, file_mask):
                files.append(f)
        return files

