from ..BaseDataEntry import BaseDataEntry

class FourierParaSet:
    def __init__(self,Vn,d,gamma,n):
        self.Vn = Vn
        self.d = d
        self.gamma = gamma
        self.n = n
        

class FourierParaEntry(BaseDataEntry,FourierParaSet):
    def __init__(self, etype, Vn, d, gamma, n):
        """
        Fourier dihedral term
        Energy defined in the below expression:
        E(φ) = Vn/d * (1+ cos(n*φ - γ))

        etype   - type label
        Vn      - half of actual barrier
        gamma   - γ in rad
        n       - n
        d       - divider that scales the potential barrier

        """
        BaseDataEntry.__init__(self,etype)
        FourierParaSet.__init__(self,d,Vn,gamma,n)

    def __iter__(self):
        yield from super().__iter__()
        yield self.Vn
        yield self.d
        yield self.gamma
        yield self.n


class MultiFourierParaEntry(BaseDataEntry):
    _vErrMsg = "Value of {attr} is ambiguous when the entry holds multiple\
        set of values.\nPlease access {attr} of individual entry instead\
        using expressions like entry[0].{attr}"
    
    def __init__(self, etype, Vn, d, gamma, n,*args):
        """
        Fourier dihedral term
        Energy defined in the below expression:
        E(φ) = Sum_i(Vn_i/d_i * (1+ cos(n_i*φ - γ_i)))

        etype   - type label
        Vn      - half of actual barrier
        d       - divider that scales the potential barrier
        gamma   - γ in rad
        n       - n
        [Vn2,d2,gamma2,n2,...]   - parameters (in groups of 4) for other Fourier series
        """
        super().__init__(etype)
        self.paraSets = [FourierParaSet(Vn,d,gamma,n)]
        for i in range(0,len(args),4):
            newParaSet = FourierParaSet(*args[i:i+4])
            self.paraSets.append(newParaSet)

    def __len__(self):
        return len(self.paraSets)
    
    def __iter__(self):
        yield from super().__iter__()
        for pSet in self.paraSets:
            yield pSet.Vn
            yield pSet.d
            yield pSet.gamma
            yield pSet.n

    @property
    def MULTIVALUE(self):
        if len(self) > 1:
            return True
        else:
            return False
        
    def merge(self,otherEntry):
        if self.type == otherEntry.type:
            for item in otherEntry.paraSets:
                self.paraSets.append(item)
    
    @property
    def Vn(self):
        if self.MULTIVALUE is True:
            raise ValueError(self._vErrMsg.format(attr="Vn"))
        else:
            return self.paraSets[0].Vn
    
    @property
    def d(self):
        if self.MULTIVALUE is True:
            raise ValueError(self._vErrMsg.format(attr="divider"))
        else:
            return self.paraSets[0].d
    
    @property
    def gamma(self):
        if self.MULTIVALUE is True:
            raise ValueError(self._vErrMsg.format(attr="gamma"))
        else:
            return self.paraSets[0].gamma
    
    @property
    def n(self):
        if self.MULTIVALUE is True:
            raise ValueError(self._vErrMsg.format(attr="n"))
        else:
            return abs(self.paraSets[0].n)