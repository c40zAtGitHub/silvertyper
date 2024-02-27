from .STFragment import STFragment

from silvertyper.File import XYZFile
from silvertyper.Utilities.AtomicMassData import atomSymbols

class STMolConverter:
    @classmethod
    def fromXYZFile(cls,xyzFileName,chargeFileName=None):
        with open(xyzFileName) as xyz:
            xyzContent = xyz.read()
        xyzObj = XYZFile.fromStream(xyzContent)
        
        exyzLines = xyzObj.atomCoords.splitlines()
        exyzTuples = []
        for line in exyzLines:
            aSymbol,x,y,z = line.split()
            try:
                aNum = int(aSymbol)
            except ValueError:
                aNum = atomSymbols.index(aSymbol) + 1

            x = float(x)
            y = float(y)
            z = float(z)
            exyzTuples.append((aNum,x,y,z))

        if chargeFileName is not None:
            charges = cls.readChargeFile(chargeFileName)
        else:
            charges = None

        stFrag = STFragment(exyzTuples,charges)
        return stFrag

    @classmethod
    def readChargeFile(self,chargeFileName):
        with open(chargeFileName) as cfile:
            charges = cfile.read()

        chargeList = [float(c) for c in charges.splitlines()]
        return chargeList

    @classmethod
    def toLAMMPSData(cls,stmol):
        pass

    @classmethod
    def toFullSMILES(cls,stmol):
        """
        Convert obmol (containing single molecule) to
        a (very redundant) SMILES expression that can
        be used for fitting
        """
        pass