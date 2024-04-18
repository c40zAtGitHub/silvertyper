from .Fragment import Fragment

from silvertyper.File import XYZFile


class MolConverter:
    @classmethod
    def fromXYZFile(cls,xyzFileName,
                    chargeFileName = None,
                    perceiveBO = False):
        with open(xyzFileName) as xyz:
            xyzContent = xyz.read()
        xyzObj = XYZFile.fromStream(xyzContent)
        exyzTuples = xyzObj.toEXYZTuples()

        if chargeFileName is not None:
            charges = cls.readChargeFile(chargeFileName)
        else:
            charges = None

        frag = Fragment(exyzTuples,charges=charges,perceiveBO=perceiveBO)
        return frag

    @classmethod
    def readChargeFile(self,chargeFileName):
        with open(chargeFileName) as cfile:
            charges = cfile.read()

        chargeList = [float(c) for c in charges.splitlines()]
        return chargeList

    @classmethod
    def toLAMMPSData(cls,frag):
        pass

    @classmethod
    def toFullSMILES(cls,mol):
        """
        Convert obmol (containing single molecule) to
        a (very redundant) SMILES expression that can
        be used for fitting
        """
        pass
