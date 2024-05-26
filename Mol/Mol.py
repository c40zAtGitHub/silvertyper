from __future__ import annotations

from .Interface.DumpLoad import DumpLoad
from .Interface.MolMatch import MolMatch
from .ObMol.ObMolConstructor import ObMolConstructor
from .GraphMol.Iterator.AtomIter import BFSAtomIter
from .Submol import Submol

# from ..ignore.Mol.OBInterface.OBMolConverter import OBMolConverter
# from ..ignore.Mol.OBInterface.OBSmartSearcher import OBSMARTSearcher

# from .MolView.MolView import MolView
# from .Iterator.MolGraphIter import BFSFloodMGIter
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ObMol import ObMolWrapper
    from .GraphMol import GraphMol
    from .ObMol.PerceptionRules import PerceptionRule

class StartSMINotHit(ValueError):
    def __init__(self):
        super().__init__("New smiles pattern does not hit the current system")


class Mol(DumpLoad):
    """
    Basic Molecule class
    initialization
    searching
    """
    def __init__(self,obmol:ObMolWrapper):
        self.obmol = obmol            
        self.molgraph = obmol.toGraphMol()
        self._startSmiles = None
        self._startIndices = None

    @classmethod
    def fromData(cls,atomTuples,
                 charges: list[float] = None,
                 startSmiles = None,
                 perceiveBC = True,
                 perceiveBO = False,
                 perceptionRule:PerceptionRule|None = None):
        """
        Generate a Mol object from various data
        Input:
        atomTuples  - list of (aNum,x,y,z) tuple
        charges     - list of floats of effective atomic charges
        startSmiles - a smiles code indicating the start of the fragment
                    used by fragment comparison
        perceiveBC  - flag for auto determine atom connectivity
        perceiveBO  - flat for auto calculate bond order
        perceptionRule - A PerceptionRule object that tells which atoms
                        are for bond and bond order perception

        """
        obmol:ObMolWrapper = ObMolConstructor.molFromEXYZ(
            atomTuples,
            perceiveBC=perceiveBC,
            perceiveBO=perceiveBO,
            perceptionRule=perceptionRule)
        mol = cls(obmol)
        mol.startSmiles = startSmiles

        if charges is not None:
            for ci,charge in enumerate(charges):
                mol.molgraph[ci].charge = charge
        return mol


    def __getitem__(self,index):
        return self.molgraph[index]
    
    def __len__(self):
        return len(self.molgraph)
    
    # def __getstate__(self):
    #     state = self.obmol.toDict()
    #     state["molgraph"] = self.molgraph
    #     state["startSmiles"] = self.startSmiles
    #     state["startIndices"] = self.startIndices
    #     return state

    # def __setstate__(self,state):
    #     obmol = ObMolConstructor.fromDict(state)
    #     self.obmol = obmol
    #     self.molgraph = state["graph"]
    #     self._startSmiles = state["startSmiles"]
    #     self._startIndices = state["startIndices"]
    
    @property
    def atoms(self):
        return self.molgraph.atoms
    
    @property
    def bonds(self):
        return self.molgraph.bonds
    
    @property
    def startSmiles(self):
        return self._startSmiles
    
    @startSmiles.setter
    def startSmiles(self,newSmiles):
        if newSmiles is None:
            self._startSmiles = None
            self._startIndices = None
        else:
            #check if the newSmiles hits certain part of self
            match = self.matchSmiles(newSmiles)
            if len(match) > 0:
                self._startSmiles = newSmiles
                self._startIndices = match
            else:
                raise StartSMINotHit()

    @property
    def startIndices(self):
        return self._startIndices
    
    
    def find(self,smilesPattern):
        return self.obmol.find(smilesPattern)
    
    def findall(self,smilesPattern):
        return self.obmol.findall(smilesPattern)

    def submol(self,atomIndices):
        return Submol(self,atomIndices)
   
    #iterators over its components
    @property
    def components(self):
        for cponentIndices in self.molgraph.components:
            yield self.submol(cponentIndices)
    
    def findbox(self,margin = 0.1):
        #find a box that encapsulate the given system
        #margin in angstrom
        atomEXYZ = self.obmol.toEXYZTuple()
        r0 = atomEXYZ[0]
        xmin = xmax = r0[1]
        ymin = ymax = r0[2]
        zmin = zmax = r0[3]
        for aCoord in atomEXYZ[1:]:
            x,y,z = aCoord[1:]
            xmin = min(xmin,x)
            xmax = max(xmax,x)
            ymin = min(ymin,y)
            ymax = max(ymax,y)
            zmin = min(zmin,z)
            zmax = max(zmax,z)
        return ((xmin-margin,ymin-margin,zmin-margin),
                (xmax+margin,ymax+margin,zmax+margin))




    
    

    
