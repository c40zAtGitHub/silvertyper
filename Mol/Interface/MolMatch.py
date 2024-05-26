from ..GraphMol.Iterator.AtomIter import BFSAtomIter

class MolMatch:
    def match(self,otherMol,startSmi = None):
        if len(self) != len(otherMol):
            return False

        #priority of starting smiles:
        #   startSmi > otherMol.startSmiles > self.startSmiles
        usableSmiles = [smi for smi in [startSmi,
                                        otherMol.startSmiles,
                                        self.startSmiles]\
                        if smi is not None]
        
        #establish the starting smiles pattern
        if len(usableSmiles) == 0:
            errMsg = "A valid starting point smiles pattern is required for mol comparison"
            raise ValueError(errMsg)
        else:
            firstSmi = usableSmiles[0]

        if firstSmi == self.startSmiles:
            selfStIndices = self.startIndices
        else:
            selfStIndices = self.find(firstSmi)

        if len(selfStIndices) == 0:
            return False

        if firstSmi == otherMol.startSmiles:
            otherStIndices = otherMol.startIndices
        else:
            otherStIndices = otherMol.find(firstSmi)

        if len(otherStIndices) == 0:
            return False

        selfFloodIter = BFSAtomIter(self.molgraph,selfStIndices)
        otherFloodIter = BFSAtomIter(otherMol.molgraph,otherStIndices)
        for atomPair in zip(selfFloodIter,otherFloodIter):
            satom,oatom = atomPair
            if satom.atomNum != oatom.atomNum:
                return False
        return True