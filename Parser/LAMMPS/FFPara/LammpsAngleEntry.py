from silvertyper.Parser.LineParser.BadiLineParser import AngleLineParser

from silvertyper.Data.Entry.FFPara import HarmonicParaEntry as HarmonicEntry

class LammpsBondEntry(AngleLineParser):
    _strTemplate = "angle_coeff {} harmonic {:.1f} {:.4g}"
    def __init__(self,entryType,
                 Kt,te):
        """
        Harmonic angle term
        atype - angle type
        Kt    - force constant in kcal/mol/rad2
        te    - θe, equilibrium angle in rad
        description - additional notes on the data (source, reliability, etc.)
        """
        data = HarmonicEntry(entryType,Kt,te)
        super().__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.Kt,
            self.te
        )

    @classmethod
    def fromString(cls,entryString):
        items = entryString.split()
        entryType = items[1]
        Kt = float(items[3])
        te = float(items[4])
        return cls(entryType,Kt,te)

    
        
