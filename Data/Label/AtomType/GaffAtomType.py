from .BaseAtomType import STBaseAtomType

class GAFFAtomType(STBaseAtomType):
    def __init__(self,typeStr = 'X'):
        super().__init__(typeStr)
    
    @property
    def isWildcard(self):
        return (self._type == 'X')