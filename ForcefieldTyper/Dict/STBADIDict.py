from __future__ import annotations

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .STFFKey import STFFKey

class STParaDictEntry:
    def __init__(self,index:int,
                 key:STFFKey,
                 para:tuple|list[tuple]):
        self.index = index
        self.key = key
        self.para = para

class STBADIDict:
    def __init__(self,bondDict:dict,
                 angleDict:dict,
                 dihedralDict:dict,
                 improperDict:dict):
        
        self.section = {
            'bond':bondDict,
            'angle':angleDict,
            'dihedral':dihedralDict,
            'improper':improperDict
        }
        self.sectionOfKeyLength = {
            2:['bond'],
            3:['angle'],
            4:['dihedral','improper']
        }

    @classmethod
    def fromFile(cls,fileName):
        """
        Construct a dict from data file
        Leave it to individual ff types
        """
        raise NotImplementedError
    
    def find(self,key):
        """
        Search the key in all sections
        """
        keyLength = len(key)
        result = {}
        try:
            targetSections = self.sectionOfKeyLength[keyLength]
        except KeyError:
            #a guaranteed miss based on key length
            return result
        
        for section in targetSections:
            secResult = self.findInSection(key,section) #list of entries
            result[section] = secResult
        
        return result

    def findInSection(self,key,section):
        return self.section[section][key]
    
    @property
    def bonds(self):
        return self.section['bond'].values()
    
    @property
    def angles(self):
        return self.section['angle'].values()

    @property
    def dihedrals(self):
        return self.section['dihedral'].values()

    @property
    def impropers(self):
        return self.section['improper'].values()

    
