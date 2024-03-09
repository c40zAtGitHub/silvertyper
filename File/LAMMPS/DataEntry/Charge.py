from .BaseDataEntry import BaseDataEntry

class ChargeEntry(BaseDataEntry):
    def __init__(self, atomID, atomType, q, x, y, z):
        super().__init__(atomID, atomType, x, y, z)
        self.charge = q

    @property
    def q(self):
        return self.charge

    def __str__(self):
        return f"{self.atomID}\t{self.atomType}\t{self.charge}\t{self.x}\t{self.y}\t{self.z}"
    
    def __next__(self):
        yield self.atomID
        yield self.atomType
        yield self.charge
        yield self.x
        yield self.y
        yield self.z
        raise StopIteration