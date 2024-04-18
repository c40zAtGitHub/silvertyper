from ..LammpsEntry import LammpsDataEntry

from silvertyper.Data.Entry.Atom import ChargeEntry
from silvertyper.Parser.LineParser.AtomLineParser import ChargeLineParser

class LammpsAtomDataEntry(LammpsDataEntry,ChargeLineParser):

    _strTemplate = "{}\t{}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}"
    def __init__(self, entryID, entryType, x, y, z, q):
        LammpsDataEntry.__init__(self,entryID)
        data = ChargeEntry(entryType,x,y,z,q)
        ChargeLineParser.__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.id,
            self.data,
            self.q,
            self.x,
            self.y,
            self.z
        )
    
    @classmethod
    def fromString(cls,lineString):
        items = lineString.split()
        entryID = int(items[0])
        entryType = int(items[1])
        x = float(items[2])
        y = float(items[3])
        z = float(items[4])
        q = float(items[5])
        return cls(entryID,entryType,x,y,z,q)