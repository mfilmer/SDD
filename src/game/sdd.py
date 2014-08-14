# SDD game class

import random
from collections import Counter

from identifiers import Alignment, Unaligned, Good, Bad
from identifiers import State, MakeTeam, VoteTeam, OnMission
from identifiers import TeamVote, Approve, Reject
from identifiers import MisisonBehavior, Pass, Fail
from identifiers import VictoryReason, ThreeMissions, FiveRejectedTeams
import errors as E

class Player(object):
    def __init__(self, name):
        self._name = name
        self._alignment = Unaligned
        self._isLeader = False
        self._game = None
        self._onTeam = False
        self._currentVote = None
    
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

class Game(object):
    def __init__(self, setup)__:
        # The game is not yet over
        self._victory = None
        # Outcome of each mission
        self._missionHistory =
                [Unaligned, Unaligned, Unaligned, Unaligned, Unaligned]
        
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
        self._advanceLeader()
        
        self._round = 0
        self._nProposedTeams = 0
        self._currentTeam = {}
        self._submittedVotes = {}
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
        if self._state is not MakeTeam:
            raise E.OutOfOrder('Cannot make a team at this time')
        if leader is not self._leader:
            raise E.RoleRulesViolation('Only the leader can propose teams')
        if len(self._currentTeam) >= self._missionSize[self._round]:
            raise E.TeamSizeError
        self._currentTeam.add(player)
        player.addToTeam()
        self.onTeamChange(self._currentTeam)
    
    def removeFromTeam(self, leader, player):
        if self._state is not MakeTeam:
            raise E.OutOfOrder('Cannot make a team at this time')
        if leader is not self._leader:
            raise E.RoleRulesViolation('Only the leader can propose teams')
        self._currentTeam.remove(player)
        player.removeFromTeam()
        self.onTeamChange(self._currentTeam)
    
    def finalizeTeam(self, leader):
        if self._state is not MakeTeam:
            raise E.OutOfOrder('Cannot make a team at this time')
        if leader is not self._leader:
            raise E.RoleRulesViolation('Only the leader can finalize a team')
        if len(self._currentTeam) != self._missionSize[self._round]
            raise E.TeamSizeError
        self._setState(VoteTeam)
    
    def vote(self, player, choice):
        if self._state is not VoteTeam:
            # Now is not the time to vote on a team
            raise E.OutOfOrder('Now is not the time to vote on a team')
        if choice is None:
            # The player is retracting their vote
            self._submittedVotes.remove(player)
            return
        if choice not isinstance(TeamVote):
            raise ValueError('Must specify a TeamVote type')
        self._submittedVotes.add(player)
        
        # If not everyone has voted, then we continue to wait
        if len(self._submittedVotes) != self._nPlayers:
            return
        
        # Tally the votes
        voteCount = Counter(p.getVote() for p in self._submittedVotes)
        self._submittedVotes = {}
        if voteCount[Approve] > voteCount[Reject]:
            # Team vote passes. Move on to the mission
            self._setState(OnMission)
        else:
            # Team vote fails
            self._nProposedTeams += 1
            if self._nProposedTeams == 5:
                # Bad team wins
                self._victory = Bad
                self._victoryReason = FiveRjectedTeams
                return
            self._advanceLeader()
    
    def submitMisisonAction(self, player, action):
        if self._state is not OnMission:
            raise E.OutOfOrder
        if player not in self._currentTeam
        if choice is not isinstance(MissionBehavior):
            raise ValueError('Must specify a MissionBehavior type')
    
    # Internal actions
    def _advanceRound(self):
        self._round += 1
        self._advanceLeader()
        self._nProposedTeams = 0
        self._currentTeam = {}
        self._setState(MakeTeam)
        self.onNewRound(self._round)
    
    def _advanceLeader(self):
        self._leader.setLeader(False)
        tmp = self._players.pop(0)
        self._players.add(tmp)
        self._leader = self._players(0)
        self._leader.setLeader(True)
        self.onNewLeader(self._leader)
    
    def _setState(self, newState):
        self._state = newState
        self.onStateChange(newState)
    
    # Abstract methods that can be modified in a subclass
    def onTeamChange(self, team):
        return
    
    def onNewLeader(self, leader):
        return
    
    def onStateChange(self, newState):
        return
    
    def onNewRound(self, roundNumber):
        return
    
    # Getters
    # Returns the round number. 0 <= round <= 4
    def getRound(self):
        return self._round
    
    # Returns number of attempts at making the team between 0 and 3 inclusive
    def getTeamAttempts(self):
        return self._nProposedTeams
    
    def getState(self):
        return self._state
    
    # Determine if the game is over or not
    def isGameOver(self):
        return self._victory is not None