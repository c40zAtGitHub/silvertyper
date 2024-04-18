from ..BaseDataEntry import BaseDataEntry

class LJParaEntry(BaseDataEntry):
    def __init__(self, etype, epsilon, re):
        super().__init__(etype)
        self.epsilon = epsilon
        self.re = re

    def __iter__(self):
        yield from super().__iter__()
        yield self.epsilon
        yield self.re