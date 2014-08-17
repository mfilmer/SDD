# SDD game class

import random
from collections import Counter

from identifiers import Alignment, Unaligned, Good, Bad \
                       ,State, MakeTeam, VoteTeam, OnMission, GameOver \
                       ,TeamVote, Approve, Reject \
                       ,MissionBehavior, Pass, Fail \
                       ,VictoryReason, WinThreeMissions, FiveRejectedTeams
import roles as R
import errors as E
from player import Player

class Game(object):
    def __init__(self, setup):
        # Game setup phase
        self._state = CreateGame
        # The game is not yet over
        self._victory = Unaligned
        # Outcome of each mission
        self._missionHistory = \
                [Unaligned, Unaligned, Unaligned, Unaligned, Unaligned]
        
        # Create the list of players
        self._players = []
        self._nPlayers = setup['nPlayers']
        if not (5 <= self._nPlayers <= 10):
            raise E.InvalidSetup('Must have between 5 and 10 players, inclusive')
        self._nGood = self._nPlayers * 2 // 3
        self._nBad = self._nPlayers - self._nGood
        
        # Set up the roles
        self._unallocatedRoles = setup['roles']
        nBadRoles = len(x for x in self._unallocatedRoles if x._team is Bad)
        nGoodRoles = len(self._unallocatedRoles) - nBadRoles
        if nBadRoles > self._nBad:
            raise E.InvalidSetup('Too many roles for the bad team')
        if nGoodRoles > self._nGood:
            raise E.InvalidSetup('Too many roles for the good team')
        self._unallocatedRoles.extend((self._nBad - nBadRoles)*[R.EvilMinion])
        self._unallocatedRoles.extend((self._nGood - nGoodRoles)*[R.LoyalServant])
        
        # Randomize the roles
        random.shuffle(self._unallocatedRoles)
        
        # Set up the rounds
        self._round = 0
        self._nProposedTeams = 0
        self._currentTeam = {}
        self._submittedVotes = {}
        self._submittedActions = {}
        self._actionsCounter = Counter()
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
    
    def playerJoin(self, newPlayer):
        if any(p.getName() == newPlayer.getName() for p in self._players):
            raise E.InvalidSetup('Name {} already taken'.format(newPlayer.getName()))
        newPlayer.setGame(self)
        self._players.add(newPlayer)
        
        # Check if game is startable
        if len(self._players) == self._nPlayers:
            self._startGame()
    
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
        if len(self._currentTeam) != self._missionSize[self._round]:
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
        if not isinstance(choice, TeamVote):
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
                self._victoryReason = FiveRejectedTeams
                self.onGameOver(Bad, FiveRejectedTeams)
                return
            self._advanceLeader()
    
    def submitMisisonAction(self, player, action):
        if self._state is not OnMission:
            raise E.OutOfOrder
        if player not in self._currentTeam:
            raise RoleRulesViolation('Not on current team')
        if not isinstance(action, MissionBehavior):
            raise ValueError('Must specify a MissionBehavior type')
        if player in self._submittedActions:
            raise IlegalPlay('Action already submitted')
        if action is Fail and player.getAlignment is Good:
            raise E.RoleRulesViolation('Only bad guys can fail missions')
        self._submittedActions.add(player)
        self._actionCounter[action] += 1
        self.onActionSubmitted(player)
        if len(self._submittedActions) < len(self._currentTeam):
            # Wait for more players to submit actions
            return
        
        # Mission done, determine the outcome of the mission
        if self._actionCounter[Fail] >= self._failsRequired[self._round]:
            # Bad guys get a point
            roundWinner = Bad
        else:
            # Good guys get a point
            roundWinner = Good
        self._missionHistory[self._round] = roundWinner
        self.onMissionComplete(self, roundWinner, self._actionCounter)
        
        # Check if there is a winner
        missionCount = Counter(self._missionHistory)
        if missionCount[roundWinner] != 3:
            # Next round
            self._advanceRound()
            return
        
        self._victory = roundWinner
        self._victoryReason = WinThreeMissions
        self.onGameOver(roundWinner, WinThreeMissions)
    
    # Internal actions
    def _startGame(self):
        random.shuffle(self._players)
        self._leader = self._players[0]
        self._leader.setLeader(True)
        self._state = MakeTeam
        self.onGameStart(self._leader)
    
    def _advanceRound(self):
        self._round += 1
        self._advanceLeader()
        self._nProposedTeams = 0
        self._currentTeam = {}
        self._setState(MakeTeam)
        self._submittedActions = {}
        self._actionCounter = Counter()
        self.onNewRound(self._round)
    
    def _advanceLeader(self):
        self._leader.setLeader(False)
        tmp = self._players.pop(0)
        self._players.append(tmp)
        self._leader = self._players[0]
        self._leader.setLeader(True)
        self.onNewLeader(self._leader)
    
    def _setState(self, newState):
        self._state = newState
        self.onStateChange(newState)
    
    # Abstract methods to be modified in a subclass
    def onGameStart(self, leader):
        return
    
    # Any time the leader changes who is on the team
    def onTeamChange(self, team):
        return
    
    def onNewLeader(self, leader):
        return
    
    def onStateChange(self, newState):
        return
    
    def onNewRound(self, roundNumber):
        return
    
    def onActionSubmitted(self, actionSubmitter):
        return
    
    def onMissionComplete(self, team, tally):
        return
    
    def onGameOver(self, winner, reason):
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
        return self._victory is not Unaligned