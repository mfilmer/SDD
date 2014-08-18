import json

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from game import Game
from player import Player

class State(object):
    pass
GetName = State()

class TheGame(Game):
    pass

class PlayerConnection(LineReceiver):
    def __init__(self, users):
        self._state = GetName
        
        self._users = users
        
        self._name = None
    
    def connectionMade(self):
        self.sendLine(json.dumps({'request':'PlayerName'}))
    
    # Eventually wait for the player to reconnect
    def connectionLost(self, reason):
        pass
    
    def lineReceived(self, line):
        if self._state is GetName:
            self._name = json.loads(line)['PlayerName']

class PlayerFactory(Factory):
    def __init__(self):
        self._players = {}
    
    def buildProtocol(self, addr):
        return PlayerConnection(self._players)

reactor.listenTCP(5004, PlayerFactory())
reactor.run()
