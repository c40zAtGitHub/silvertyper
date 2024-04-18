"""
Entries used to describe badi
"""
from ..BaseDataEntry import BaseDataEntry

class TwoAtomEntry(BaseDataEntry):
    def __init__(self,etype,
                 atom1,atom2):
        super().__init__(etype)
        self.atom1 = atom1
        self.atom2 = atom2

    def __iter__(self):
        yield from super().__iter__()
        yield self.atom1
        yield self.atom2
    
class ThreeAtomEntry(BaseDataEntry):
    def __init__(self,etype,
                 atom1,atom2,atom3):
        super().__init__(etype)
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
    
    def __iter__(self):
        yield from super().__iter__()
        yield self.atom1
        yield self.atom2
        yield self.atom3
    
class FourAtomEntry(BaseDataEntry):
    def __init__(self,etype,
                 atom1,atom2,atom3,atom4):
        super().__init__(etype)
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.atom4 = atom4

    def __iter__(self):
        yield from super().__iter__()
        yield self.atom1
        yield self.atom2
        yield self.atom3
        yield self.atom4
