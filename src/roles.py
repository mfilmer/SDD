from identifiers import Alignment, Good, Bad

class Role(object):
    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name
    
    # Abstract methods
    def gameStart(self, game):
        pass

##### Good Guys #####
# Basic good guy
class LoyalServant(Role):
    _team = Good
    _name = 'Loyal Servant'

# Knows the bad guys
class Oracle(Role):
    _team = Good
    _name = 'Oracle'
    
    def gameStart(self, game):
        self._badGuys = [p for p in game._players if p.getAlignment() is Bad and not isinstance(p._role, MasterOfDisguise)]

# Knows both the Oracle and the Chameleon,
# but not which is which
class Apprentice(Role):
    _team = Good
    _name = 'Apprentice'
    
    def gameStart(self, game):
        self._oracle = [p for p in game._players if isinstance(p._role, (Oracle, Chameleon))]

##### Bad Guys #####
# Basic bad guy
class EvilMinion(Role):
    _team = Bad
    _name = 'Evil Minion'
    
    def gameStart(self, game):
        self._badGuys = [p for p in game._players if p.getAlignment() is Bad]

# Unknown to the Oracle
class MasterOfDisguise(Role):
    _team = Bad
    _name = 'Master Of Disguise'
    
    def gameStart(self, game):
        self._badGuys = [p for p in game._players if p.getAlignment() is Bad]

# Known to the Apprentice
class Chameleon(Role):
    _team = Bad
    _name = 'Chameleon'
        
    def gameStart(self, game):
        self._badGuys = [p for p in game._players if p.getAlignment() is Bad]

# Does not know the other bad guys
class Fool(Role):
    _team = Bad
    _name = 'Fool'