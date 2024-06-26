from __future__ import annotations

#from silvertyper.OBInterface import OBSMARTSearcher
#from Typer import ffDefaultPrm
#from Mol.Iterator.MolGraphIter import STBFSFloodMGIter

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Mol import Mol

class ForcefieldTyper:
    def __init__(self,mol:Mol):
        self.mol = mol

class ForcefieldTyper:
    def __init__(self,ffname,smartsDict):
        self._ffname = ffname
        self._smdict = smartsDict

    @classmethod
    def forForcefield(cls,forcefield=None):
        if forcefield is None:
            return None
        elif forcefield in ffDefaultPrm.keys():
            ffname = ffDefaultPrm[forcefield]["name"]
            ffdict = ffDefaultPrm[forcefield]["dict"]
            return cls(ffname,ffdict)
        else:
            raise ValueError("Forcefield {} not found".format(forcefield))

    def assignAtomType(self,stmol):
        molSearcher = OBSMARTSearcher(stmol.obmol)
        ffname = self._ffname
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
                            stmol[aindex].ffname = ffname
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
                            catom.ffname = fatom.ffname

                    

