from .BaseAtomType import BaseAtomType

class GAFFAtomType(BaseAtomType):
    def __init__(self,typeStr = 'X'):
        super().__init__(typeStr)
    
    @property
    def isWildcard(self):
        return (self._type == 'X')
    
    def match(self,otherType):
        if otherType == 'X':
            return True
        else:
            return super().match(otherType)