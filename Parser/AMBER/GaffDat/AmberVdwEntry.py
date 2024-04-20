"""
Line parser for atom type definition section
"""
from .AmberEntry import AmberEntry
from silvertyper.Parser.LineParser.BadiLineParser import VdWLineParser

from silvertyper.Data.Label.FFTermLabel import FFTermLabel
from silvertyper.Data.Label.AtomType.GaffAtomType import GAFFAtomType as GaffLabel
from silvertyper.Data.Entry.FFPara.Pair import LJParaEntry

class AmberVdwEntry(AmberEntry,VdWLineParser):
    _keyLength = 2
    _strTemplate = "{}\t{:.4f}\t{:.4f}\t{}"
    def __init__(self,atype,re,eps,description):
        """
        Van der Waals interaction term
        the pairwise re and epsilon is combined as
        re_ij = 1/2 * (re_i + re_j);
        eps_ij = sqrt(eps_i*eps_j)
        see https://ambermd.org/vdwequation.pdf for details

        atype   - atom type (in corresponding type label)
        re      - atom radius in Angstrom
        eps     - well depth parameter (epsilon) in kcal/mol
        """
        AmberEntry.__init__(self,description)
        data = LJParaEntry(atype,eps,re)
        VdWLineParser.__init__(self,data)

    def __str__(self):
        return self._strTemplate.format(
            self.type,
            self.re,
            self.epsilon,
            self.description
        )

    @classmethod
    def fromString(cls,entryString):
        key,elements = cls.keyElements(entryString)
        btype = FFTermLabel(key,LabelType=GaffLabel)
        re = float(elements[0])
        eps = float(elements[1])
        desp = " ".join(elements[2:])
        return cls(btype,re,eps,description = desp)