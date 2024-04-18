from ..LammpsEntry import LammpsDataEntry

from silvertyper.Data.Entry.Badi import TwoAtomEntry
from silvertyper.Parser.LineParser.BadiLineParser import LineParser

class LammpsBondDataEntry(LammpsDataEntry,LineParser):
    _attrLink = ["type","atom1","atom2"]
    _strTemplate = "{}\t{}\t{}\t{}"
    def __init__(self, entryID, entryTypeID, atom1ID,atom2ID):
        LammpsDataEntry.__init__(self,entryID)
        data = TwoAtomEntry(entryTypeID,atom1ID,atom2ID)
        LineParser.__init__(self,data)

    def __str__(self):
        self._strTemplate.format(
            self.id,
            self.type,
            self.atom1,
            self.atom2
        )

    @classmethod
    def fromString(cls, entryString):
        items = entryString.split()
        entryID = int(items[0])
        entryTypeID = int(items[1])
        atom1 = int(items[2])
        atom2 = int(items[3])
        return cls(entryID,entryTypeID,atom1,atom2)
        

        