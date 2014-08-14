# Errors

# When there are errors in the setup
class InvalidSetup(Error):
    pass
# General purpose illegal play exception. Other exceptions are derived from
# this one
class IllegalPlay(Error):
    pass
# TeamSizeError is for proposed teams of the wrong size for the current round
class TeamSizeError(IllegalPlay):
    pass
# OutOfOrder is for players doing things at the wrong time. Such as voting on a
# team while the mission is running
class OutOfOrder(IllegalPlay):
    pass
# RoleRulesViolation is for things like good guys failing a mission
class RoleRulesViolation(IllegalPlay):
    pass
# GameIsOver is used when the game is over and yet plays are trying to be made
class GameIsOver(IllegalPlay):
    pass