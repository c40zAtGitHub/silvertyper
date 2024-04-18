from .Atomic import AtomicEntry

class ChargeEntry(AtomicEntry):
    def __init__(self, atype, x, y, z, q):
        super().__init__(atype, x, y, z)
        self.charge = q

    def __iter__(self):
        yield from super().__iter__()
        yield self.charge

    @property
    def q(self):
        return self.charge
