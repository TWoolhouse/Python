import urllib.request
from caching import cache
import re

class Site:

    BASE = ""
    CAT = {}

    @staticmethod
    @cache
    def _request(url: str) -> str:
        request = urllib.request.Request(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        print("Send Request:", request.get_full_url())
        return urllib.request.urlopen(request).read().decode("utf-8")

    def request(self) -> str:
        return self._request(self.BASE+self.CAT[self.category])

    def __init__(self, category: str):
        self.category = category

    def process(self):
        return [{"name": "Test", "url": "www.example.com"}]

    def output(self):
        SIZE = 120
        for url, item in self.process().items():
            print(f"{item['name']}\n\t{url}\n\t{item['img']}")

class Uniqlo(Site):

    __re_item = re.compile("<article class=\"productTile product-tile-component js_product-tile-component  js-quickshop-tile\"[\\s\\S]*?<img class=\"productTile__image owl-lazy\" src=\"([^\\s]*?)\\?[\\s\\S]*?<a class=\".*?name-link.*?\" href=\"([^\\s]+)(?:\").*>([\\s\\S]*?)</a>[\\s\\S]*?</article>")

    BASE = "https://www.uniqlo.com/uk/en/"
    CAT = {
        "mtshirt": "men/tops/t-shirts-tops/short-sleeved-t-shirts",
        "mltshirt": "men/tops/t-shirts-tops/long-sleeved-t-shirts",
        "mhoodie": "men/tops/sweatshirts-hoodies",
        "mcshirt": "men/tops/shirts/casual-shirts",
        "msshirt": "men/tops/shirts/smart-shirts",
        "mshort": "men/bottoms/shorts",
        "mjacket": "men/outerwear/coats-jackets/jackets",
        "mcoat": "men/outerwear/coats-jackets/coats",
        "mpolo": "men/tops/polo-shirts",
        "mjeans": "men/bottoms/jeans",
        "mtrousers": "men/bottoms/trousers-chinos-sweatpants",
    }

    def process(self) -> dict:
        data = self.request()
        links = {
            f"https://www.uniqlo.com{i.group(2).strip()}" : {
                "name": i.group(3).strip(),
                "img": i.group(1).strip(),
            } for i in self.__re_item.finditer(data)}
        return links