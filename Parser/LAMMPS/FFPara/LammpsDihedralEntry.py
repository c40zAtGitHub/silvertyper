"""
Line parser for dihedral parameter section
"""
from silvertyper.Parser.LineParser.BadiLineParser import DihedralLineParser

from silvertyper.Data.Label.AtomType.GaffAtomType import GaffAtomType as GaffLabel
from silvertyper.Data.Label.FFTermLabel import FFTermLabel
from silvertyper.Data.Entry.FFPara import MultiFourierParaEntry as MFourierEntry

class LammpsDihedralEntry(DihedralLineParser):
    _strTemplate = "dihedral_coeff {} fourier {} {}"
    _pSetStrTemplate = "{:.3f}\t{}\t{:.1f}"

    def __init__(self,dtype,
                 Vn,gamma,n):
        """
        Amber dihedral term
        Energy defined in multiple Fourier series:
        E(φ) = Sum(Vn/d * (1+ cos(n*φ - γ)))

        Vn      - Vn in kcal/mol, half of actual barrier
        gamma   - γ in degree
        n       - n
        """
        data = MFourierEntry(dtype,Vn,1,gamma,n)
        DihedralLineParser.__init__(self,data)

    def __str__(self):
        """
        One line for each parameter set
        """
        def genSingleLine(pSet):
            Vn = pSet.Vn
            gamma = pSet.gamma
            n = int(pSet.n)
            line = self._pSetStrTemplate.format(
                Vn,n,gamma
            )
            return line
        
        paraStr = ""
        for pSet in self.data.paraSets[:-1]:
            lineStr = genSingleLine(pSet)
            paraStr += (lineStr + "\t")
        paraStr = paraStr.strip()
        fullStr = self._strTemplate.format(
            self.type,
            len(self.data.paraSets),
            paraStr
        )
        
        return fullStr
    
    @classmethod
    def fromLine(cls,line):
        #dihedral_coeff 739 fourier 3 0.235 2 180.0 0.5 3 0.0 1.302 1 0.0
        items = line.split()
        entryType = items[1]
        nParaSet = int(items[3])
        Vn,n,gamma = items[index:index+3]
        Vn = float(Vn)
        n = int(n)
        gamma = float(gamma)
        newEntry = cls(entryType,Vn,gamma,n)
        if nParaSet > 1:
            for index in range(7,len(items),3):
                Vn,n,gamma = items[index:index+3]
                Vn = float(Vn)
                n = int(n)
                gamma = float(gamma)
                pSet = cls(entryType,Vn,gamma,n)
                newEntry.data.merge(pSet)
        return newEntry