from .BaseDataEntry import BaseDataEntry

class AtomicEntry(BaseDataEntry):
    def __init__(self, atomID, atomType, x, y, z):
        super().__init__(atomID, atomType, x, y, z)

    def __str__(self):
        return f"{self.atomID}\t{self.atomType}\t{self.x}\t{self.y}\t{self.z}"
    
    def __next__(self):
        yield self.atomID
        yield self.atomType
        yield self.x
        yield self.y
        yield self.z
        raise StopIteration