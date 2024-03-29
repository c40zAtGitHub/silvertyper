from __future__ import annotations

from silvertyper.ForcefieldTyper.Dict.STFFKey import STFFKey

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .STFFKey import STFFKey

class STParaDictEntry:
    def __init__(self,index,key,para):
        self.index = index
        self.key = key
        self.para = para

class STBadiDict:
    def __init__(self,
                 bondDict,
                 angleDict,
                 dihedralDict,
                 improperDict):
        """
        dicts are in key:STParaDictEntry format
        """
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
        #ref to default key class that is used to
        #establish entries when inserting data
        self._DefaultKey = STFFKey     

    @classmethod
    def fromFile(cls,fileName):
        """
        Construct a dict from data file
        Leave it to individual ff types
        """
        raise NotImplementedError
    
    @property
    def sectionNames(self):
        return list(self.section.keys())
    
    def findall(self,key):
        """
        Search the key in all sections
            key - string or instance of Key object
        Returns a dict of hits in all sections
        """
        if type(key) is str:
            key = self._DefaultKey.fromString(key)
        
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
    
    def entries(self,sectionName,indices=None):
        if indices is None:
            #by default, all indices are fetched
            return self.section[sectionName].values()
        else:
            return [entry for entry in self.section[sectionName].values() if entry.index in indices]

    
