import os
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text
from src.base import Base, style


class Characters(Base):
    def __init__(self):
        super().__init__()

        self.main_folder = self.path("development/characters")
        self.GENERATE_SNIPPET_PROMPT = self.get_text("prompts/characters/summarise.txt")
        self.GENERATE_SHORT_PROMPT = self.get_text("prompts/characters/summarise_short.txt")

    
    def menu(self):
        print_formatted_text("\nCharacters - Select an option:")
        submenu_items = {
            "1": {"name": "Regenerate character snippets from full descriptions", "action": lambda: self.create_snippet_files()},
            "2": {"name": "Compile character_all_snippets.txt file from snippets sub folders", "action": lambda: self.create_character_files()},
            "3": {"name": "Regenerate character_all_summary.txt file using LLM", "action": lambda: self.create_short_summary()},
            "9": {"name": "Back (x)", "action": lambda: None},
        }

        while True:
            user_input = self.output_menu_with_prompt(submenu_items)

            if user_input == "x":
                break

            if user_input in submenu_items:
                submenu_items[user_input]["action"]()
                if user_input == "9":
                    break
            else:
                print("Invalid option. Please try again.")

    
    def get_summary_from_full(self, full_text: str) -> str:
        prompt_full = self.GENERATE_SNIPPET_PROMPT + "\n\n" + full_text
        result = self.call_llm(prompt_full)
        return result
        

    def create_snippet_files(self):
        confirmation = prompt(f"Call LLM with each long character profile and create the short snippet for each (y/n): ")
        if confirmation.lower() == "n":
            return
        for setting_folder in os.listdir(self.main_folder):
            setting_path = Path(self.main_folder) / setting_folder
            if setting_path.is_dir():
                full_txt_path = setting_path / "long_profile.txt"
                if full_txt_path.exists():
                    with open(full_txt_path, "r") as full_file:
                        full_text = full_file.read()

                    summary = self.get_summary_from_full(full_text)
                    snippet_txt_path = setting_path / "snippet.txt"
                    with open(snippet_txt_path, "w") as snippet_file:
                        snippet_file.write(summary)
    


    def create_character_files(self):
        settings_all_names_path = Path(self.main_folder) / "character_all_names.txt"
        settings_all_snippets_path = Path(self.main_folder) / "character_all_snippets.txt"
        
        with open(settings_all_names_path, "w") as names_file, open(settings_all_snippets_path, "w") as snippets_file:
            for setting_folder in os.listdir(self.main_folder):
                setting_path = Path(self.main_folder) / setting_folder
                if setting_path.is_dir():
                    setting_name = setting_folder.replace("_", " ")
                    names_file.write(f"{setting_name}\n")
                    
                    snippet_path = setting_path / "snippet.txt"
                    if snippet_path.exists():
                        with open(snippet_path, "r") as snippet_file:
                            snippet = snippet_file.read().strip()
                            snippets_file.write(f"{setting_name}: {snippet}\n")

        print("Done.", settings_all_names_path, settings_all_snippets_path, "regenerated.")



    def create_short_summary(self):
        full_text = self.get_text("development/characters/character_all_snippets.txt")
        prompt_full = self.GENERATE_SHORT_PROMPT + "\n\n" + full_text
        result = self.call_llm(prompt_full)
        self.set_text("development/characters/character_all_summary.txt", result)
