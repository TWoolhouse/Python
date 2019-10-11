import libs
import node
from tags import Tag

IP = "109.156.73.196"

#---Menus---------------------------------------------------------------------#

def type_input(msg: str, Type: type=int, empty=False) -> type:
    while True:
        try:
            value = input("\n"+msg+"\n")
            if empty and not value:
                return None
            return Type(value)
        except ValueError:
            print("Please enter a valid '{}'\n\n".format(Type.__name__))

def menu(*options, ret=False):
    return "Enter a Number:\n" + "\n".join(("{}) {}".format(i, m.replace("_", " ").title()) for i, m in enumerate(options, start=1))) + ("\n\n0) Return" if ret else "")

def m_name(client):
    fname, lname = None, None
    while True:
        user_input = type_input(menu("Lookup", *("{} -> {}".format(n, v) for v,n in zip((fname, lname), ("First", "Last"))), ret=True))
        if user_input == 0:
            break
        elif user_input == 1:
            res = c_name(client, fname, lname)
            print("\n#-------Results-------#\n\n{}\n\n#---------------------#".format("No Values Found!" if not res else "\n".join(res)))
        elif user_input == 2:
            fname = type_input("Please enter the first name:", str, True)
        elif user_input == 3:
            lname = type_input("Please enter the last name:", str, True)

def m_info(client):
    tags = list(Tag.tags.keys())
    name, tag, value = None, None, None
    while True:
        user_input = type_input(menu("Lookup", *("{} -> {}".format(n, v) for v,n in zip((name, tag, value), ("Name", "Tag", "Value"))), ret=True))
        if user_input == 0:
            break
        elif user_input == 1:
            res = c_info(client, name, tag, value)
            print("\n#-------Results-------#\n\n{}\n\n#---------------------#".format("No Values Found!" if not res else "\n".join(res)))
        elif user_input == 2:
            name = type_input("Please enter a name:", str, True)
        elif user_input == 3:
            val = type_input(menu(*tags), empty=True)
            if val:    tag = tags[abs(val - 1)]
            else:    tag, value = None, None
        elif user_input == 4:
            if tag is not None:
                ttags = [t.name for t in Tag(tag)]
                val = type_input(menu(*ttags), empty=True)
                value = ttags[abs(val - 1)] if val else val
            else:
                print("\nPlease enter a 'Tag' first")

def m_birthday(client):
    name, year, month, day = None, None, None, None
    while True:
        user_input = type_input(menu("Lookup", *("{} -> {}".format(n, v) for v,n in zip((name, year, month, day), ("Name", "Year", "Month", "Day"))), ret=True))
        if user_input == 0:
            break
        elif user_input == 1:
            res = c_birthday(client, name, year, month, day)
            print("\n#-------Results-------#\n\n{}\n\n#---------------------#".format("No Values Found!" if not res else "\n".join(res)))
        elif user_input == 2:
            name = type_input("Please enter a name:", str, True)
        elif user_input == 3:
            year = type_input("Please enter a Year: (YYYY)", empty=True)
        elif user_input == 4:
            month = type_input("Please enter a Month: (MM)", empty=True)
        elif user_input == 5:
            day = type_input("Please enter a Day: (DD)", empty=True)

menu_options = [m_name, m_info, m_birthday]

#---Client-------------------------------------------------------------------#

def c_recv(client: node.Client, prefix="data"):
    length = int(client.data("length", res=True)[0][1])
    data = []
    while len(data) < length:
        data.extend((i[1] for i in client.data("lk"+prefix)))
    return data

def c_repopulate(client: node.Client):
    client.cmd("s_repopulate")
    client.data("repopulate", res=True)

def c_name(client: node.Client, fname: str=None, lname: str=None):
    client.cmd("s_name", fname, lname)
    return c_recv(client, "name")

def c_info(client: node.Client, name: str=None, tag: str=None, value: str=None):
    client.cmd("s_info", name, tag, value)
    return c_recv(client, "info")

def c_birthday(client: node.Client, name: str=None, year: int=None, month: int=None, day: int=None):
    client.cmd("s_birthday", name, "-".join(("0"*(l - len(str(i))) + str(i) if i is not None else "_"*l for i,l in zip((year, month, day), (4, 2, 2)))))
    return c_recv(client, "birthday")

#---Main----------------------------------------------------------------------#

client = node.Client(addr=IP, port=53337, password="Orwell", encrypt=69420)
with client:
    while True:
        user_input = type_input(menu(*(m.__name__[2:] for m in menu_options), ret=True))
        if user_input == 0:
            break
        menu_options[abs(user_input - 1)](client)
