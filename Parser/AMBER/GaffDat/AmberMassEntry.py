"""
Line parser for atom type definition section
"""
from .AmberEntry import AmberEntry
from silvertyper.Parser.LineParser.AtomMassLineParser import AtomMassPolarLineParser as AMPLineParser

from silvertyper.Data.Label.AtomType.GaffAtomType import GAFFAtomType as GaffLabel
from silvertyper.Data.Entry.FFPara.Mass import MassPolarParaEntry as MassPolarEntry

class AmberMassEntry(AmberEntry,AMPLineParser):
    _keyLength = 2
    _strTemplate = "{}\t{:.4g}\t{:.3f}\t{}"
    def __init__(self, atype, mass, polarizability, description=None):
        """
        #atom type entry 
        atype           - atom type label
        mass            - atomicMass in amu
        polarizability  - atom polarizability in A3
        """
        AmberEntry.__init__(self,description)
        data = MassPolarEntry(atype, mass, polarizability)
        AMPLineParser.__init__(self,data)
        

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.mass,
            self.polarizability,
            self.description
            )
        
    @classmethod
    def fromString(cls,entryString):
        key,elements = cls.keyElements(entryString)
        atype = GaffLabel(key)
        amass = float(elements[0])
        apol = float(elements[1])
        desp = " ".join(elements[2:])
        return cls(atype,amass,apol,description = desp)