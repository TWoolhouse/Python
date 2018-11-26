from src import network

#---Global Variables-----------------------------------------------------------#

ns = network.Server()
commands = ["help", "quit", "close", "open", "update", "users"]

#---Classes--------------------------------------------------------------------#

#---Functions------------------------------------------------------------------#

def c_help():
    return "Commands: "+", ".join(commands)

def c_close():
    ns.close()
    return "Closed Server"

def c_open():
    if network.options["allowed"]:
        ns.open()
        return "Opened Server"
    return "Failed - Error Ocurred"

def c_quit():
    quit()

def c_update():
    ns.update_options()
    return "Updated Options"

def c_users():
    return "Connections:\n\t"+"\n\t".join(["{} [{}]".format(key, ns.connections[key].addr) for key in ns.connections])

#---Setup----------------------------------------------------------------------#

#---Main Loop------------------------------------------------------------------#

try:
    while True:
        user_input = input(">>> ").lower()
        try:
            print(globals()["c_"+user_input]())
        except KeyError:
            print("Command Not Found. Try \"help\" for a list of commands")
except (SystemExit, KeyboardInterrupt):
    pass

#---End------------------------------------------------------------------------#

print("Server Shuting Down")
ns.close()
