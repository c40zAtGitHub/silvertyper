class BaseAtomType:
    def __init__(self,typeStr):
        self._type = typeStr

    def __hash__(self):
        return hash(self._type)

    def __str__(self):
        return self._type
    
    def __eq__(self,otherType):
        return self.match(otherType)
    
    def isExactly(self,otherType):
        #is exactly means NO wildcard match
        return self._type == otherType._type

    def match(self,otherType):
        if self.isWildcard:
            return True
        
        if isinstance(otherType,BaseAtomType):
            if otherType.isWildcard:
                return True     
            elif self._type == otherType._type:
                return True
            
        elif isinstance(otherType,str):
            if self._type == otherType:
                return True
        else:
            return False 
    
    @property
    def isWildcard(self):
        #definition of wildcard is forcefield specific
        return False