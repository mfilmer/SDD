from identifiers import Alignment, Good, Bad

class Role(object):
    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name

##### Good Guys #####
# Basic good guy
class LoyalServant(Role):
    _team = Good
    _name = 'Loyal Servant'

# Knows the bad guys
class Oracle(Role):
    _team = Good
    _name = 'Oracle'

# Knows both the Oracle and the Chameleon,
# but not which is which
class Apprentice(Role):
    _team = Good
    _name = 'Apprentice'

##### Bad Guys #####
# Basic bad guy
class EvilMinion(Role):
    _team = Bad
    _name = 'Evil Minion'

# Unknown to the Oracle
class MasterOfDisguise(Role):
    _team = Bad
    _name = 'Master Of Disguise'

# Known to the Apprentice
class Chameleon(Role):
    _team = Bad
    _name = 'Chameleon'

# Does not know the other bad guys
class Fool(Role):
    _team = Bad
    _name = 'Fool'