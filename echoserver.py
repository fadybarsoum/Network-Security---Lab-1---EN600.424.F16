from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from datetime import datetime as dt

class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("<" +dt.now().isoformat()+ "> Connection Made")

    def connectionLost(self, reason):
        print("<" +dt.now().isoformat()+ "> Connection Lost")

    def dataReceived(self, data):
        print("<" +dt.now().isoformat()+ "> Received: " + data)
        self.transport.write(data)

class EchoFactory(Factory):
    def buildProtocol(self, addr):
        return Echo(self)

endpoint = TCP4ServerEndpoint(reactor, 1337)
endpoint.listen(EchoFactory())
reactor.run()
