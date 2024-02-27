"""
OBMol related conversion methods
"""
from openbabel import openbabel as ob

from silvertyper.Mol.STMolGraph import STMolGraph

class OBMolConverter:
    @classmethod
    def molFromEXYZ(cls,exyzTuples):
        obmol = ob.OBMol()
        for exyz in exyzTuples:
            ele,x,y,z = exyz
            atom = obmol.NewAtom()

            #convert atom symbol to atomic number
            if type(ele) == str:
                ele = ob.GetAtomicNum(ele)

            atom.SetAtomicNum(ele)
            atom.SetVector(x,y,z)
        obmol.ConnectTheDots()
        return obmol
    
    @classmethod
    def subObmolToEXYZ(cls,obmol,indices=None):
        if indices is None:
            indices = range(obmol.NumAtoms())
        
        exyzTuples = []
        for index in indices:
            atom = obmol.GetAtom(index+1)
            aNum = atom.GetAtomicNum()
            aTuple = (aNum,atom.GetX(),atom.GetY(),atom.GetZ())
            exyzTuples.append(aTuple)

        return exyzTuples

    @classmethod
    def graphFromMol(cls,obmol):
        """
        create an STMolGraph instance based on the given mol
        """
        molgraph = STMolGraph()
        for atom in ob.OBMolAtomIter(obmol):
            aIndex = atom.GetIdx() - 1
            aNumber = atom.GetAtomicNum()
            molgraph.addAtom(aIndex,aNumber)

        for bond in ob.OBMolBondIter(obmol):
            begin = bond.GetBeginAtomIdx()-1
            end = bond.GetEndAtomIdx()-1
            molgraph.addBond(begin,end)

        return molgraph