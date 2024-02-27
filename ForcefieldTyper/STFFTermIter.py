from silvertyper.Mixins.STFFTermIterMixin import BondIterMixin,AngleIterMixin,DihedralIterMixin,ImpTorsionIterMixin


class STFFIter(BondIterMixin,
              AngleIterMixin,
              DihedralIterMixin,
              ImpTorsionIterMixin):
    def __init__(self,mol):
        super().__init__()
        self.mol = mol
        self.graph = mol.molgraph
        #mol should have info on atom, GAFF_Atype, connectivity graph

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


