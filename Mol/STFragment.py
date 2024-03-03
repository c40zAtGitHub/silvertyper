#[S]ilver [T]yper Fragment class
#generated from common molecular structure files files:
#   x
#designated functionality:
#   SMARTS search via openbabel
#   generate sub molecules
#   assign charge

from silvertyper.Mixins.STDLMixin import STDLMixin
from silvertyper.OBInterface.OBMolConverter import OBMolConverter
from silvertyper.OBInterface.OBSmartSearcher import OBSMARTSearcher
from .STMolGraphIter import STBFSFloodMGIter

class STFragment(STDLMixin):
    """
    Basic STFragment class
    initialization
    searching
    """

    def __init__(self,
                 exyzTuples,        #list of (aNum,x,y,z) tuple
                 charges = None,    #list of floats of effective atomic charges
                 startSmiles = None,#a smiles code indicating the start of the fragment
                                    #   used by fragment comparison
                 perceiveBO = False #auto calculate bond order
                 ):
        #define placeholder variables
        self.obmol = OBMolConverter.molFromEXYZ(exyzTuples,perceiveBO=perceiveBO)
        self.molgraph = OBMolConverter.graphFromMol(self.obmol)
        self._startSmiles = None
        self._startIndices = None

        #intialization of individual variables
        self.startSmiles = startSmiles
        if charges is not None:
            for ci,charge in enumerate(charges):
                self.molgraph[ci].charge = charge


    def __getitem__(self,index):
        return self.molgraph[index]
    
    def __len__(self):
        return len(self.molgraph)
    
    def __getstate__(self):
        exyz = OBMolConverter.subObmolToEXYZ(self.obmol)
        state = {
            "exyz":exyz,
            "graph":self.molgraph,
            "startSmiles":self.startSmiles,
            "startIndices":self.startIndices
        }
        return state

    def __setstate__(self,state):
        obmol = OBMolConverter.molFromEXYZ(state["exyz"])
        self.obmol = obmol
        self.molgraph = state["graph"]
        self._startSmiles = state["startSmiles"]
        self._startIndices = state["startIndices"]
    
    @property
    def atoms(self):
        return self.molgraph.atoms
    
    @property
    def startSmiles(self):
        return self._startSmiles
    
    @startSmiles.setter
    def startSmiles(self,newSmiles):
        if newSmiles is None:
            self._startIndices = None
        else:
            #check if the newSmiles hits certain part of self
            match = self.matchSmiles(newSmiles)
            if len(match) > 0:
                self._startSmiles = newSmiles
                self._startIndices = match
            else:
                raise ValueError("New smiles pattern does not hit the current system")

    @property
    def startIndices(self):
        return self._startIndices
    
    
    def matchSmiles(self,smilesPattern):
        searcher = OBSMARTSearcher(self.obmol)
        match = searcher.find(smilesPattern)
        return match


    def subFrag(self,indices):
        newEXYZ = OBMolConverter.subObmolToEXYZ(self.obmol,indices)
        newCharges = [self.molgraph[i].charge for i in indices]
        newFrag = STFragment(newEXYZ,newCharges)
        return newFrag

    def subView(self,indices):
        sView = STFragView(self,indices)
        return sView
    
    #iterators over its components
    @property
    def components(self):
        for component in self.molgraph.components:
            yield STFragView(self,list(component))

    def matchFrag(self,otherFrag,startSmi = None):
        if len(self) != len(otherFrag):
            return False

        #priority of starting smiles:
        #   startSmi > otherFrag.startSmiles > self.startSmiles
        usableSmiles = [smi for smi in [startSmi,
                                        otherFrag.startSmiles,
                                        self.startSmiles]\
                        if smi is not None]
        
        #establish the starting smiles pattern
        if len(usableSmiles) == 0:
            errMsg = "The starting point smiles pattern is required"
            raise ValueError(errMsg)
        else:
            firstSmi = usableSmiles[0]

        if firstSmi == self.startSmiles:
            selfStIndices = self.startIndices
        else:
            selfStIndices = self.matchSmiles(firstSmi)

        if len(selfStIndices) == 0:
            return False

        if firstSmi == otherFrag.startSmiles:
            otherStIndices = otherFrag.startIndices
        else:
            otherStIndices = otherFrag.matchSmiles(firstSmi)

        if len(otherStIndices) == 0:
            return False

        selfFloodIter = STBFSFloodMGIter(self.molgraph,selfStIndices)
        otherFloodIter = STBFSFloodMGIter(otherFrag.molgraph,otherStIndices)
        for atomPair in zip(selfFloodIter,otherFloodIter):
            satom,oatom = atomPair
            if satom.atomNum != oatom.atomNum:
                return False
        return True
    
    def findBox(self,margin = 0.1):
        #find a box that encapsulate the given system
        #margin in angstrom
        atomCoords = OBMolConverter.subObmolToEXYZ(self.obmol)
        r0 = atomCoords[0]
        xmin = xmax = r0[1]
        ymin = ymax = r0[2]
        zmin = zmax = r0[3]
        for aCoord in atomCoords[1:]:
            x,y,z = aCoord[1:]
            xmin = min(xmin,x)
            xmax = max(xmax,x)
            ymin = min(ymin,y)
            ymax = max(ymax,y)
            zmin = min(zmin,z)
            zmax = max(zmax,z)
        return ((xmin-margin,ymin-margin,zmin-margin),
                (xmax+margin,ymax+margin,zmax+margin))

class STFragView:
    """
    ST Fragment View class
    A "view" of a STFragment class
    """
    def __init__(self,parent:STFragment,
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

    
    

    
