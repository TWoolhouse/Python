from table import Database
from tags import Tag
import datetime
import queue
import libs
import iofile
import database
import node

PATH = "C:/dev/Code/Python/Project/Orwell/"

def get_data():
    path = PATH+"Data/"
    data = {
    "people": iofile.read.text(path+"people"),
    "birthday": ((n, datetime.date(*map(int, b.split("-")))) for n, b in iofile.read.text(path+"birthday", split_char=" = ")),
    "info": ((n, (Tag(t, d) for t, d in (j.strip().split("-") for j in i.split(",")))) for n, i in iofile.read.text(path+"info", split_char=" = "))
    }
    return data

def repopulate():
    db.database.close()
    with db:
        data = get_data()
        db.new(data["people"])
        for name, bday in data["birthday"]:
            db.insert_birthday(name, bday)
        for name, data in data["info"]:
            for tag in data:
                db.insert_info(name, tag)
    db.database.open()

def db_func(func, *args, **kwargs):
    e = queue.threading.Event()
    db_proc.put((e, func, args, kwargs))
    e.wait()
    res = db_res[e]
    del db_res[e]
    return res

#---Server Functions----------------------------------------------------------#

def Name(name: int):
    return db_func(db.lookup_person, name)

def s_send(client: node.Client, data: iter, prefix: str = "data"):
    count = 0
    if data:
        for i in data:
            client.send(i, "lk"+prefix)
            count += 1
    client.send(count, "length")

def s_callback(client: node.SClient):
    print("{}\n\t{}".format(client.server, "\n\t".join(map(str, client.server.connections.values()))))

def s_repopulate(client):
    db_func(repopulate)
    client.send("", "repopulate")

def s_name(client, fname, lname):
    data = db_func(db.lookup_person_full, fname, lname)
    s_send(client, ("{} {}".format(f, l) for i,f,l in data) if data else data, "name")

def s_info(client, name, tag, value):
    data = db_func(db.lookup_info, name, Tag(tag, value) if tag else None)
    s_send(client, ("{}: {} -> {}".format(Name(p), Tag.name(t), t.name) for i,p,t in data) if data else data, "info")

def s_birthday(client, name, bday):
    data = db_func(db.lookup_birthday, name, bday)
    s_send(client, ("{}: {}".format(Name(p), b) for i, p, b in data) if data else data, "birthday")

db = Database(PATH+"database")

db_proc = queue.Queue()
db_res = {}
s_funcs = {
    "s_repopulate": s_repopulate,
    "s_name": s_name,
    "s_info": s_info,
    "s_birthday": s_birthday,
}
server = node.Server(port=53337, limit=2, password="Orwell", encrypt=69420, funcs=s_funcs, connection=s_callback)

with db, server:
    db.load()
    while True:
        event, func, args, kwargs = db_proc.get()
        db_res[event] = (func(*args, **kwargs))
        event.set()
        db_proc.task_done()
