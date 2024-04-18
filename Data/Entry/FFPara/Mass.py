from ..BaseDataEntry import BaseDataEntry

class MassParaEntry(BaseDataEntry):
    def __init__(self, etype, mass):
        """
        etype - atom type label
        mass - atomic mass in amu
        """
        super().__init__(etype)
        self.mass = mass

    def __iter__(self):
        yield from super().__iter__()
        yield self.mass

class MassPolarParaEntry(MassParaEntry):
    def __init__(self,atype, mass, polarizability):
        super().__init__(atype,mass)
        self.polarizability = polarizability

    def __iter__(self):
        yield from super().__iter__()
        yield self.polarizability





    
