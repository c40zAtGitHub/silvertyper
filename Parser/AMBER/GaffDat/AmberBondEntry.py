"""
Line parser for bond parameter section
"""
from .AmberEntry import AmberEntry
from silvertyper.Parser.LineParser.BadiLineParser import BondLineParser

from silvertyper.Data.Label.AtomType.GaffAtomType import GAFFAtomType as GaffLabel
from silvertyper.Data.Label.FFTermLabel import FFTermLabel
from silvertyper.Data.Entry.FFPara import HarmonicParaEntry as HarmonicEntry

class AmberBondEntry(AmberEntry,BondLineParser):
    _keyLength = 5
    _strTemplate = "{}\t{:.1f}\t{:.4f}\t{}"
    def __init__(self,btype,Kr,re,description = None):
        """
        Harmonic bond term
        btype       - bond type
        Kr          - force constant in kcal/mol/A2
        re          - equilibrium bond distance in A
        description - additional notes on the data (source, reliability, etc.)
        """
        AmberEntry.__init__(self,description)
        data = HarmonicEntry(btype,Kr,re)
        BondLineParser.__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.Kr,
            self.re,
            self.description
        )

    @classmethod
    def fromString(cls,entryString):
        key,elements = cls.keyElements(entryString)
        btype = FFTermLabel(key,LabelType=GaffLabel)
        Kr = float(elements[0])
        re = float(elements[1])
        desp = " ".join(elements[2:])
        return cls(btype,Kr,re,description = desp)