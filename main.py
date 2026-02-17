#!/usr/bin/env python3
import sys
import json
import argparse
import os
from pathlib import Path
from nltk.corpus import wordnet as wn

# --- Configuration: Save in Project Folder ---
# This ensures the history file is created in the same directory as this script
APP_DIR = Path(__file__).resolve().parent
HISTORY_FILE = APP_DIR / ".word_history.json"

class Bcolors:
    HEADER, BOLD, CYAN, YELLOW, RED, GREEN, BLUE, ENDC = (
        '\033[95m', '\033[1m', '\033[96m', '\033[93m', 
        '\033[91m', '\033[92m', '\033[94m', '\033[0m'
    )

def die(msg, code=1):
    print(f"{Bcolors.RED}error:{Bcolors.ENDC} {msg}", file=sys.stderr)
    sys.exit(code)

# --- Logic ---

def get_wordnet_data(word, mode):
    synsets = wn.synsets(word)
    if not synsets:
        return []

    results = set()
    for s in synsets:
        if mode == 'synonym':
            results.update(l.name() for l in s.lemmas() if l.name().lower() != word.lower())
        elif mode == 'antonym':
            for l in s.lemmas():
                if l.antonyms():
                    results.update(a.name() for a in l.antonyms())
        elif mode == 'hypernym':
            for h in s.hypernyms():
                results.update(l.name() for l in h.lemmas())
        elif mode == 'example':
            for ex in s.examples():
                results.add(ex)
        else: # definition
            results.add(f"{Bcolors.YELLOW}({s.pos()}){Bcolors.ENDC} {s.definition()}")
                
    return sorted(list(results))

def format_output(word, mode, data):
    output = []
    output.append(f"{Bcolors.BOLD}{Bcolors.HEADER}{word.upper()}{Bcolors.ENDC} {Bcolors.CYAN}[{mode}]{Bcolors.ENDC}")
    
    if not data:
        output.append(f"{Bcolors.RED}No results found.{Bcolors.ENDC}")
    else:
        for item in data:
            clean_item = item.replace('_', ' ')
            output.append(f" {Bcolors.GREEN}•{Bcolors.ENDC} {clean_item}")
    
    return "\n".join(output)

def save_history(word, mode):
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except: history = []
    
    # Remove duplicate if exists to push it to top
    history = [h for h in history if not (h['word'] == word and h['mode'] == mode)]
    history.insert(0, {"word": word, "mode": mode})
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:50], f, indent=2)

def show_history():
    if not HISTORY_FILE.exists():
        print(f"{Bcolors.YELLOW}No history found in {HISTORY_FILE}{Bcolors.ENDC}")
        return
    
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except: 
        print(f"{Bcolors.RED}Corrupt history file.{Bcolors.ENDC}")
        return

    print(f"\n{Bcolors.BOLD}--- SEARCH HISTORY ---{Bcolors.ENDC}")
    for i, entry in enumerate(data, 1):
        print(f"{Bcolors.YELLOW}[{i}]{Bcolors.ENDC} {entry['word']} {Bcolors.CYAN}({entry['mode']}){Bcolors.ENDC}")

def chat_mode():
    print(f"{Bcolors.BOLD}DictBot Interactive Mode{Bcolors.ENDC}")
    print(f"Commands: {Bcolors.YELLOW}<word>{Bcolors.ENDC} (def) | {Bcolors.YELLOW}syn <word>{Bcolors.ENDC} | {Bcolors.YELLOW}ant <word>{Bcolors.ENDC} | {Bcolors.YELLOW}hyper <word>{Bcolors.ENDC} | {Bcolors.YELLOW}ex <word>{Bcolors.ENDC}")
    print(f"Other:    {Bcolors.YELLOW}history{Bcolors.ENDC} | {Bcolors.YELLOW}clear{Bcolors.ENDC} | {Bcolors.YELLOW}exit{Bcolors.ENDC}")
    
    while True:
        try:
            user_input = input(f"\n{Bcolors.BLUE}>>{Bcolors.ENDC} ").strip().split()
            if not user_input: continue
            
            cmd = user_input[0].lower()
            
            if cmd in ['exit', 'quit', 'q']:
                break
            
            if cmd == 'history':
                show_history()
                continue

            if cmd == 'clear':
                if HISTORY_FILE.exists(): HISTORY_FILE.unlink()
                print(f"{Bcolors.GREEN}History cleared.{Bcolors.ENDC}")
                continue
            
            mode = 'definition'
            word = None

            if cmd == 'syn' and len(user_input) > 1:
                mode = 'synonym'; word = user_input[1]
            elif cmd == 'ant' and len(user_input) > 1:
                mode = 'antonym'; word = user_input[1]
            elif cmd == 'ex' and len(user_input) > 1:
                mode = 'example'; word = user_input[1]
            elif cmd == 'hyper' and len(user_input) > 1:
                mode = 'hypernym'; word = user_input[1]
            else:
                # Default case: assume input is just the word
                word = user_input[0]

            data = get_wordnet_data(word, mode)
            print(format_output(word, mode, data))
            save_history(word, mode)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"{Bcolors.RED}Error: {e}{Bcolors.ENDC}")

# --- Main ---

def main():
    parser = argparse.ArgumentParser(prog="dictbot")
    parser.add_argument("word", nargs="?", help="Word to lookup")
    parser.add_argument("--syn", action="store_true", help="Get synonyms")
    parser.add_argument("--ant", action="store_true", help="Get antonyms")
    parser.add_argument("--hyper", action="store_true", help="Get hypernyms")
    parser.add_argument("--ex", action="store_true", help="Get usage examples")
    parser.add_argument("--chat", action="store_true", help="Enter interactive chat mode")
    parser.add_argument("--history", action="store_true", help="View search history")
    parser.add_argument("--clear", action="store_true", help="Clear history")
    
    args = parser.parse_args()

    # Ensure WordNet is ready
    try:
        wn.ensure_loaded()
    except:
        import nltk
        nltk.download('wordnet', quiet=True)

    if args.clear:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        print(f"{Bcolors.GREEN}History cleared.{Bcolors.ENDC}")
        return

    if args.history:
        show_history()
        return

    if args.chat:
        chat_mode()
        return

    if not args.word:
        parser.print_help()
        return

    mode = 'definition'
    if args.syn: mode = 'synonym'
    elif args.ant: mode = 'antonym'
    elif args.hyper: mode = 'hypernym'
    elif args.ex: mode = 'example'

    data = get_wordnet_data(args.word, mode)
    print(format_output(args.word, mode, data))
    save_history(args.word, mode)

if __name__ == "__main__":
    main()