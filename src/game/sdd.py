# SDD game class

import random

from identifiers import Alignment, Unaligned, Good, Bad
from identifiers import State, MakeTeam, VoteTeam, OnMission
import errors as E

class Player(object):
    def __init__(self, name):
        self._name = name
        self._alignment = Unaligned
        self._isLeader = False
        self._game = None
        self._onTeam = False
    
    # Player Actions
    def vote(self, choice):
        self.getGame().vote(self, choice)
    
    def runMission(self, choice):
        self.getGame().runMission(self, choice)
    
    # Setters
    def setGame(self, game):
        if self._game is not None:
            raise Exception('Cannot change the game a player is in')
        else:
            self._game = game
    
    def setAlignment(self, alignment):
        self._alignment = alignment
    
    def setLeader(self, isLeader):
        self._isLeader = bool(isLeader)
    
    def addToTeam(self):
        self._onTeam = True
    
    def removeFromTeam(self):
        self._onTeam = False
    
    # Getters
    def getGame(self):
        return self._game

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
            player.setGame(self)
        for player in self._good:
            player.setAlignment(Good)
            player.setGame(self)
        
        # Shuffle the players
        self._players = random.sample(self._players)
        
        # Set up the rounds
        self._state = MakeTeam
        self._leader = self._players[0]
        self._leader.setLeader(True)
        
        self._round = 0
        self._nProposedTeams = 0
        self._currentTeam = {}
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
    
    # Player Actions
    def addToTeam(self, leader, player):
        if leader is not self._leader:
            raise E.RoleRulesViolation('Only the leader can propose teams')
        else:
            self._currentTeam.add(player)
            player.addToTeam()
    
    def removeFromTeam(self, leader, player):
        if leader is not self._leader:
            raise E.RoleRulesViolation('Only the leader can propose teams')
        else:
            self._currentTeam.remove(player)
            player.removeFromTeam()
    
    def vote(self, player, choice):
        if self._state is not VoteTeam:
            raise E.OutOfOrder
        else:
            if choice not isinstance(TeamVote):
                raise ValueError('Must specify a TeamVote type')
    
    def runMission(self, player, action):
        if self._state is not OnMission:
            raise E.OutOfOrder
        else:
            if choice is not isinstance(MissionBehavior):
                raise ValueError('Must specify a MissionBehavior type')
    
    # Getters
    # Returns the round number. 0 <= round <= 4
    def getRound(self):
        return self._round
    
    # Returns number of attempts at making the team between 0 and 3 inclusive
    def getTeamAttempts(self):
        return self._nProposedTeams
    
    # Determine if the game is over or not
    def isGameOver(self):
        return self._gameOver