"""
Line parser for angle parameter section
"""
from .AmberEntry import AmberEntry
from silvertyper.Parser.LineParser.BadiLineParser import AngleLineParser

from silvertyper.Data.Label.AtomType.GaffAtomType import GAFFAtomType as GaffLabel
from silvertyper.Data.Label.FFTermLabel import FFTermLabel
from silvertyper.Data.Entry.FFPara import HarmonicParaEntry as HarmonicEntry


class AmberAngleEntry(AmberEntry,AngleLineParser):
    _keyLength = 8
    _strTemplate = "{}\t{:.1f}\t{:.2f}\t{}"
    def __init__(self,btype,Kt,te,description = None):
        """
        Harmonic angle term
        atype - angle type
        Kt    - force constant in kcal/mol/rad2
        te    - θe, equilibrium angle in degree
        description - additional notes on the data (source, reliability, etc.)
        """
        AmberEntry.__init__(self,description)
        data = HarmonicEntry(btype,Kt,te)
        AngleLineParser.__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.Kt,
            self.te,
            self.description
        )

    @classmethod
    def fromString(cls,entryString):
        key,elements = cls.keyElements(entryString)
        btype = FFTermLabel(key,LabelType=GaffLabel)
        Kt = float(elements[0])
        te = float(elements[1])
        desp = " ".join(elements[2:])
        return cls(btype,Kt,te,description = desp)