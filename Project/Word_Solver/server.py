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
    # print("VALID", phrase, length)
    s_text = phrase.replace("_", "\\w")
    l_text = len(phrase)
    prog = re.compile(s_text, re.I)

    res = []
    for name, language in languages.items():
        # print("Language:", name)
        for word in language:
            if ((not length) or l_text == len(word)) and re.match(s_text, word):
                # print(word)
                res.append(word)
    return res

class VALID(node.Dispatch):

    def handle(self):
        data = valid(self.data.data, "LENGTH" in self.data.tags)
        print("Request: {} -> <{}> {}".format(self.__class__.__name__, len(data), self.data.data))
        self.node.send(len(data), "VALID", node.Tag("COUNT"))
        self.node.send("|".join(data), "DATA", "VALID")

server = node.Server("", 80, dispatchers=(VALID,))
with server:
    input("Press Enter to Exit\n")
