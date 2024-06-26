import os
from ..FileInterface import File

class LAMMPSParameterFile(File):
    _symbolDefLineTemp = "labelmap\t{idType}\t{numID}\t{strID}"
    def __init__(self,
                 bonds,
                 angles,
                 dihedrals,
                 impropers,
                 pairs,
                 symbolDefs = None):
        self.symbolDef = symbolDefs
        self.bonds = bonds
        self.angles = angles
        self.dihedrals = dihedrals
        self.impropers = impropers
        self.pairs = pairs

    def __str__(self):
        sep = os.linesep
        bondLines = sep.join(self.bonds)
        angleLines = sep.join(self.angles)
        dihedralLines = sep.join(self.dihedrals)
        improperLines = sep.join(self.impropers)
        pairLines = sep.join(self.pairs)
        fileContent = sep.join([bondLines,angleLines,dihedralLines,improperLines,pairLines])
        return fileContent
    
    @classmethod
    def fromStream(cls,fileContent):
        raise NotImplementedError
    
    def toStream(self):
        raise NotImplementedError
