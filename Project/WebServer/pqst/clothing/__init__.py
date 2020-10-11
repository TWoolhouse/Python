import website
from interface import Interface
from . import scraper
import random

class RandomGen(website.Request):

    sections = (*scraper.Uniqlo.CAT,)

    async def handle(self):
        self.client.buffer << website.buffer.Python(f"{website.path}page/clothing/result.html", self)

    async def generate(self):
        output = ""
        types = set()
        picked = set()
        for section in range(random.randint(2, min(6, len(self.sections)))):
            for i in range(64):
                section = random.choice(tuple(self.sections))
                if section not in types:
                    types.add(section)
                    break
            else:
                break
            print("Section:", section)
            response = await Interface.process(scraper.Uniqlo(section).process)
            for i in range(64):
                single = random.choice(tuple(response))
                if single not in picked:
                    picked.add(single)
                    break
            else:
                continue
            response = response[single]
            output += f"""<a class="link" href="{single}"><img src="{response["img"]}" title="{response["name"]}"">{response["name"]}</a>"""
        return output

class Home(website.Request):

    async def handle(self):
        self.client.buffer << website.buffer.Python(f"{website.path}page/clothing/home.html", self)

request = website.Tree(
    Home, Home, Home,
    random=RandomGen,
)