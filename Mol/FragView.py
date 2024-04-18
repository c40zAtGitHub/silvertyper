from __future__ import annotations

from .OBInterface.OBMolSync import OBMolSyncronizer

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Mol.Fragment import Fragment

class FragView:
    """
    Fragment View class
    A "view" of a Fragment class
    """
    def __init__(self,parent:Fragment,
                 atomIndices):
        self.parent = parent
        self._indices = atomIndices
        self._vmol = None

    def __getitem__(self,index):
        pIndex = self._indices[index]
        return self.parent[pIndex]
    
    def __len__(self):
        return len(self._indices)

    def matchFrag(self,otherFrag):
        return self.vmol.matchFrag(otherFrag)
    
    def matchSmiles(self,smilesPattern,parentIndex = False):
        indices = self.vmol.matchSmiles(smilesPattern)
        if parentIndex is True:
            return [self.pindex[i] for i in indices]
        else:
            return indices
    
    @property
    def molgraph(self):
        return self.parent.molgraph
    
    @property
    def obmol(self):
        return self.parent.obmol
    
    @property
    def pindex(self):
        return self._indices
    
    def toMol(self):
        return self.parent.subFrag(self._indices)
    
    @property
    def vmol(self):
        if self._vmol is None:
            self._vmol = self.toMol()
        return self._vmol
    
    def syncVmol(self):
        #sync obmol
        #sync bond connection and order
        syncronizer = OBMolSyncronizer(self.vmol.obmol,                 #srcMol
                                       self.parent.obmol,               #destMol
                                       srcIndex = list(range(len(self))),
                                       destIndex= self._indices)
        syncronizer.syncBonds()

        #sync graph
        #   sync bond connection
        for bond in self.vmol.bonds:
            self.parent.molgraph.addBond(self.pindex[bond[0]],
                                         self.pindex[bond[1]])
