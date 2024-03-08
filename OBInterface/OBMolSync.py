from openbabel import openbabel as ob

class OBMolSyncronizer:

    def __init__(self,
                 srcMol: ob.OBMol,
                 destMol: ob.OBMol,
                 srcIndex: list[int]|None = None,
                 destIndex: list[int]|None = None):
        self._smol = srcMol
        self._dmol = destMol

        if srcIndex is None:
            srcIndex = list(range(srcMol.NumAtoms()))
        self._sIndex = [index + 1 for index in srcIndex]

        if destIndex is None:
            destIndex = list(range(destMol.NumAtoms()))
        self._dIndex = [index + 1 for index in destIndex]
    
    @property
    def MOL_SIZE_CONSISTENT(self):
        return len(self._sIndex) == len(self._dIndex)
    
    def destAtom(self,satom):
        sindex = satom.GetIdx()
        dindex = self._dIndex[self._sIndex.index(sindex)]
        datom = self._dmol.GetAtom(dindex)
        return datom
    
    def syncBonds(self):
        if self.MOL_SIZE_CONSISTENT:
            for sbond in ob.OBMolBondIter(self._smol):
                satom1 = sbond.GetBeginAtom()
                satom2 = sbond.GetEndAtom()
                sbondOrder = sbond.GetBondOrder()
                datom1 = self.destAtom(satom1)
                datom2 = self.destAtom(satom2)
                self._dmol.AddBond(datom1.GetIdx(),
                                   datom2.GetIdx(),
                                   sbondOrder)


