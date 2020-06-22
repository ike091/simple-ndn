import time
from pyndn import Name
from pyndn import Face
from pyndn import Interest
from pyndn.transport import UdpTransport
from pyndn.security import KeyChain

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


    def onNetworkNack(self, interest, networkNack):
        self._callbackCount += 1
        dump("Network nack for interest", interest.getName().toUri())


def main():

    # silence the warning from interest wire encode
    Interest.setDefaultCanBePrefix(True)

    # set up a face that connects to the remote forwarder
    udp_connection_info = UdpTransport.ConnectionInfo("10.10.1.1")
    udp_transport = UdpTransport()
    face = Face(udp_transport, udp_connection_info)
    #  face.setCommandSigningInfo(KeyChain(), certificateName)
    #  face.registerPrefix(Name("/ndn"), onInterest, onRegisterFailed)

    #  face = Face("10.10.1.1")

    counter = Counter()

    # try to fetch from provided name
    name_text = input("Enter a name to request content from: ")
    name = Name(name_text)
    dump("Express name", name.toUri())
    face.expressInterest(name, counter.onData, counter.onTimeout, counter.onNetworkNack)

    # try to fetch anything
    #  name2 = Name("/")
    #  dump("Express name", name2.toUri())
    #  face.expressInterest(name2, counter.onData, counter.onTimeout, counter.onNetworkNack)


    while counter._callbackCount < 1:
        face.processEvents()

        # don't use 100% of the CPU
        time.sleep(0.01)

    face.shutdown()


main()

