#iteration mixins for forcefield term generation
#asserted property (or member) for parent:
#   mol -   a networkx.Graph instance with atom indices as nodes
#           and the connection of atoms as edges

#imports
from itertools import combinations

#mol wrapper that facilitates networkx data access
class MolWrapper:
    def __init__(self,mol):
        self.mol = mol

    @property
    def atoms(self):
        return list(self.mol.nodes)

    def neighbors(self,atomNode):
        neibrNodes = list(self.mol.neighbors(atomNode))
        neibrNodes.sort()
        return neibrNodes

    @property
    def bonds(self):
        return list(self.mol.edges)

class BondIterMixin:
    @property
    def bonds(self):
        mol = MolWrapper(self.mol)
        for bond in mol.bonds:
            yield bond

class AngleIterMixin:
    @property
    def angles(self):
        mol = MolWrapper(self.mol)
        for atom in mol.atoms:
            neibrs = mol.neighbors(atom)
            numNeibr = len(neibrs)
            if numNeibr < 2:
                continue
            else:
                for pair in combinations(neibrs,2):
                    yield (pair[0],atom,pair[1])

class DihedralIterMixin:
    @property
    def dihedrals(self):
        mol = MolWrapper(self.mol)
        for bond in mol.bonds:
            atom1,atom2 = bond
            a1Neighbrs = [nei for nei in mol.neighbors(atom1) if nei != atom2]
            a2Neighbrs = [nei for nei in mol.neighbors(atom2) if nei != atom1]
            for a1n in a1Neighbrs:
                for a2n in a2Neighbrs:
                    if a1n != a2n:
                        yield (a1n,atom1,atom2,a2n)

class ImpTorsionIterMixin:
    @property
    def impropers(self):
        #focus on atoms that have three bonds only
        mol = MolWrapper(self.mol)
        for atom in mol.atoms:
            neibrs = mol.neighbors(atom)
            if len(neibrs) == 3:
                a1,a2,a3 = neibrs
                yield (a1,a2,atom,a3)
                yield (a2,a3,atom,a1)
                yield (a3,a1,atom,a2)
            
        
