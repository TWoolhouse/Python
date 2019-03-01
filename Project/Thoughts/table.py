import libs
import iofile
import re
import crypt

#---Global Variables-----------------------------------------------------------#

iofile.path("C:/dev/Code/Python/Project/Thoughts/Data/")
file_name = "people"
sql = iofile.sql(file_name)

#---Classes--------------------------------------------------------------------#

class Person:

    @staticmethod
    def id_lookup(id, cols="*"):
        return sql.select("people", id, cols=cols, conditional="ID = ?", all=False) or False

    @staticmethod
    def name_lookup(name, lname=None, cols="*"):
        name = ["%"+i+"%" for i in ([name, lname] if lname else name.split(" ", 1))]
        return sql.select("people", *name, cols=cols, conditional="(fname LIKE ?) AND (lname LIKE ?)", all=False) or False

    @staticmethod
    def name_search(fname=None, lname=None, start=True, end=True, all=True, cols="*"):
        return sql.select("people", "{}{}{}".format("%" if start else "", fname if fname else "", "%" if end else ""), "{}{}{}".format("%" if start else "", lname if lname else "", "%" if end else ""), cols=cols, conditional="fname LIKE ? AND lname LIKE ?", all=all) or False

    @staticmethod
    def name(person):
        return " ".join(person[1:])

    @staticmethod
    def add(fname, lname):
        sql.insert("people", str(fname).title(), str(lname).title(), parameters=("fname", "lname"))

class Opinion:

    @staticmethod
    def id_lookup(id, cols="*"):
        return sql.select("opinion", id, cols=cols, conditional="ID = ?", all=False) or False

    @staticmethod
    def person_lookup(tar, person=None, cols="*"):
        return sql.select("opinion", tar, person if person else "%", cols=cols, conditional="targetID LIKE ? AND personID LIKE ?") or False

    @staticmethod
    def quote_text(opinion):
        q = opinion[3].replace("<t>", "<"+str(opinion[1])+">").replace("<s>", "<"+str(opinion[2])+">")
        return re.sub("<\d*>", lambda x: Person.name(Person.id_lookup(x.group(0)[1:-1])), q)

    @staticmethod
    def pretty(op):
        return "{} - {} -> {}".format(Opinion.quote_text(op), *(Person.name(Person.id_lookup(op[i])) for i in range(2, 0, -1)))

    @staticmethod
    def add(tar_id, person_id, quote, *tags):
        tar_id, person_id, quote, tags = str(tar_id), str(person_id), str(quote), ["["+str(i)+"]" for i in tags]
        quote = re.sub("(<{}>)|(<{}>)".format(tar_id, person_id), lambda x: "<t>" if x.group(1) else "<s>", quote)
        quote  = re.sub("<\w* \w*>", lambda x: "<{}>".format(id(Person.name_lookup(x.group(0)[1:-1], cols="ID"))), quote)
        args = [tar_id, person_id, quote.strip()]
        params = ["targetID", "personID", "quote"]
        if tags:
            args.append("".join(tags))
            params.append("tags")
        if re.search("<\d*>", quote):
            args.append(",".join({i[1:-1] for i in re.findall("<\d*>", quote)}))
            params.append("extern_ref")
        sql.insert("opinion", *args, parameters=tuple(params))

class Relationship:

    @staticmethod
    def id_lookup(id, cols="*"):
        return sql.select("relationship", id, cols=cols, conditional="ID = ?", all=False) or False

    @staticmethod
    def person_lookup(a_id, b_id=None, all=True):
        return (sql.select("relationship", a_id, b_id, b_id, a_id, conditional="(aID = ? AND bID = ?) OR (aID = ? AND bID = ?)", all=all) or False) if b_id else (sql.select("relationship", a_id, a_id, conditional="aID = ? OR bID = ?", all=all) or False)

    @staticmethod
    def pretty(r):
        return "{0} -{2}- {1}".format(*(Person.name(Person.id_lookup(r[i])) for i in range(1, 3)), Relationship.states[r[3]])

    @staticmethod
    def add(a_id, b_id, state):
        state_val = Relationship.states.index(state)
        sql.insert("relationship", a_id, b_id, state_val, parameters=("aID", "bID", "state"))

    states = ["Current", "Over"]

class Info:
    pass

#---Functions------------------------------------------------------------------#

def id(val):
    return val[0]

def encrypt(key):
    iofile.write.bin(file_name, crypt.encrypt(iofile.read.bin(file_name, ext="db"), key, False), ext="encrypt")
def decrypt(key):
    iofile.write.bin(file_name, crypt.decrypt(iofile.read.bin(file_name, ext="encrypt"), key, False), ext="db")
def backup():
    iofile.write.bin(file_name+".encrypt", iofile.read.bin(file_name, ext="encrypt"), ext="backup")
    #iofile.write.bin(file_name+".db", iofile.read.bin(file_name, ext="db"), ext="backup")


def setup(): # This is the code to make a new database and transfer all the information over
    sql.new()
    sql.table("people", "ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL", "fname TEXT", "lname TEXT")
    sql.command("VACUUM")

    print("Populating Table: people")
    for i in iofile.read.text("people"):
       Person.add(*i.split(" ", 1))

    sql.table("opinion", "ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL", "targetID INTEGER NOT NULL", "personID INTEGER NOT NULL", "quote TEXT", "tags TEXT", "extern_ref TEXT", "FOREIGN KEY (targetID) REFERENCES people(ID)", "FOREIGN KEY (personID) REFERENCES people(ID)")
    opinions = [i for i in iofile.read.text("opinions", "<#>")]
    print("Populating Table: opinion")
    for i in opinions:
        x = [id(Person.name_lookup(i[j], cols="ID")) for j in range(2)]
        for j in i[2:]:
            tags = [i[1:-1] for i in re.findall("\[.*\]", j)]
            j = re.sub("\[.*\]", "", j)
            Opinion.add(*x, j, *tags)

    sql.table("relationship", "ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL", "aID INTEGER NOT NULL", "bID INTEGER NOT NULL", "state TINYINT", "FOREIGN KEY (aID) REFERENCES people(ID)", "FOREIGN KEY (bID) REFERENCES people(ID)")
    relationships = [i for i in iofile.read.text("relationships", "<#>")]
    print("Populating Table: relationship")
    for i in relationships:
        x = [id(Person.name_lookup(i[j], cols="ID")) for j in range(2)]
        Relationship.add(*x, i[2])

    #sql.table("information", "ID INTERGER PRIMARY KEY AUTOINCREMENT NOT NULL")
    print("Populating Table: information")

    print("\nSetup Complete")

#---Setup----------------------------------------------------------------------#

# us = {i[0][0].lower() : name_lookup(*i, all=False) for i in [("Thomas", "Woolhouse"), ("James", "Meadows"), ("Matthew", "Winter"), ("Alex", "Cooper")]}
# print(us)

#---Main Loop------------------------------------------------------------------#

setup()
#
# encrypt("Orwell")

#---End------------------------------------------------------------------------#
