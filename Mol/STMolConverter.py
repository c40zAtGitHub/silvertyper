from .STFragment import STFragment

from silvertyper.File import XYZFile


class STMolConverter:
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

        stFrag = STFragment(exyzTuples,charges=charges,perceiveBO=perceiveBO)
        return stFrag

    @classmethod
    def readChargeFile(self,chargeFileName):
        with open(chargeFileName) as cfile:
            charges = cfile.read()

        chargeList = [float(c) for c in charges.splitlines()]
        return chargeList

    @classmethod
    def toLAMMPSData(cls,stfrag):
        pass

    @classmethod
    def toFullSMILES(cls,stmol):
        """
        Convert obmol (containing single molecule) to
        a (very redundant) SMILES expression that can
        be used for fitting
        """
        pass
