# Singleton Identifiers
class Single(object):
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return self._name

class Alignment(Single):
    pass
Unaligned = Alignment('Unaligned')
Good = Alignment('Good')
Bad = Alignment('Bad')

class State(Single):
    pass
MakeTeam = State('MakeTeam')
VoteTeam = State('VoteTeam')
OnMission = State('OnMission')
GameOver = State('GameOver')

class TeamVote(Single):
    pass
Approve = TeamVote('Approve')
Reject = TeamVote('Reject')

class MissionBehavior(Single):
    pass
Pass = MissionBehavior('Pass')
Fail = MissionBehavior('Fail')

# Reason the winning team won
class VictoryReason(Single):
    pass
ThreeMissions = VictoryReason('WinThreeMissions')
FiveRejectedTeams = VictoryReason('FiveRejectedTeams')