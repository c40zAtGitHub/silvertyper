import os

class XYZFile(object):
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
    def fromCluster(cls,cluster):
        nAtoms = cluster.atomCount
        title = ""
        atomCoords = ""
        for atomEntry in cluster:
            atomCoords += "{}\t{:10f}\t{:10f}\t{:10f}\n".format(atomEntry.atom.symbol,
                                                                atomEntry.coordinate.x,
                                                                atomEntry.coordinate.y,
                                                                atomEntry.coordinate.z)
        return XYZFile(nAtoms,title,atomCoords)

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
