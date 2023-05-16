# AI Fiction Writer

This is an experimental project aimed at probing the capabilities and limitations of Large Language Models (LLMs) in the context of writing.

The experiment revealed that LLMs struggle with generating vast amounts of prose, maintaining consistency across chapters, and they frequently employ repetitive phrasing.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -r requirements.txt
```

You will need an OpenAI API key and access to GPT4.

:warning: WARNING: This application utilizes GPT4, which can incur significant costs! Regularly monitor your API usage via the OpenAI developer console and ensure to set cost limits.

Remember to set your OPENAI_API_KEY environment variable, as the application cannot function without it.


## Usage

To begin, set the style, genre, and themes in the text files located in the `/development/*.txt` files. Although you can do this using menu 1, direct file editing is often simpler.

* `author_style.txt` - Your preferred writing style. Avoid using names of living authors or those protected by copyright.
* `book_style.txt` - A single-sentence description of your novel's style.
* `genre.txt` - The concise genre of your novel (e.g., "science fiction").
* `themes.txt` - A bulleted list of the primary themes you wish to explore in your novel.

This application is a command-line tool. Initiate it using:

```bash
python main.py
```

In general, the process involves crafting "seeds" (akin to seeds of an idea). These seeds are brief outlines describing characters, settings, scenes, etc., which the LLM expands upon. All developmental writing is directed into the `development` sub-folders.

### Menus

Navigate through the command-line menus using the numbers adjacent to each menu option and the 'x' key to go back.

The commands should be executed in sequence as they gradually define the novel and flesh out characters, settings, scenes, etc.

Note: Currently, the dependencies aren't explicitly clear, so examining the code might be necessary to comprehend them.

### Terminology

The following terms are used in the menus and to organize prompts and development material:

* Outline: This is a high-level summary of the book's structure, including main events and turning points. It helps maintain the story's pacing and coherence, ensuring that all elements are connected and consistent.
* Characters: These are detailed descriptions of each character, including their appearance, personality, background, motivations, relationships, and development arc. This helps maintain consistency in character behavior and dialogue, as well as create well-rounded and believable characters.
* Settings: Detailed notes about the story's settings, including geographical, historical, and cultural context. This helps create a vivid and immersive world for their readers.
* Scenes: A breakdown of the story into individual scenes, with brief descriptions of each. This helps track the progression of the story and ensure a proper balance of action, dialogue, and description.
* Research (not implemented): Any research conducted for the book, including historical, scientific, or cultural information relevant to the story. 
* Timeline (not implemented): A chronological list of events, often including dates and times, that helps authors maintain consistency in their narrative and ensure that the story's events unfold logically.
* Style guide (not implemented): A list of guidelines for the author's writing style, including preferred grammar, punctuation, and formatting. This helps authors maintain consistency throughout the book and makes the editing process smoother.


## Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss your proposed modifications.

## License

[MIT](https://choosealicense.com/licenses/mit/)



