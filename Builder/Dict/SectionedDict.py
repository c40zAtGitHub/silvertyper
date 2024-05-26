from __future__ import annotations

from silvertyper.Data.SectionedDict import SectionedDict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.Parser.LineParser import LineParser



class SectionedDictBuilder:
    """
    Build a sectioned dict from a File object
    """
    _sections = []

    def __init__(self,fileObj):
        self.sdict = SectionedDict()
        self.file = fileObj

    def __section_lines__(self,section:str) -> list[str]:
        """
        find the lines of content of a given section
        """
        raise NotImplementedError
    
    def __section_parser__(self,section:str) -> LineParser:
        """
        find the parser of a given section that
        resolves line contents
        """
        raise NotImplementedError
    
    def build(self):
        for section in self._sections:
            self.sdict.newSection(section)
            secParser = self.__section_parser__(section)
            secLines = self.__section_lines__(section)
            for line in secLines:
                dataEntry = secParser.fromString(line)
                key = dataEntry.type
                self.sdict[section].addEntry(key,dataEntry)    
        return self.sdict
        
