# dict-bot 📖

A lightweight, terminal-based dictionary and thesaurus built with Python and NLTK WordNet. It provides fast definitions, synonyms, antonyms, and usage examples directly from your command line.

## Features

* **Definitions:** Quick lookup for word meanings.
* **Relations:** Fetch synonyms (`--syn`), antonyms (`--ant`), and hypernyms (`--hyper`).
* **Examples:** View usage examples for words (`--ex`).
* **Interactive Mode:** A REPL-style chat interface (`--chat`).
* **History:** Tracks your search history locally in the project folder.
* **Offline Capable:** Uses the local NLTK WordNet corpus.

## Installation

### 1. Project Setup
Clone or create the project in your workspace:
```bash
mkdir -p ~/Documents/workspace/dict-bot
cd ~/Documents/workspace/dict-bot
# Place main.py here

```

### 2. Python Environment

Create a virtual environment to keep dependencies isolated:

```bash
python3 -m venv dict-env
source dict-env/bin/activate
pip install nltk

```

*(Note: The script automatically downloads WordNet data on the first run if missing.)*

### 3. Global Command Setup

Create a wrapper script to run `dictbot` from anywhere.

1. Create `~/bin` if it doesn't exist:
```bash
mkdir -p ~/bin

```


2. Create the file `~/bin/dictbot` with the following content:
```bash
#!/usr/bin/env bash
APP="$HOME/Documents/workspace/dict-bot"
"$APP/dict-env/bin/python" "$APP/main.py" "$@"

```


3. Make it executable:
```bash
chmod +x ~/bin/dictbot

```


4. Ensure `~/bin` is in your PATH (add to `.bashrc` or `.zshrc` if needed):
```bash
export PATH="$HOME/bin:$PATH"

```



## Usage

Now you can use `dictbot` from any terminal window.

### One-off Commands

```bash
# Define a word
dictbot serendipity

# Get synonyms
dictbot happy --syn

# Get antonyms
dictbot hot --ant

# Get broader terms (hypernyms)
dictbot car --hyper

# See usage examples
dictbot run --ex

```

### Interactive Mode

Enter chat mode for continuous lookups without retyping the command.

```bash
dictbot --chat

```

* Type `word` to define.
* Type `syn word` for synonyms.
* Type `exit` to quit.

### History

View your recent searches (stored in `~/Documents/workspace/dict-bot/.word_history.json`).

```bash
dictbot --history
dictbot --clear

```

