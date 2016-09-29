from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import connectProtocol
from twisted.internet.protocol import ReconnectingClientFactory
import sys
sys.path.append("/home/fady/Documents/PlayGround/firsttest/src/")
import playground
from playground.twisted.endpoints import GateServerEndpoint, GateClientEndpoint

class FadyHTTPProtocol(Protocol):
    def sendMessage(self, msg):
        print("Sending: \r\n" + msg)
        self.transport.write(msg)

    def dataReceived(self, data):
        bodyindex = data.find("\r\n\r\n")+4
        print("Received: \r\n" + data[bodyindex:])
        self.transport.loseConnection()

class FadyHTTPClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('Connected.')
        print('Resetting reconnection delay')
        self.resetDelay()
        return FadyHTTPProtocol()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        print('Attempting to reconnect...')
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

def gotProtocol(p):
    request = ("GET " + sys.argv[1] + " HTTP/1.0\r\n" +
               "Host: localhost\r\n\r\n")
    p.sendMessage(request)

if len(sys.argv) < 2:
    print("No arguments given. Quitting...")
else:
    point = GateClientEndpoint.CreateFromConfig(reactor, "20164.0.17.221", 80, "gatekey00")
    d = connectProtocol(point, FadyHTTPProtocol())
    d.addCallback(gotProtocol)
    reactor.run()
