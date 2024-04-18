from ..BaseDataEntry import BaseDataEntry

class HarmonicParaEntry(BaseDataEntry):
    def __init__(self, etype, K, eq):
        """
        Forcefield terms in the following form:
        E(r) = K*(r-eq)**2

        etype   - type label
        K  - the half of force constant
        eq - the equilibrium point (distance, angle, etc.)

        """
        super().__init__(etype)
        self.K = K
        self.eq = eq

    def __iter__(self):
        yield from super().__iter__()
        yield self.K
        yield self.eq