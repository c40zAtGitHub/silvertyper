from __future__ import annotations

from .SectionedDict import SectionedDictBuilder

from silvertyper.Parser.LineParser import LineParser
from silvertyper.Parser.AMBER.GaffDat import AmberMassEntry,AmberVdwEntry,\
    AmberBondEntry,AmberAngleEntry,AmberDihedralEntry,AmberImproperEntry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.File.AMBER.GaffDatFile import GaffDatFile

class AMBERGaffParaDictBuilder(SectionedDictBuilder):
    

    _sectionParsers = {"type":AmberMassEntry,
                       "bond":AmberBondEntry,
                       "angle":AmberAngleEntry,
                       "dihedral":AmberDihedralEntry,
                       "improper":AmberImproperEntry,
                       "vdw":AmberVdwEntry}
    _sections = list(_sectionParsers.keys())

    def __init__(self,fileObj:GaffDatFile):
        super().__init__(fileObj)

    def __section_lines__(self, section: str) -> list[str]:
        """
        find the lines of content of a given section
        """
        return getattr(self.file,section+"Section")
    
    def __section_parser__(self, section: str) -> LineParser:
        """
        find the parser of a given section that
        resolves line contents
        """
        return self._sectionParsers[section]
