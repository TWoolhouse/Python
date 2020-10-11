import website
import secrets
from caching import cache

class Session(website.Session):

    def __init__(self, id: str):
        if id is None:
            id = secrets.token_urlsafe(32)
        super().__init__(id)
        self.auth = False

class AuthRequest(website.Request):

    KEY = "test"
    keys = {}
    async def handle(self):
        key = self.client.query.get("key")
        if key == self.KEY:
            self.client.session.auth = True

class DataRequest(website.Request):

    async def handle(self):
        self.client.buffer << website.buffer.Python(f"{website.path}page/cupboard/reader.html", self)

class GenerateRequest(website.Request):

    async def handle(self):
        expire = self.client.query.get("exp", None)
        if not expire:
            return self.client.buffer << website.buffer.File(f"{website.path}page/cupboard/generate.html")

        amount = self.client.query["amt"]
        self.new_key = 5
        return self.client.buffer << website.buffer.Python(f"{website.path}page/cupboard/show_key.html", self)

class RootRequest(website.Request):

    sessions = website.Sessions(Session)
    @website.Request.secure
    async def handle(self):
        self.client.session = self.sessions[self.client.cookie.value("sid")]
        self.client.cookie["sid"] = self.client.session.id
        self.client.cookie["sid"]["path"] = "/cupboard"
        self.client.cookie["sid"]["Max-Age"] = 86400
        self.client.cookie["sid"]["Secure"] = self.client.cookie["sid"]["HttpOnly"] = True

        if not self.client.session.auth:
            await AuthRequest(self.client, self.request, self.seg)
        if not self.client.session.auth:
            return self.client.buffer << website.buffer.File(f"{website.path}page/cupboard/key.html")
        return self.tree.traverse(self.request, self.seg, self.client)

    tree = website.Tree(
        DataRequest,
        DataRequest,
        DataRequest,
        gen=GenerateRequest,
        genkey=GenerateRequest,
    )

request = RootRequest