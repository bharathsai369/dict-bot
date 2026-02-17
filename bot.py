import click
import json
import os
from nltk.corpus import wordnet as wn

HISTORY_FILE = ".word_history.json"

def save_to_history(word, feature):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    history.append({"word": word, "feature": feature})
    # Keep only last 20 searches
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-20:], f)

def get_wordnet_data(word, mode):
    synsets = wn.synsets(word)
    if not synsets:
        return ["No results found."]
    
    results = set()
    for s in synsets:
        if mode == 'synonym':
            results.update(l.name() for l in s.lemmas())
        elif mode == 'antonym':
            for l in s.lemmas():
                if l.antonyms():
                    results.update(a.name() for a in l.antonyms())
        elif mode == 'hypernym':
            for h in s.hypernyms():
                results.update(l.name() for l in h.lemmas())
        elif mode == 'definition':
            results.add(f"({s.pos()}) {s.definition()}")
        elif mode == 'example':
            for ex in s.examples():
                results.add(ex)
                
    return sorted(list(results))

@click.group()
def cli():
    """A CLI Dictionary and Thesaurus using WordNet."""
    pass

@cli.command()
@click.argument('word')
@click.option('--syn', is_flag=True, help='Get synonyms')
@click.option('--ant', is_flag=True, help='Get antonyms')
@click.option('--hyper', is_flag=True, help='Get hypernyms (broader terms)')
@click.option('--ex', is_flag=True, help='Get usage examples')
def look(word, syn, ant, hyper, ex):
    """Look up a word's definition and relations."""
    mode = 'definition'
    if syn: mode = 'synonym'
    elif ant: mode = 'antonym'
    elif hyper: mode = 'hypernym'
    elif ex: mode = 'example'

    data = get_wordnet_data(word, mode)
    save_to_history(word, mode)
    
    click.secho(f"\nResults for '{word}' [{mode}]:", fg='cyan', bold=True)
    for item in data:
        click.echo(f" • {item.replace('_', ' ')}")

@cli.command()
def history():
    """View your search history."""
    if not os.path.exists(HISTORY_FILE):
        click.echo("History is empty.")
        return
    
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
        click.secho("\nSearch History:", fg='yellow', bold=True)
        for i, entry in enumerate(data, 1):
            click.echo(f"{i}. {entry['word']} ({entry['feature']})")

if __name__ == '__main__':
    cli()