from __future__ import annotations

from silvertyper.File import XYZFile
from silvertyper.Mol.STFragment import STFragment


#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.OBInterface.OBMolBondingRule import OBMBRule

class STRuledMolConverter:
    @classmethod
    def RuledMolFromXYZFile(self,
                            xyzFile:str,
                            rules:OBMBRule):
        with open(xyzFile) as xyzf:
            xyzContent = xyzf.read()
        xyzObj = XYZFile.fromStream(xyzContent)
        xyzTuples = xyzObj.toEXYZTuples()
        mol = STFragment(xyzTuples,
                         perceiveBC=False,
                         perceiveBO=False)
        conIndices = rules.conIndices(mol.obmol)
        conView = mol.subView(conIndices)
        conView.vmol.obmol.ConnectTheDots()
        conView.syncVmol()

        orderIndices = rules.orderIndices(mol.obmol)
        orderView = mol.subView(orderIndices)
        orderView.vmol.obmol.ConnectTheDots()
        orderView.vmol.obmol.PerceiveBondOrders()
        orderView.syncVmol()
        return mol



