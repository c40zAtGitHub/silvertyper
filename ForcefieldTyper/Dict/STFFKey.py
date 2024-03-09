def compareArray(arr1,arr2):
    result = True
    for pair in zip(arr1,arr2):
        if pair[0] != pair[1]:
            result = False
            break
    return result

class FFAtomType:
    def __init__(self,typeStr):
        self._type = typeStr

    def __hash__(self):
        return hash(self._type)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self._type
    
    def __eq__(self,otherType):
        return self.matches(otherType)
    
    def isExactly(self,otherType):
        #is exactly means NO wildcard match
        return self._type == otherType._type

    def matches(self,otherType):
        if self.isWildcard or otherType.isWildcard:
            return True
        elif self._type == otherType._type:
            return True
        else:
            return False 
    
    @property
    def isWildcard(self):
        #definition of wildcard is forcefield specific
        return False
    
class STFFKey:
    def __init__(self,key):
        #key is a series of symbols connected by dashes ('-')
        keyElements = key.split('-')
        self._elements = tuple([FFAtomType(ele.strip()) for ele in keyElements])
        self._length = len(self._elements)

    def __str__(self):
        return '-'.join([str(ele) for ele in self._elements])

    def __hash__(self):
        return hash(self._elements)

    def __eq__(self,otherkey):
        return self.matches(otherkey)
        
    def __len__(self):
        return self._length
    
    @property
    def hasWildcard(self):
        for ele in self._elements:
            if ele.isWildcard:
                return True
        return False
    
    def isExactly(self,otherkey):
        return self._elements == otherkey._elements
    
    def matches(self,otherkey):
        if self._length == otherkey._length:
            isSame = compareArray(self._elements,otherkey._elements)
            isSameReverse = compareArray(self._elements,reversed(otherkey._elements))
            return isSame or isSameReverse
        else:
            return False