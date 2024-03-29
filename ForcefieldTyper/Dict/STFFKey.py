from .STFFAtomTypeLabel import STFFAtomTypeLabel as AtomTypeLabel

def compareArray(arr1,arr2):
    result = True
    for pair in zip(arr1,arr2):
        if pair[0] != pair[1]:
            result = False
            break
    return result
    
class STFFKey:
    def __init__(self,keyElements,Label = AtomTypeLabel):
        self._Label = Label
        self._elements = tuple([self._Label(ele.strip()) for ele in keyElements])
        self._length = len(self._elements)
        
    def __str__(self):
        return '-'.join([str(ele) for ele in self._elements])

    def __hash__(self):
        return hash(self._elements)

    def __eq__(self,otherkey):
        return self.match(otherkey)
        
    def __len__(self):
        return self._length
    
    @classmethod
    def fromString(cls,string):
        """
        Construct STFFKey instances from strings
        like "a-b-c-d"
        """
        atomTypesStrs = string.split('-')
        newKey = cls(atomTypesStrs)
        return newKey
    
    @property
    def hasWildcard(self):
        for ele in self._elements:
            if ele.isWildcard:
                return True
        return False
    
    def isExactly(self,otherkey):
        return self._elements == otherkey._elements
    
    def match(self,otherkey):
        if self._length == otherkey._length:
            isSame = compareArray(self._elements,otherkey._elements)
            isSameReverse = compareArray(self._elements,reversed(otherkey._elements))
            return isSame or isSameReverse
        else:
            return False