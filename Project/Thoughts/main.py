import table
import sys

def unlock(key):
    table.decrypt(key)
    if table.iofile.read.bin(table.file_name, ext="db")[:6] == b"SQLite":
        return True
    clear()
    return False

def clear():
    table.iofile.write.bin(table.file_name, bytes((0)*len(table.iofile.read.bin(table.file_name, "db"))), ext="db")

class Cmd:
    def __init__(self):
        pass

commands = {
"person": ("list [-i <id>] [-n <name|fname> [-l <lname>]]\n",
"\n\t-i <id>\t\tThe id of the person\n\t-n <name|fname>\tThe full name or first name of the person\n\t-l <lname>\tThe last name of the person"),
"opinion": ("list [-t <id|name>] [-p <id|name>] [-r]\n",
"\n\t-t <id|name>\tThe id|name of the target in the opinion\n\t-p <id|name>\tThe id|name of the person in the opinion\n\t-r\t\tReturn the raw version of the quote without substitution"),
"relationship": ("list [-a <id|name> [-b <id|name>]] [-s <state>]\n",
"\n\t-a <id|name>\tThe id|name of the person A in the relationship\n\t-b <id|name>\tThe id|name of the person B in the relationship\n\t-s <state>\tThe state of the relationship")
}

tags = {None: "Usage: "+sys.argv[0].split("\\")[-1]+" <key> <command> [<args>]\n",
"command": "\n\t"+("\n\t".join(commands)), **{k : "".join(commands[k]) for k in commands}}

def help(*t):
    out = ""
    for i in t:
        if i in tags:
            out += tags[i]
    return out

def main():
    if len(sys.argv) < 3:
        quit(help(None, "command"))
    elif not unlock(sys.argv[1]):
        quit("Key: '{}' is incorrect!".format(sys.argv[1]))

main()

# unlock("Orwell")

# table.encrypt("Orwell")
# table.backup()
