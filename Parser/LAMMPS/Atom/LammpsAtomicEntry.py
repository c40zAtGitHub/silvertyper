from ..LammpsEntry import LammpsDataEntry

from silvertyper.Data.Entry.Atom import AtomicEntry
from silvertyper.Parser.LineParser.AtomLineParser import AtomicLineParser

class LammpsAtomDataEntry(LammpsDataEntry,AtomicLineParser):
    _strTemplate = "{}\t{}\t{:.8f}\t{:.8f}\t{:.8f}"
    def __init__(self, entryID, entryType, x, y, z):
        LammpsDataEntry.__init__(self,entryID)
        data = AtomicEntry(entryType,x,y,z)
        AtomicLineParser.__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.id,
            self.data,
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
        return cls(entryID,entryType,x,y,z)


        
        