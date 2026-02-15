from nltk.corpus import wordnet as wn

def define(word):
    synsets = wn.synsets(word)
    if not synsets:
        return "No definition found."
    return synsets[0].definition()

def synonyms(word):
    synsets = wn.synsets(word)
    words = set()
    for s in synsets:
        for l in s.lemmas():
            words.add(l.name())
    return ", ".join(words) if words else "No synonyms."

def reply(msg):
    msg = msg.strip().lower()

    if msg in ("hello", "hi", "domo"):
        return "Hello."
    if msg.startswith("define "):
        return define(msg.split(" ",1)[1])
    if msg.startswith("synonym "):
        return synonyms(msg.split(" ",1)[1])
    if msg == "exit":
        return None

    return "I don't understand."

while True:
    user = input("> ")
    r = reply(user)
    if r is None:
        print("bye")
        break
    print(r)
