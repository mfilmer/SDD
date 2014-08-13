# SDD game class

import random

from identifiers import Alignment, Unaligned, Good, Bad
import errors as E

class Player(object):
    def __init__(self, name):
        self._name = name
        self._alignment = Unaligned
        self._isLeader = False
    
    # Setters
    def setAlignment(self, alignment):
        self._alignment = alignment
    
    def setLeader(self, isLeader):
        self._isLeader = bool(isLeader)

class Game(object):
    def __init__(self, setup)__:
        # The game is not yet over
        self._gameOver = False
        
        # Get the set of players and count them
        self._players = set(setup['players'])
        self._nPlayers = len(self._players)
        if not (5 <= self._nPlayers <= 10):
            raise E.InvalidSetup('Must have between 5 and 10 players, inclusive')
        self._nGood = self._nPlayers * 2 // 3
        self._nBad = self._nPlayers - self._nGood
        
        # Set up the teams
        self._bad = set(random.sample(self._players, self._nBad))
        self._good = self._players - self._bad
        
        for player in self._bad:
            player.setAlignment(Bad)
        for player in self._good:
            player.setAlignment(Good)
        
        # Shuffle the players
        self._players = random.sample(self._players)
        
        # Set up the rounds
        self._players[0].setLeader(True)
        
        self._round = 0
        self._nProposedTeams = 0
        if self._nPlayers == 5:
            self._missionSize = [2,3,2,3,3]
            self._failsRequired = [1,1,1,1,1]
        elif self._nPlayers == 6:
            self._missionSize = [2,3,4,3,4]
            self._failsRequired = [1,1,1,1,1]
        elif self._nPlayers == 7:
            self._missionSize = [2,3,3,4,4]
            self._failsRequired = [1,1,1,1,1]
        elif self._nPlayers == 8:
            self._missionSize = [3,4,4,5,5]
            self._failsRequired = [1,1,1,2,1]
        elif self._nPlayers == 9:
            self._missionSize = [3,4,4,5,5]
            self._failsRequired = [1,1,1,2,1]
        elif self._nPlayers == 10:
            self._missionSize = [3,4,4,5,5]
            self._failsRequired = [1,1,1,2,1]
    
    # Getters
    # Returns the round number. 0 <= round <= 4
    def getRound(self):
        return self._round
    
    def getTeamAttempts(self):
        
    
    # Determine if the game is over or not
    def isGameOver(self):
        return self._gameOver