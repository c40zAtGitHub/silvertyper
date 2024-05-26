from openbabel import openbabel as ob
class ObSubmol:

    def submol(self,atomIndices:list[int]):
        # Create a new OBMol object
        mol = self.obmol
        slicedMol = ob.OBMol()
        
        # Add atoms with the given indices to the new molecule
        for idx in atomIndices:
            atom = mol.GetAtom(idx)
            if atom is not None:
                newAtom = atom.Clone()
                slicedMol.AddAtom(newAtom)

        # Restore bonds between atoms
        for sliceIdx,parentIdx in enumerate(atomIndices):
            parentAtom = mol.GetAtom(parentIdx)
            for nbrAtom in ob.OBAtomAtomIter(parentAtom):
                nbrIdx = nbrAtom.GetIdx()
                try:
                    sliceNbrIdx = atomIndices.index(nbrIdx)
                except ValueError:
                    continue
                
                bond = parentAtom.GetBond(nbrAtom)
                bondOrder = bond.GetBondOrder()
                slicedMol.AddBond(sliceIdx, sliceNbrIdx, bondOrder)
        return slicedMol
