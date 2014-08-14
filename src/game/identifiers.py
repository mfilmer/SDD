# Singleton Identifiers
class Alignment(object):
    pass
Unaligned = Role()
Good = Role()
Bad = Role()

class State(object):
    pass
MakeTeam = State()
VoteTeam = State()
OnMission = State()

class TeamVote():
    pass
Approve = TeamVote()
Reject = TeamVote()

class MissionBehavior(object):
    pass
Pass = MissionBehavior()
Fail = MissionBehavior()

# Reason the winning team won
class VictoryReason(object):
    pass
ThreeMissions = VictoryReason()
FiveRejectedTeams = VictoryReason()