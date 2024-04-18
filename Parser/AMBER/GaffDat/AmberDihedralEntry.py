"""
Line parser for dihedral parameter section
"""
from .AmberEntry import AmberEntry
from silvertyper.Parser.LineParser.BadiLineParser import DihedralLineParser

from silvertyper.Data.Label.AtomType.GaffAtomType import GaffAtomType as GaffLabel
from silvertyper.Data.Label.FFTermLabel import FFTermLabel
from silvertyper.Data.Entry.FFPara import MultiFourierParaEntry as MFourierEntry

class AmberDihedralEntry(AmberEntry,DihedralLineParser):
    _keyLength = 11
    _strTemplate = "{}\t{}\t{}"
    _pSetStrTemplate = "{}\t{:.3f}\t{:.3f}\t{:.3f}"

    def __init__(self,dtype,
                 d,Vn,gamma,n,
                 description = None):
        """
        Amber dihedral term
        Energy defined in multiple Fourier series:
        E(φ) = Sum(Vn/d * (1+ cos(n*φ - γ)))

        d       - divider of Vn
        Vn      - Vn in kcal/mol, half of actual barrier
        gamma   - γ in degree
        n       - n
        """
        AmberEntry.__init__(self,description)
        data = MFourierEntry(dtype,Vn,d,gamma,n)
        DihedralLineParser.__init__(self,data)

    def __str__(self):
        """
        One line for each parameter set
        """
        def genSingleLine(pSet,negN = False):
            Vn = pSet.Vn
            gamma = pSet.gamma
            d = pSet.d
            n = pSet.n
            if negN is True:
                n *= -1
            line = self._pSetStrTemplate.format(
                d,Vn,gamma,n
            )
            return line
        
        fullStr = ""
        for pSet in self.data.paraSets[:-1]:
            lineStr = genSingleLine(pSet,negN=True)
            fullStr += (lineStr + "\n")
        lastLine = genSingleLine(self.data.paraSets[-1])
        fullStr += lastLine
        return fullStr
    
    @classmethod
    def fromLine(cls,lines):
        def processSingleLine(line):
            key,elements = cls.keyElements(line)
            dtype = FFTermLabel(key,LabelType=GaffLabel)
            d = int(elements[0])
            Vn = float(elements[1])
            gamma = float(elements[2])
            n = abs(float(elements[3]))
            desp = " ".join(elements[4:])
            return (dtype,d,Vn,gamma,n,desp)
        
        if isinstance(lines,str):
            #single line input
            dtype,d,Vn,gamma,n,desp = processSingleLine(lines)
            obj = cls(dtype,d,Vn,gamma,n,description = desp)
        elif isinstance(lines,list):
            #multi line input
            dtype,d,Vn,gamma,n,desp = processSingleLine(lines[0])
            obj = cls(dtype,d,Vn,gamma,n,description = desp)
            for line in lines[1:]:
                dtype,d,Vn,gamma,n,desp = processSingleLine(line)
                obj1 = cls(dtype,d,Vn,gamma,n,description = desp)
                obj.data.merge(obj1)
        return obj