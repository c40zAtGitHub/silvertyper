from __future__ import annotations

from .AtomDataEntry.Charge import ChargeEntry as LAMMPSChargeEntry

from silvertyper.ForcefieldTyper.STFFTermIter import STFFIter
from silvertyper.OBInterface.OBMolConverter import OBMolConverter
from silvertyper.Utilities.AtomicMassData import elementMasses

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.Mol.STFragment import STFragment

"""
Notes:
IDs (atom, bond, ...), including type IDs, are by default numbers.
    Additional setup required if strings are to be used.
IDs starts with 1
BADI IDs have few variety in their format, while Atoms lines have many
"""

class LAMMPSBadiEntry:
    """
    Entry that represents BADI data line format in LAMMPS
    Usually in the following format
    [BADI ID] [BADI Type ID] [Atom1 ID] [Atom2 ID] [?Atom3/4 ID]
    """
    def __init__(self,entryID,entryTypeID,*entryItems):
        self.entryID = entryID
        self.entryTypeID = entryTypeID
        self.entryItems = [item for item in entryItems]

    def __iter__(self):
        return self
    
    def __next__(self):
        yield self.entryID
        yield self.entryTypeID
        for item in self.entryItems:
            yield item
    
    def __str__(self):
        template = "\t{}"*(len(self.entryItems) + 2)
        strRepr = template.format(self.entryID,self.entryTypeID,*self.entryItems)
        return strRepr

class DataGroup:
    def __init__(self,groupName,entryClass = LAMMPSBadiEntry):
        self.name = groupName
        self.data = []

        #self.type includes both key:typeID
        #and typeID:key entries
        #call type[ID] for keys and type[key] for ids
        self.type = {}                  
        self.EntryClass = entryClass

    def __getitem__(self,index):
        return self.data[index]

    def addDataEntry(self,
                     entryKey,                  #strings of slash connected atom types
                     *entryElements,            #items to be parsed to the EntryClass construction
                     ):
        entryID = len(self.data) + 1
        entryTypeID = self._newTypeID(entryKey) #singleton constructor
        entry = self.EntryClass(entryID,entryTypeID,*entryElements)
        self.data.append(entry)

    def _newTypeID(self,key):
        #distribute type ID as singleton
        if key in self.type.keys():
            return self.type[key]
        else:
            newID = len(self.type) + 1
            self.type[key] = newID
            self.type[newID] = key
            return newID


class LAMMPSBadiData:
    
    def __init__(self,stmol:STFragment):
        self._iter = STFFIter(stmol)

        self._dataGroups = {
            'atom':DataGroup('atom',entryClass=LAMMPSChargeEntry),
            'bond':DataGroup('bond'),
            'angle':DataGroup('angle'),
            'dihedral':DataGroup('dihedral'),
            'improper':DataGroup('improper')
        }
        self.box = stmol.findBox()

        self._updateAtom()
        self._updateBADI()

    def __getitem__(self,sectionName):
        return self._dataGroups[sectionName]

    @property
    def mol(self):
        return self._iter.mol
    
    @property
    def sections(self):
        return list(self._dataGroups.keys())
    
    @property
    def dataGroups(self):
        return self._dataGroups.values()

    def _updateAtom(self):
        atoms = self.mol.atoms
        atomCoords = OBMolConverter.subObmolToEXYZ(self.mol.obmol)
        for atom,accord in zip(atoms,atomCoords):
            atype = atom.type               #atom type
            charge = atom.charge            #partial charge
            x,y,z = accord[1:]              #Cartesian coordinate
            self._dataGroups['atom'].addDataEntry(atype,charge,x,y,z)

    def _updateBADI(self):
        for bond in self._iter.bonds:
            atmIndices = [index+1 for index in bond]
            key = '-'.join([self.mol[index].type for index in bond])
            self._dataGroups['bond'].addDataEntry(key,*atmIndices)

        for angle in self._iter.angles:
            atmIndices = [index+1 for index in angle]
            key = '-'.join([self.mol[index].type for index in angle])
            self._dataGroups['angle'].addDataEntry(key,*atmIndices)

        for dihedral in self._iter.dihedrals:
            atmIndices = [index+1 for index in dihedral]
            key = '-'.join([self.mol[index].type for index in dihedral])
            self._dataGroups['dihedral'].addDataEntry(key,*atmIndices)

        for improper in self._iter.impropers:
            atmIndices = [index+1 for index in improper]
            key = '-'.join([self.mol[index].type for index in improper])
            self._dataGroups['improper'].addDataEntry(key,*atmIndices)

    @property
    def atom(self):
        return self._dataGroups['atom'].data

    @property
    def bond(self):
        return self._dataGroups['bond'].data

    @property
    def angle(self):
        return self._dataGroups['angle'].data

    @property
    def dihedral(self):
        return self._dataGroups['dihedral'].data

    @property
    def improper(self):
        return self._dataGroups['improper'].data

        


        
