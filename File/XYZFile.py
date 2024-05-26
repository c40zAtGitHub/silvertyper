import os

from .FileInterface import File

from silvertyper.Utilities.AtomicMassData import atomSymbols

class XYZFile(File):
    def __init__(self,nAtom,title,atomCoords):
        self.nAtom = nAtom
        self.title = title
        self.atomCoords = atomCoords
        #atomCoords is a multiline string

    @classmethod
    def fromStream(cls,fstream):
        flines = fstream.splitlines()
        nAtom = int(flines[0])
        title = flines[1]
        atomLines = os.linesep.join(flines[2:2+nAtom])
        return XYZFile(nAtom,title,atomLines)

    @classmethod
    def fromEXYZTuples(cls,tupleList):
        """Generate xyz file from list of (Element,x,y,z) tuples"""
        nAtoms = len(tupleList)
        title = ""
        atomCoords = ""
        for entry in tupleList:
            atomCoords += "{}\t{:10f}\t{:10f}\t{:10f}\n".format(*entry)
        return XYZFile(nAtoms,title,atomCoords)

    def toStream(self):
        return """{}
{}
{}""".format(self.nAtom,self.title,self.atomCoords)
    
    def toEXYZTuples(self):
        exyzLines = self.atomCoords.splitlines()
        exyzTuples = []
        for line in exyzLines:
            aSymbol,x,y,z = line.split()
            try:
                aNum = int(aSymbol)
            except ValueError:
                aNum = atomSymbols.index(aSymbol) + 1

            x = float(x)
            y = float(y)
            z = float(z)
            exyzTuples.append((aNum,x,y,z))
        return exyzTuples
