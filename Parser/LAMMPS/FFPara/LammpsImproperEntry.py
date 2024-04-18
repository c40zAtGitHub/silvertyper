"""
Line parser for improper parameter section
"""
from silvertyper.Parser.LineParser.BadiLineParser import CvffImproperLineParser

from silvertyper.Data.Entry.FFPara import CvffParaEntry as CvffEntry

class LammpsImproperEntry(CvffImproperLineParser):
    _strTemplate = "improper_coeff {} cvff {} {} {}"
    def __init__(self,itype,
                 Vn,d,n):
        """
        Improper term
        Energy defined in the below expression:
        E(φ) = Vn * (1+ d*cos(nφ))

        Vn      - Vn in kcal/mol, half of actual barrier
        d       - -1 or 1
        n       - n
        """
        data = CvffEntry(itype,Vn,d,n)
        CvffImproperLineParser.__init__(self,data)

    def __str__(self):

        return self._strTemplate.format(
            self.type,
            self.Vn,
            self.d,
            self.n
        )
    
    @classmethod
    def fromLine(cls,line):
        items = line.split()
        entryType = items[1]
        Vn = float(items[3])
        d = int(items[4])
        n = int(items[5])
        return cls(entryType,Vn,d,n)