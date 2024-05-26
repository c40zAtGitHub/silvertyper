from __future__ import annotations

from itertools import combinations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..GraphMol import GraphMol

class BondIter:
    @property
    def bonds(self):
        gmol:GraphMol = self.parent
        for bond in gmol.bonds:
            yield bond

class AngleIter:
    @property
    def angles(self):
        gmol:GraphMol = self.parent
        for atom in gmol.atoms:
            neibrs = gmol.neighbors(atom)
            numNeibr = len(neibrs)
            if numNeibr < 2:
                continue
            else:
                for pair in combinations(neibrs,2):
                    yield (pair[0],atom,pair[1])

class DihedralIter:
    @property
    def dihedrals(self):
        gmol:GraphMol = self.parent
        for bond in gmol.bonds:
            atom1,atom2 = bond
            a1Neighbrs = [nei for nei in gmol.neighbors(atom1) if nei != atom2]
            a2Neighbrs = [nei for nei in gmol.neighbors(atom2) if nei != atom1]
            for a1n in a1Neighbrs:
                for a2n in a2Neighbrs:
                    if a1n != a2n:
                        yield (a1n,atom1,atom2,a2n)

class ImpTorsionIter:
    @property
    def impropers(self):
        #focus on atoms that have three bonds only
        gmol:GraphMol = self.parent
        for atom in gmol.atoms:
            neibrs = gmol.neighbors(atom)
            if len(neibrs) == 3:
                a1,a2,a3 = neibrs
                yield (a1,a2,atom,a3)
                yield (a2,a3,atom,a1)
                yield (a3,a1,atom,a2)


class BadiIter(BondIter,
               AngleIter,
               DihedralIter,
               ImpTorsionIter):
    
    def __init__(self,mol:GraphMol):
        self.parent = mol

    @property
    def terms(self):
        for bond in self.bonds:
            yield bond
        for angle in self.angles:
            yield angle
        for dihedral in self.dihedrals:
            yield dihedral
        for imp in self.impropers:
            yield imp