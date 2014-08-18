import json

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol

class Client(Protocol):
    def sendMessage(self, message):
        self.transport.write(message)
    
class ClientFactory(ClientFactory):
    def startedConnectiong(self, connector):
        print 'Started to connect'
    
    def buildProtocol(self, addr):
        print 'Connected'
        return Client()
    
    def clientConnectionLost(self, connector, reason):
        print 'Lost connection. Reason: {}'.format(reason)
    
    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason: {}'.format(reason)
    
def gotProtocol(p):
    p.sendMessage('sup?')
    p.transport.loseConnection()

reactor.connectTCP("localhost", 5004, ClientFactory())
reactor.run()
