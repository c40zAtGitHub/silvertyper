"""
Line parser for improper parameter section
"""
from .AmberEntry import AmberEntry
from silvertyper.Parser.LineParser.BadiLineParser import FourierImproperLineParser

from silvertyper.Data.Label.AtomType.GaffAtomType import GaffAtomType as GaffLabel
from silvertyper.Data.Label.FFTermLabel import FFTermLabel
from silvertyper.Data.Entry.FFPara import FourierParaEntry as FourierEntry

class AmberImproperEntry(AmberEntry,FourierImproperLineParser):
    _keyLength = 11
    _strTemplate = "{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{}"
    def __init__(self,itype,
                 Vn,gamma,n,
                 description = None):
        """
        Improper term
        Energy defined in the below expression:
        E(φ) = Vn * (1+ cos(nφ - γ))

        Vn      - Vn in kcal/mol, half of actual barrier
        gamma   - γ in degree
        n       - n
        """
        AmberEntry.__init__(self,description)
        data = FourierEntry(itype,Vn,1,gamma,n)
        FourierImproperLineParser.__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.Vn,
            self.gamma,
            self.n,
            self.description
        )

    @classmethod
    def fromLine(cls,line):
        key,elements = cls.keyElements(line)
        dtype = FFTermLabel(key,LabelType=GaffLabel)
        Vn = float(elements[0])
        gamma = float(elements[1])
        n = float(elements[2])
        desp = " ".join(elements[3:])
        return cls(dtype,Vn,gamma,n,description = desp)