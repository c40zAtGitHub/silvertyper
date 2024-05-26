from openbabel import openbabel as ob
from ..GraphMol import GraphMol


class ObMolConverter:
    """
    Mixin of ObMolWrapper
    """
    def toEXYZTuple(self,indices=None):
        """
        Convert atom coordinates to list of (atomic number,x,y,z) tuples
        """
        if indices is None:
            indices = range(self.obmol.NumAtoms())
        
        exyzTuples = []
        for index in indices:
            atom = self.obmol.GetAtom(index+1)
            aNum = atom.GetAtomicNum()
            aTuple = (aNum,atom.GetX(),atom.GetY(),atom.GetZ())
            exyzTuples.append(aTuple)

        return exyzTuples
    
    def toDict(self):
        """
        Convert atom and bond information to
        a dictionary containing two keys:
        "exyz","bonds"
        exyz stores a list of (atom number,x,y,z) tuples
        bonds stores a list of (atom1 index, atom2 index, bond order) tuple
        """
        molDict = {}
        exyz = self.toEXYZTuple()
        molDict["exyz"] = exyz
        bonds = []
        for bond in ob.OBMolBondIter(self.obmol):
            begin = bond.GetBeginAtomIdx()-1
            end = bond.GetEndAtomIdx()-1
            order = bond.GetBondOrder()
            bonds.append((begin,end,order))
        molDict["bonds"] = bonds
            
        return molDict

    def toGraphMol(self):
        """
        convert to a GraphMol instance
        """
        gmol = GraphMol()
        for atom in ob.OBMolAtomIter(self.obmol):
            aIndex = atom.GetIdx() - 1
            aNumber = atom.GetAtomicNum()
            gmol.addAtom(aIndex,aNumber)

        for bond in ob.OBMolBondIter(self.obmol):
            begin = bond.GetBeginAtomIdx()-1
            end = bond.GetEndAtomIdx()-1
            gmol.addBond(begin,end)

        return gmol