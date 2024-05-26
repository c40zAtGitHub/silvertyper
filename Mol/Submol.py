from __future__ import annotations

from .Interface.MolMatch import MolMatch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Mol import Mol
    from .ObMol import ObMolWrapper
class Submol(MolMatch):
    def __init__(self,
                 parentMol:Mol,
                 subIndices:list[int]):
        self.parent = parentMol
        self._subIndices = subIndices

        #_obmolCache is lazy initialized
        #when .find and .findall method is called
        self._obmolCache:ObMolWrapper = None

    def __getitem__(self,index):
        pindex = self._pindices(index)
        return self.parent.molgraph[pindex]
    
    def __len__(self):
        return len(self._subIndices)

    def _pindices(self,indices:int|list[int]):
        """
        Convert local index to corresponding parent index
        """
        if isinstance(indices,int):
            return self._subIndices[indices]
        elif isinstance(indices,list):
            return [self._subIndices[i] for i in indices]
        else:
            raise ValueError
        
    def _initObmolCache(self):
        subIndices = self._subIndices
        self._obmolCache:ObMolWrapper = self.parent.obmol.submol(subIndices)
        
    def startSmiles(self):
        return self.parent.startSmiles

    def find(self,pattern):
        if self._obmolCache is None:
            self._initObmolCache()
        self._obmolCache.find(pattern)
    
    def findall(self,pattern):
        if self._obmolCache is None:
            self._initObmolCache()
        self._obmolCache.findall(pattern)
