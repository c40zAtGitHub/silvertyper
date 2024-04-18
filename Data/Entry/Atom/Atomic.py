from ..BaseDataEntry import BaseDataEntry

class AtomicEntry(BaseDataEntry):
    def __init__(self, atype, x, y, z):
        super().__init__(atype)
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield from super().__iter__()
        yield self.x
        yield self.y
        yield self.z

