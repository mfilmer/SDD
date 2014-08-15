# SDD player class

from identifiers import Unaligned

class Player(object):
    def __init__(self, name):
        self._name = name
        self._alignment = Unaligned
        self._isLeader = False
        self._game = None
        self._onTeam = False
        self._currentVote = None
    
    def __str__(self):
        return 'Player: {}'.format(self._name)
    
    def __repr__(self):
        return 'player({})'.format(self._name)
    
    # Player Actions
    def vote(self, choice):
        self.getGame().vote(self, choice)
        self._currentVote = choice
    
    def retractVote(self):
        self.getGame().vote(self, None)
        self._currentVote = None
    
    def submitMissionAction(self, choice):
        self.getGame().submitMissionAction(self, choice)
    
    def finalizeTeam(self):
        self.getGame().finalizeTeam(self)
    
    # Setters
    def setGame(self, game):
        if self._game is not None:
            raise Exception('Cannot change the game a player is in')
        else:
            self._game = game
    
    def setAlignment(self, alignment):
        self._alignment = alignment
        self.onAlignmentChange(alignment)
    
    def setLeader(self, isLeader):
        self._isLeader = bool(isLeader)
        if self._isLeader:
            self.onBecomeLeader()
        else:
            self.onLoseLeader()
    
    def addToTeam(self):
        self._onTeam = True
        self.onJoinTeam()
    
    def removeFromTeam(self):
        self._onTeam = False
        self.onLeaveTeam()
    
    # Getters
    def getGame(self):
        return self._game
    
    def getVote(self):
        return self._currentVote
    
    def getAlignment(self):
        return self._alignment
    
    # Abstract methods to be implemented in subclasses
    def onBecomeLeader(self):
        return
    
    def onLoseLeader(self):
        return
    
    def onJoinTeam(self):
        return
    
    def onLeaveTeam(self):
        return
    
    def onAlignmentChange(self, alignment):
        return