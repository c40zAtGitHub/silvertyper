from __future__ import annotations
from .GraphMol.Iterator.AtomIter import BFSAtomIter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Mol import Mol
    from .Submol import Submol

class NoValidStartSMI(ValueError):
    """
    Exception rased when no valid starting smiles
    is provided during mol comparison.
    """
    errMsg = "A valid starting point smiles pattern is required for mol comparison"
    def __init__(self):
        super().__init__(self.errMsg)

class MolNotMatch(ValueError):
    errMsg = "Two mols does not match under given conditions"
    def __init__(self):
        super().__init__(self.errMsg)

class MolAlignment:
    def __new__(cls,
                 srcMol:Mol|Submol|None = None,
                 destMol:Mol|Submol|None = None,
                 startSmi:str|None = None):
        if srcMol is None or destMol is None:
            return None
        else:
            try:
                srcSerial,destSerial = cls.findSerial(srcMol,destMol,startSmi=startSmi)
            except MolNotMatch:
                return None
            
            newMAObj = super().__new__(cls)
            newMAObj.srcMol = srcMol
            newMAObj.destMol = destMol
            newMAObj.srcSerial = srcSerial
            newMAObj.destSerial = destSerial
            return newMAObj
        
    def atomPairs(self):
        for srcIdx,destIdx in zip(self.srcSerial,self.destSerial):
            yield (self.srcMol[srcIdx],self.destMol[destIdx])

    @classmethod
    def findSerial(self,mol1,mol2,
                    startSmi = None):
        if len(mol1) != len(mol2):
            raise MolNotMatch

        #priority of starting smiles:
        #   startSmi > mol1.startSmiles > mol2.startSmiles
        usableSmi = [smi for smi in [startSmi,
                                        mol1.startSmiles,
                                        mol2.startSmiles]\
                        if smi is not None]
        
        #establish the starting smiles pattern
        if len(usableSmi) == 0:
            raise NoValidStartSMI
        else:
            firstSmi = usableSmi[0]

        def findStartIdx(smi,mol):
            """
            Sub routine to find starting
            atom indices from smi
            """
            if smi == mol.startSmiles:
                idx = mol.startIndices
            else:
                idx = mol.find(smi)
            return idx

        m1Idx = findStartIdx(firstSmi,mol1)
        if len(m1Idx) == 0:
            #the two mols does not match at all
            raise MolNotMatch
        m2Idx = findStartIdx(firstSmi,mol2)
        if len(m2Idx) == 0:
            raise MolNotMatch

        m1FloodIter = BFSAtomIter(mol1.molgraph,m1Idx)
        m2FloodIter = BFSAtomIter(mol2.molgraph,m2Idx)
        for atomPair in zip(enumerate(m1FloodIter),enumerate(m2FloodIter)):
            a1,a2 = atomPair
            index1,atom1 = a1
            index2,atom2 = a2
            if atom1.atomNum != atom2.atomNum:
                raise MolNotMatch
            else:
                m1Idx.append(index1)
                m2Idx.append(index2)
        return (m1Idx,m2Idx)

    def syncProperties(self,
                       attributes:list[str]|None = None):
        if attributes is None:
            attributes = []
            
        for srcAtom,destAtom in self.atomPairs:
            for attr in attributes:
                srcAttrValue = getattr(srcAtom,attr)
                setattr(destAtom,attr,srcAttrValue)
