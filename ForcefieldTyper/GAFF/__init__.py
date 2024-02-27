import os

from silvertyper.ForcefieldTyper.STSmartsDict import STSmartsDict
from silvertyper.ForcefieldTyper.STFFTyper import STForcefieldTyper
_dirName = os.path.dirname(__file__)
_gaffPrmDir = os.path.join(_dirName,"gaff.prm")
_gaffSmartsDict = STSmartsDict.fromPrmFile(_gaffPrmDir)
gaffTyper = STForcefieldTyper(_gaffSmartsDict)