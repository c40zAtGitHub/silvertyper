from silvertyper.ForcefieldTyper.Dict.STFFAtomTypeLabel import STFFAtomTypeLabel

class GAFFAtomTypeLabel(STFFAtomTypeLabel):
    def __init__(self,typeStr = 'X'):
        super().__init__(typeStr)
    
    @property
    def isWildcard(self):
        return (self._type == 'X')