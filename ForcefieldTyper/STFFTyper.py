from __future__ import annotations

from silvertyper.OBInterface import OBSMARTSearcher
from silvertyper.ForcefieldTyper import ffDefaultPrm
from silvertyper.Mol.STMolGraphIter import STBFSFloodMGIter

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.Mol.STFragment import STFragment

class STForcefieldTyper:
    def __init__(self,smartsDict):
        self._smdict = smartsDict

    @classmethod
    def forForcefield(cls,forcefield=None):
        if forcefield is None:
            return None
        elif forcefield in ffDefaultPrm.keys():
            return cls(ffDefaultPrm[forcefield])
        else:
            raise ValueError("Forcefield {} not found".format(forcefield))

    def assignAtomType(self,stmol):
        molSearcher = OBSMARTSearcher(stmol.obmol)
        for smEntry in self._smdict:
            smPattern  = smEntry.pattern
            smATypes = smEntry.atomTypes
            smMatches = molSearcher.findall(smPattern)
            if len(smMatches)>0:
                for match in smMatches:
                    for index,aindex in enumerate(match):
                        #atype = smATypes[index]
                        #stmol[aindex].type = atype
                        try:
                            stmol[aindex].type = smATypes[index]
                        except IndexError:
                            break
                        

class STFragmentTyper:
    """
    STFragmentTyper
    A class that performs atom type assignment based on 
    a list of preassigned small fragments
    """
    def __init__(self,fragments):
        """
        Initialization
        fragments - list of STFragment that has a variety of info
        """
        self.fragments = {}
        for frag in fragments:
            size = len(frag)
            if size not in self.fragments.keys():
                self.fragments[size] = [frag]
            else:
                self.fragments[size].append(frag)


    def assignByFragments(self,stmol:STFragment):
        for component in stmol.components:
            cSize = len(component)
            if cSize in self.fragments.keys():
                for frag in self.fragments[cSize]:
                    if component.matchFrag(frag):
                        fragIter = STBFSFloodMGIter(frag.molgraph,frag.startIndices)
                        compIndices = component.matchSmiles(frag.startSmiles,parentIndex=True)
                        compIter = STBFSFloodMGIter(component.molgraph,compIndices)
                        for atomPair in zip(fragIter,compIter):
                            fatom,catom = atomPair
                            catom.type = fatom.type
                            catom.charge = fatom.charge

                    

