from ForcefieldTyper.STFFKey import FFAtomType

class GAFFAtomType(FFAtomType):
    def __init__(self,typeStr = 'X'):
        super().__init__(typeStr)
    
    @property
    def isWildcard(self):
        return (self._type == 'X')