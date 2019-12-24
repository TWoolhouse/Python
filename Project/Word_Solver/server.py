import libs
import node
import re

path = "C:/dev/Code/TextFiles/Other/"
languages = {}

def load(lang="all"):
    languages[lang] = set()
    with open(path+lang+"_words.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip().lower()
            languages[lang].add(line)
load()

def valid(phrase, length=True):
    s_text = phrase.replace("_", "\\w")
    l_text = len(phrase)
    prog = re.compile(s_text, re.I)

    res = []
    for name, language in languages.items():
        print("Language:", name)
        for word in language:
            if l_text == len(word) and re.match(s_text, word):
                print(word, s_text)
                res.append(word)
    return res

class VALID(node.Dispatch):

    def handle(self):
        data = valid(self.data.data, "LENGTH" in self.data.tags)
        self.node.send(len(data), "VALID", node.Tag("COUNT"))
        for w in data:
            self.node.send(w, "DATA", "VALID")

server = node.Server("", 80, dispatchers=(VALID,))
with server:
    input("Press Enter to Exit\n")
