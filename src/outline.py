from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import print_formatted_text
from src.base import Base, style


class Outline(Base):
    def __init__(self):
        super().__init__()

        self.main_folder = self.path("development/scenes")
        self.GENERATE_SCENES_PROMPT = self.get_text("prompts/scenes/write_chapter_scenes.txt")
        self.GENERATE_SHORT_PROMPT = self.get_text("prompts/outline/short_summary.txt")

    def menu(self):
        print_formatted_text("\nOutline - Select an option:")
        submenu_items = {
            "1": {"name": "Generate novel idea/seed based on your config", "action": lambda: self.generate_idea()},
            "2": {"name": "Generate chapter_summary.txt from full chapter_outline.txt", "action": lambda: self.generate_chapter_summary()},
            "3": {"name": "Generate scenes (chapter_seed.txt) for a chapter in chapter_outline.txt", "action": lambda: self.define_scenes_for_chapter()},
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


    
    def generate_idea(self):
        output_file = "development/outline/seed_summary.txt"
        summary_prompt = self.get_text("prompts/outline/summary.txt")
        settings = self.get_config()
        if not self.object_has_keys(settings, ["genre", "author_style", "themes"]):
            return
        llm_prompt = self.replace_prompts_in_template(summary_prompt, settings)

        print("Prompt is:")
        print(style.GREEN + llm_prompt)
        
        confirmation = prompt(f"Call LLM with prompt (y/n): ")
        if confirmation.lower() == "n":
            return
        
        response = self.call_llm(llm_prompt)
        
        confirmation = prompt(f"Replace the current text in {output_file} with the new text? (y/n): ")

        if confirmation.lower() == "y":
            self.set_text(output_file, response)
            print("Text updated.")
        elif confirmation.lower() == "n":
            return
        else:
            print("Invalid input. Please try again.")


    def define_scenes_for_chapter(self) -> str:
        chapter_outlines = self.get_text("development/outline/chapter_summary.txt")
        print("Choose which chapter to define scenes for:")
        print(chapter_outlines)

        prompts = self.get_config()
        prompts["chapter_outline"] = self.get_text("development/outline/chapter_outline.txt")
        prompts["settings_summary"] = self.get_text("development/settings/settings_summary.txt")
        prompts["character_all_summary"] = self.get_text("development/characters/character_all_summary.txt")

        user_input = prompt("Chapter roman numeral/name (or 9 to exit): ")
        prompts["chapter_roman_numeral"] = user_input
        if user_input == "9":
            return
        
        user_input = prompt("Give the chapter a number eg. 020 (or x to exit): ")
        if user_input == "x":
            return
        
        chapter_number = user_input.strip()
        
        if not self.object_has_keys(prompts, ["genre", "author_style", "themes", "chapter_outline", "settings_summary", "character_all_summary"]):
            print("ERROR: Missing required settings. Please set them in the settings menu.")
            return
        llm_prompt = self.replace_prompts_in_template(self.GENERATE_SCENES_PROMPT, prompts)
        result = self.call_llm(llm_prompt)

        user_input = prompt("Overwrite existing chapter breakdown for chapter_"+chapter_number+"? (y/n): ")
        if user_input == "y":
            self.set_text(f"book/chapter_{chapter_number}/chapter_seed.txt", result)
            self.set_text(f"book/chapter_{chapter_number}/chapter_seed_prompt.txt", llm_prompt)


    def generate_chapter_summary(self):
        full_text = self.get_text("development/outline/chapter_outline.txt")
        prompt_full = self.GENERATE_SHORT_PROMPT + "\n\n" + full_text
        result = self.call_llm(prompt_full)
        self.set_text("development/outline/chapter_summary.txt", result)
        
    

    
