import libs
import database as db
import re
import datetime
from tags import Tag

class Database:
    def __init__(self, filepath):
        self.database = db.Database(filepath)

    def __enter__(self):
        self.database.open()
        return self
    def __exit__(self, *args):
        self.database.close()

    def new(self, data):
        self.database.new()

        self.database.table("People", db.Column("fname", db.Type.String, db.Type.NotNull), db.Column(
            "lname", db.Type.String, db.Type.NotNull))
        self.database.table("Opinions", db.Column.Foreign("judge", self.database["People"]), db.Column.Foreign(
            "target", self.database["People"]), db.Column("opinion", db.Type.String, db.Type.NotNull))
        self.database.table("Rating", db.Column.Foreign("judge", self.database["People"]), db.Column.Foreign(
            "target", self.database["People"]), db.Column("value", db.Type.Integer, db.Type.NotNull))
        self.database.table("Birthday", db.Column.Foreign(
            "person", self.database["People"]), db.Column("date", db.Type.Date))

        for obj in Tag.tags.keys():
            self.database.table(obj, db.Column.Foreign(
                "person", self.database["People"]), db.Column("data", db.Type.Integer, db.Type.NotNull))

        for person in data:
            self.insert_person(person)

    def load(self):
        self.database.load()
        return self

    def insert_person(self, name: str):
        self.database.insert(self.database["People"], *Name(name))

    def insert_opinion(self, jname, tname, text):
        jid, tid = self.lookup_person(jname, id=True), self.lookup_person(tname, id=True)
        self.database.insert(self.database["Opinions"], jid, tid, self._opinion_replace_insert(text))
    
    def insert_rating(self, jname, tname, value):
        self.database.insert(self.database["Rating"], self.lookup_person(jname, id=True), self.lookup_person(tname, id=True), value)

    def insert_birthday(self, name: str, date: datetime.date):
        self.database.insert(self.database["Birthday"], self.lookup_person(name, id=True), date)
    
    def insert_info(self, name: str, tag: Tag):
        self.database.insert(self.database[Tag.name(tag)], self.lookup_person(name, id=True), tag.value)

    def lookup_person(self, name: str, id=False):
        res = self.database.select(self.database["People"], name, all=False) if isinstance(name, int) else self.database.select(self.database["People"], *map(db.Condition, Name(name)), all=False)
        return (res[0] if id else Name(*res[1:])) if res else res

    def lookup_person_full(self, fname: str=None, lname: str=None):
        conditions = []
        if fname is not None:
            conditions.append(db.Condition(0, "%"+fname+"%", db.OP.LIKE))
        if lname is not None:
            conditions.append(db.Condition(1, "%"+lname+"%", db.OP.LIKE))
        return self.database.select(self.database["People"], *conditions)

    def lookup_opinion(self, judge=None, target=None, text=None):
        conditions = []
        if isinstance(text, int):
            conditions.append(text)
        else:
            if judge is not None:
                conditions.append(db.Condition(0, self.lookup_person(judge, id=True)))
            if target is not None:
                conditions.append(db.Condition(1, self.lookup_person(target, id=True)))
            if text is not None:
                conditions.append(db.Condition(2, "%"+str(text)+"%", db.OP.LIKE))
        res = self.database.select(self.database["Opinions"], *conditions)
        return ((i, j, t, self._opinion_replace_lookup(q)) for i,j,t,q in res) if res else False

    def lookup_rating(self, judge=None, target=None, value=None, op=db.OP.EQ):
        conditions = []
        if judge is not None:
            conditions.append(db.Condition(0, self.lookup_person(judge, id=True)))
        if target is not None:
            conditions.append(db.Condition(1, self.lookup_person(target, id=True)))
        if value is not None:
            conditions.append(db.Condition(2, value, op))
        return self.database.select(self.database["Rating"], *conditions)

    def lookup_birthday(self, name: str=None, date: datetime.date=None):
        conditions = []
        if name is not None:
            conditions.append(db.Condition(0, self.lookup_person(name, id=True)))
        if date is not None:
            conditions.append(db.Condition(1, date, db.OP.LIKE))
        return self.database.select(self.database["Birthday"], *conditions)

    def lookup_info(self, name: str = None, tag: Tag=None, op = db.OP.EQ):
        conditions = []
        if name is not None:
            conditions.append(db.Condition(0, self.lookup_person(name, id=True)))
        if tag is not None:
            if hasattr(tag, "value"):
                conditions.append(db.Condition(1, tag.value, operator=op))
            tn = Tag.name(tag)
            r = self.database.select(self.database[tn], *conditions)
            return ((i,p,Tag(tn, v)) for i,p,v in r) if r else r
        res = []
        for t,tag in Tag.tags.items():
            r = self.database.select(self.database[t], *conditions)
            if r:
                res.extend(((i,p,tag(v)) for i,p,v in r))
        return res

    def _opinion_replace_lookup(self, text):
        return re.sub("<[\d]+>", lambda x: str(self.lookup_person(int(x.group()[1:-1]))), text)
    def _opinion_replace_insert(self, text):
        return re.sub("(?!<)[\w\s]+(?=>)", lambda x: str(self.lookup_person(x.group(), id=True)), text)

def Name(name: str, lname:str=None) -> list:
    return name.title().split(" ", 1) if lname is None else " ".join((name, lname))
