import numpy as np
from openbabel import openbabel as ob

class ObSmartSearch:

    def find(self,smartsPatterm):
        matches  = self.findall(smartsPatterm)
        if len(matches) > 0:
            return matches[0]
        else:
            return []

    def findall(self,smartsPatterm:str):
        obSmartPattern = ob.OBSmartsPattern()
        obSmartPattern.Init(smartsPatterm)
        matchFound = obSmartPattern.Match(self.obmol)
        if matchFound is True:
            obMatchList = list(obSmartPattern.GetUMapList())
            matchlist = [np.array(match)-np.ones(len(match)) for match in obMatchList]
            return matchlist
        else:
            return []