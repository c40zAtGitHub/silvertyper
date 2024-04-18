from ..LammpsEntry import LammpsDataEntry

from silvertyper.Data.Entry.Badi import FourAtomEntry
from silvertyper.Parser.LineParser.BadiLineParser import LineParser

class LammpsDihedralDataEntry(LammpsDataEntry,LineParser):
    _attrLink = ["type","atom1","atom2","atom3","atom4"]
    _strTemplate = "{}\t{}\t{}\t{}\t{}\t{}"
    def __init__(self, entryID, entryTypeID, atom1ID,atom2ID,atom3ID,atom4ID):
        LammpsDataEntry.__init__(self,entryID)
        data = FourAtomEntry(entryTypeID,atom1ID,atom2ID,atom3ID,atom4ID)
        LineParser.__init__(self,data)

    def __str__(self):
        self._strTemplate.format(
            self.id,
            self.type,
            self.atom1,
            self.atom2,
            self.atom3,
            self.atom4
        )

    @classmethod
    def fromString(cls, entryString):
        items = entryString.split()
        entryID = int(items[0])
        entryTypeID = int(items[1])
        atom1 = int(items[2])
        atom2 = int(items[3])
        atom3 = int(items[4])
        atom4 = int(items[5])
        return cls(entryID,entryTypeID,atom1,atom2,atom3,atom4)