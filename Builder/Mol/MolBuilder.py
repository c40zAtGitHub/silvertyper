from __future__ import annotations
from silvertyper.Mol import Mol
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.File.XYZFile import XYZFile
    from silvertyper.File.ChargeFile import ChargeFile

class MolBuilder:
    @classmethod
    def fromFile(cls,
                 xyzFileObj:XYZFile,
                 chargeFileObj:ChargeFile = None,
                 perceiveBO:bool = False):
        exyzTuples = xyzFileObj.toEXYZTuples()

        if chargeFileObj is not None:
            charges = chargeFileObj.chargeList
        else:
            charges = None

        mol = Mol.fromData(exyzTuples,charges=charges,perceiveBO=perceiveBO)
        return mol