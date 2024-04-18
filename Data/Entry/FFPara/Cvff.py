from ..BaseDataEntry import BaseDataEntry

class CvffParaEntry(BaseDataEntry):
    def __init__(self, etype, Vn, d, n):
        """
        Fourier dihedral term
        Energy defined in the below expression:
        E(φ) = Vn * (1+ d*cos(n*φ))
        etype   - type label
        Vn      - half of actual barrier
        n       - n the period
        d       - -1 or 1
        """
        BaseDataEntry.__init__(self,etype)
        self.Vn = Vn
        self.d = d
        self.n = n

    def __iter__(self):
        yield from super().__iter__()
        yield self.Vn
        yield self.d
        yield self.n