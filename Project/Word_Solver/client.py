import libs
import node

class VALID(node.Dispatch, output=True):

    def handle(self):
        data = self.node.recv("VALID", wait=True)[0].data
        words = data.split("|")
        self.data.tags.append("RESULT")
        return words

client = node.Client("192.168.1.105", 80, dispatch=(VALID,))

with client:
    while True:
        string = input("Please enter a word:\n")
        if not string:
            break
        client.send(string, "VALID")
        data = client.recv("VALID", node.Tag("RESULT"), wait=True)[0].data
        print("Words: {} -> <{}>:".format(string, len(data)))
        print("\n".join((str(i)+") "+j for i,j in enumerate(data, start=1))))
