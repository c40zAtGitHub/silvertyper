from __future__ import annotations

from silvertyper.OBInterface.OBMolConverter import OBMolConverter

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.Mol.STFragment import STFragment

class AtomEntry:
    def __init__(self,atomNum,charge,x,y,z):
        self.atomNum = atomNum
        self.charge = charge
        self.x = x
        self.y = y
        self.z = z

    @property
    def R(self):
        return (self.x,self.y,self.z)



class STBadiData:
    def __init__(self,stmol:STFragment):
        #atom coordinate charge
        self.atoms = [] #including atom,charge,coords
        self.bonds = []
        self.angles = []
        self.dihedrals = []
        self.impropers = []
        self.vdw = []

        #construct atom data
        atoms = stmol.atoms
        atomCoords = OBMolConverter.subObmolToEXYZ(stmol.obmol)
        for atom,accord in zip(atoms,atomCoords):
            x,y,z = accord[1:]
            self.acc.append(STAtomEntry(atom.atomNum,
                             atom.charge,
                             x,y,z))

        
