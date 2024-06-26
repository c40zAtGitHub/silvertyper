from __future__ import annotations
from openbabel import openbabel as ob

from .ObMolWrapper import ObMolWrapper
from .ObMolSync import ObMolSyncronizer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.File.XYZFile import XYZFile
    from .PerceptionRules import PerceptionRule
    
def obmolFromTuples(exyzTuples):
    obmol = ob.OBMol()
    for exyz in exyzTuples:
        ele,x,y,z = exyz
        atom = obmol.NewAtom()
        #convert atom symbol to atomic number
        if type(ele) == str:
            ele = ob.GetAtomicNum(ele)
        atom.SetAtomicNum(ele)
        atom.SetVector(x,y,z)
    return obmol

class ObMolConstructor:
    @classmethod
    def fromXYZFile(cls,
        xyzFileObj:XYZFile,
        perceiveBC:bool = True,  #Flag telling if bond connection is to be perceived
        perceiveBO:bool = False,  #Flag telling if bond order is to be perceived
        perceptionRule:PerceptionRule|None = None #Rule object that controls bond perception and bond order
        ):
        exyzTuples = xyzFileObj.toEXYZTuples()
        return cls.fromEXYZTuples(exyzTuples,
                                  perceiveBC=perceiveBC,
                                  perceiveBO=perceiveBO,
                                  perceptionRule = perceptionRule)
    @classmethod
    def fromDict(cls,molDict):
        """
        Construct a obmol from dict generated by toDict() method
        dict contains "exyz" and "bonds" key
        exyz gives a list of (atom number,x,y,z) tuples
        bonds gives a list of (atom1 index, atom2 index, bond order) tuple
            indices start from 0
        """
        exyz = molDict["exyz"]
        bonds = molDict["bonds"]
        obmol = obmolFromTuples(exyz,perceiveBC=False)
        for bond in bonds:
            atom1Idx = bond[0]+1
            atom2Idx = bond[1]+1
            bondOrder = bond[2]
            obmol.AddBond(atom1Idx,atom2Idx,bondOrder)
        return ObMolWrapper(obmol)
        
    @classmethod
    def fromEXYZTuples(cls,
        exyzTuples,
        perceiveBC:bool = True,
        perceiveBO:bool = False,
        perceptionRule:PerceptionRule|None = None):
        """
        Construct a wrapped ObMol object with exyz tuples
        Input:
        exyzTuples  - list of (aNum,x,y,z) tuple
        perceiveBC  - flag for auto determine atom connectivity
        perceiveBO  - flat for auto calculate bond order
        perceptionRule - A PerceptionRule object that tells which atoms
                        are for bond and bond order perception
        """
        obmol = obmolFromTuples(exyzTuples)

        if perceiveBC is True:
            if perceptionRule is None:
                obmol.ConnectTheDots()
            else:
                bondIndices = perceptionRule.conIndices(obmol)
                bondTuples = [exyzTuples[index] for index in bondIndices]
                bondobmol = obmolFromTuples(bondTuples)
                bondobmol.ConnectTheDots()
                synchronizer = ObMolSyncronizer(bondobmol,obmol,
                                                destIndex=bondIndices)
                synchronizer.syncBonds()

        if perceiveBO is True:
            if perceptionRule is None:
                obmol.PerceiveBondOrders()
            else:
                orderIndices = perceptionRule.orderIndices(obmol)
                orderTuples = [exyzTuples[index] for index in orderIndices]
                orderobmol = obmolFromTuples(orderTuples)
                orderobmol.ConnectTheDots()
                orderobmol.PerceiveBondOrders()
                synchronizer = ObMolSyncronizer(orderobmol,obmol,
                                                destIndex=orderIndices)
                synchronizer.syncBonds()
        return ObMolWrapper(obmol)