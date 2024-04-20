from silvertyper.Parser.LineParser.AtomMassLineParser import AtomMassLineParser
from silvertyper.Data.Entry.FFPara.Mass import MassParaEntry as MassEntry

class LammpsMassEntry(AtomMassLineParser):
    _strTemplate = "\t{}\t{:.4g}"
    def __init__(self, atype,mass):
        """
        atype - the type (label) of atom
        mass  - atomic mass in amu
        """
        data = MassEntry(atype,mass)
        super().__init__(data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.mass
        )
    
    @classmethod
    def fromString(cls,entryString):
        items = entryString.split()
        atype = int(items[0])
        mass = float(items[1])
        return cls(atype,mass)
        

        
