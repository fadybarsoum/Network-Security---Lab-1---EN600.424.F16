from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from datetime import datetime as dt
from twisted.web.http import HTTPFactory

class FadyHTTPProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("<" +dt.now().isoformat()+ "> Connection Made")

    def connectionLost(self, reason):
        print("<" +dt.now().isoformat()+ "> Connection Lost")

    def dataReceived(self, data):
        print("<" +dt.now().isoformat()+ "> Received: \n" + data)
        if not data.startswith("GET"):
            print("Badly formatted request 1: ignoring it")
            return
        getloc = data.find("GET")
        firstlineend = data.find("\r\n")
        firstline = data[:firstlineend]
        if not (firstline.endswith("HTTP/1.1") or firstline.endswith("HTTP/1.0")):
            print("Badly formatted request 2: ignoring it")
            return
        docname = firstline[4:firstlineend-9]
        redirect_flag = False
        if "." not in docname and not docname.endswith("/"):
            docname += "/"
        if not docname.startswith("/"):
            docname = "/" + docname
        if docname.endswith("/"):
            docname += "index.html"
            redirect_flag = True
        print("Client requested file: " + docname)
        responsecode = "200 OK"
        try:
            doc = open("./webcontents" + docname,'r')
        except IOError:
            print("Error finding this document. Sending a 404...")
            responsecode = "404 Not Found"
            docname = "/404.html"
            doc = open("./webcontents" + docname,'r')
        doccontents = doc.read()
        docsize = len(doccontents) + 4
        response = ("HTTP/1.0 " + responsecode + "\r\n" +
                    "Date: " + dt.now().ctime() + "\r\n" +
                    "Server: Twisted/1.6.4 (Fady Custom)\r\n" +
                    "Content-Type: text/html\r\n" +
                    "Content-Length: " + str(docsize) + "\r\n" +
                    "Connection: Closed\r\n\r\n" +
                    "" + doccontents + "\r\n\r\n")
        print(response)
        self.transport.write(response)
        self.transport.loseConnection()
                                 
                                 
                

class FadyHTTPFactory(HTTPFactory):
    def buildProtocol(self, addr):
        return FadyHTTPProtocol(self)

endpoint = TCP4ServerEndpoint(reactor, 80)
endpoint.listen(FadyHTTPFactory())
reactor.run()
