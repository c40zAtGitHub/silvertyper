from .FileInterface import File

class ChargeFile(File):
    """
    A file of multiple lines
    Each contains a float indicating the partial charge
    of each atom in a molecule
    """
    def __init__(self,charge:list[float]):
        self.chargeList = charge

    @classmethod
    def fromStream(cls,fileContent):
        chargeList = [float(c) for c in fileContent.splitlines()]
        return cls(chargeList)

    def toStream(self):
        displayFormat = "{:.4f}"
        chargeStr = [displayFormat.format(c) for c in self.chargeList]
        fileContent = "\n".join(chargeStr)
        return fileContent