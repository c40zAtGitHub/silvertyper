import numpy as np
from openbabel import openbabel as ob

class OBSMARTSearcher:
    def __init__(self,obmol):
        self.mol = obmol 


    def find(self,smartsPatterm):
        matches  = self.findall(smartsPatterm)
        if len(matches) > 0:
            return matches[0]
        else:
            return []

    def findall(self,smartsPatterm):
        obSmartPattern = ob.OBSmartsPattern()
        obSmartPattern.Init(smartsPatterm)
        matchFound = obSmartPattern.Match(self.mol)
        if matchFound is True:
            obMatchList = list(obSmartPattern.GetUMapList())
            matchlist = [np.array(match,dtype=np.int16)-np.ones(len(match),dtype=np.int16) for match in obMatchList]
            return matchlist
        else:
            return []