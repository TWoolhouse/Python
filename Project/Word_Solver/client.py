import libs
import node

class VALID(node.Dispatch, output=True):

    def handle(self):
        data = self.node.recv("VALID", wait=int(self.data.data))
        words = []
        for w in data:
            words.append(w.data)
        return words

client = node.Client("192.168.1.105", 80, dispatchers=(,))

with client:
    while True:
        string = input("Please enter a word:\n")
        if not string:
            break
        client.send(string, "VALID")
