from identifiers import Alignment, Good, Bad

class Role(object):
    pass

##### Good Guys #####
# Basic good guy
class LoyalServant(Role):
    _team = Good

# Knows the bad guys
class Oracle(Role):
    _team = Good

# Knows both the Oracle and the Chameleon,
# but not which is which
class Apprentice(Role):
    _team = Good

##### Bad Guys #####
# Basic bad guy
class EvilMinion(Role):
    _team = Bad

# Unknown to the Oracle
class MasterOfDisguise(Role):
    _team = Bad

# Known to the Apprentice
class Chameleon(Role)
    _team = Bad

# Does not know the other bad guys
class Fool(Role):
    _team = Bad