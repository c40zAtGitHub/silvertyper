from silvertyper.Parser.LineParser.BadiLineParser import BondLineParser

from silvertyper.Data.Entry.FFPara import HarmonicParaEntry as HarmonicEntry

class LammpsBondEntry(BondLineParser):
    _strTemplate = "bond_coeff {} harmonic {:.1f} {:.4g}"
    def __init__(self,entryType,
                 Kr,re):
        """
        Harmonic bond term
        btype       - bond type
        Kr          - force constant in kcal/mol/A2
        re          - equilibrium bond distance in A
        """
        data = HarmonicEntry(entryType,Kr,re)
        super().__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.Kr,
            self.re
        )

    @classmethod
    def fromString(cls,entryString):
        items = entryString.split()
        entryType = items[1]
        Kr = float(items[3])
        re = float(items[4])
        return cls(entryType,Kr,re)

    
        
