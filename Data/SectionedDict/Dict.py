
from .DictSection import Section

class SectionedDict:
    """
    Dictionary divided by section
    data access supports both by index and by key

    mainly for ff para and atomic data
    query is more frequent than insertion/deletion
    """
    def __init__(self):
        self._sections = {}
        self._sectionOfKeyLength = {}
    
    def __getitem__(self,sectionName):
        return self._sections[sectionName]

    def newSection(self,sectionName):
        if sectionName in self._sections.keys():
            raise ValueError(f"Section {sectionName} already exists")
        else:
            self._sections[sectionName] = Section(sectionName)

    @classmethod
    def fromFile(cls,fileContent):
        raise NotImplementedError
    
    def findEntryInSection(self,entryKey,section):
        return self[section][entryKey]
    
    def findall(self,entryKey):
        pass





