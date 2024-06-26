from openbabel import openbabel as ob

class PerceptionRule:
    """
    Base rule interface used by Mol that defines
    the bond forming behavior of different portion of an obmol system
    """
    def __init__(self):
        self.guessBondCon = True
        self.guessBondOrder = True

    def __con__(self,obatom):
        """
        Judgement function that determines whether an atom
        should be included in atom connection determination
        returns True or False
        """
        raise NotImplementedError
    

    def __order__(self,obatom):
        """
        Judgement function that determines whether an atom
        should be included in bond order determination
        returns True or False
        """
        raise NotImplementedError

    def allIndices(self,obmol):
        return list(range(obmol.NumAtoms()))


    def conIndices(self,obmol):
        """
        Atom indices that participates in bond connection perception
        """
        indices = []
        if self.guessBondCon is True:
            for atom in ob.OBMolAtomIter(obmol):
                if self.__con__(atom):
                    indices.append(atom.GetIdx()-1)
        return indices

    def orderIndices(self,obmol):
        """
        Atom indices that participates in bond order perception
        """
        indices = []
        if self.guessBondOrder is True:
            for atom in ob.OBMolAtomIter(obmol):
                if self.__order__(atom):
                    indices.append(atom.GetIdx()-1)
        return indices
    
    def nobondIndices(self,obmol):
        """
        Atom indices that does not participate bonding
        Should be the atoms not in conIndices
        """
        return [index for index in self.allIndices(obmol)\
                 if index not in self.conIndices(obmol)]

