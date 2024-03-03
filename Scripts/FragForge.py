import sys

from silvertyper.Mol.STMolConverter import STMolConverter
from silvertyper.ForcefieldTyper.GAFF import gaffTyper

# fragXYZFile = sys.argv[1]
# try:
#     chargeFile = sys.argv[2]
# except IndexError:
#     chargeFile = None

fragXYZFile = "water.xyz"
chargeFile = None

mol = STMolConverter.fromXYZFile(fragXYZFile,chargeFileName=chargeFile)
gaffTyper.assignAtomType(mol)

for atom in mol.atoms:
    print(atom.type)

mol.dump("water.pickle")
