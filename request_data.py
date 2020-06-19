import time
from pyndn import Name
from pyndn import Face
from pyndn import Interest


def dump(*list):
    """Prints all parameters"""

    result = ""
    for element in list:
        result += (element if type(element) is str else str(element)) + " "
    print(result)
    


class Counter():
    
    def __init__(self):
        self._callbackCount = 0

    
    def onData(self, interest, data):
        self._callbackCount += 1
        dump("Got data packet with name", data.getName().toUri())
        dump(data.getContent().toRawStr())


    def onTimeout(self, interest):
        self._callbackCount += 1
        dump("Time out for interest", interest.getName().toUri())


def main():

    # silence the warning from interest wire encode
    Interest.setDefaultCanBePrefix(True)

    # the default face will connect using a Unix socket, or go to "localhost"
    face = Face()

    counter = Counter()

    word = input("Enter a word to echo: ")
    
    name = Name("/testecho")
    name.append(word)
    dump("Express name", name.toUri())
    face.expressInterest(name, counter.onData, counter.onTimeout)

    while counter._callbackCount < 1:
        face.processEvents()

        # don't use 100% of the CPU
        time.sleep(0.01)

    face.shutdown()


main()

