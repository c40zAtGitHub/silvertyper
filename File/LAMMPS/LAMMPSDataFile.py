import os
from ..FileInterface import File

class LAMMPSDataFile(File):
    _fileTemplate = """LAMMPS Data File

    {natm}  atoms
    {nbnd}  bonds
    {nang}  angles
    {ndhd}  dihedrals
    {nimp}  impropers

    {ntatm}  atom types
    {ntbnd}  bond types
    {ntang}  angle types
    {ntdhd}  dihedral types
    {ntimp}  improper types

    {xlow}    {xhigh} xlo xhi
    {ylow}    {yhigh} ylo yhi
    {zlow}    {zhigh} zlo zhi

Masses

{massesSection}

Atoms

{atomsSection}

Bonds

{bondsSection}

Angles

{anglesSection}

Dihedrals

{dihedralsSection}

Impropers

{impropersSection}

"""
    def __init__(self,
                sysBox,                 #((xlow,ylow,zlow),(xhigh,yhigh,zhigh))
                atomLines,              #list of atom lines
                bondLines,              #list of bond lines
                angleLines,             #list of angle lines
                dihedralLines,          #list of dihedral lines
                improperLines,          #list of improper lines
                massLines = None,       #list of atom mass lines
                nAtomType = None,       #number of atom types
                nBondType = None,       #number of bond types
                nAngleType = None,      #number of angle types
                nDihedralType = None,   #number of dihedral types
                nImproperType = None,   #number of improper types
                ):
        self.box = sysBox

        self.atoms = atomLines
        self.bonds = bondLines
        self.angles = angleLines
        self.dihedrals = dihedralLines
        self.impropers = improperLines

        if massLines is None:
            self.masses = []
        else:
            self.masses = massLines
        
        self.nAtomType = nAtomType
        self.nBondType = nBondType
        self.nAngleType = nAngleType
        self.nDihedralType = nDihedralType
        self.nImproperType = nImproperType

    @property
    def _xyzRange(self):
        return (*self.sysBox[0],*self.sysBox[1])

    def __str__(self):
        sep = os.linesep
        xlow,ylow,zlow,xhigh,yhigh,zhigh = self._xyzRange
        massesSection = sep.join(self.masses)
        atomsSection = sep.join(self.atoms)
        bondsSection = sep.join(self.bonds)
        anglesSection = sep.join(self.angles)
        dihedralsSection = sep.join(self.dihedrals)
        impropersSection = sep.join(self.impropers)

        nAtom = len(self.atoms)
        nBond = len(self.bonds)
        nAngle = len(self.angles)
        nDihedral = len(self.dihedrals)
        nImproper = len(self.impropers)

        fileString = self._fileTemplate.format(
            natm = nAtom,
            nbnd = nBond,
            nang = nAngle,
            ndhd = nDihedral,
            nimp = nImproper,
            ntatm = self.nAtomType,
            ntbnd = self.nBondType,
            ntang = self.nAngleType,
            ntdhd = self.nDihedralType,
            ntimp = self.nImproperType,
            xlow = xlow,
            xhigh = xhigh,
            ylow = ylow,
            yhigh = yhigh,
            zlow = zlow,
            zhigh = zhigh,
            massesSection = massesSection,
            atomsSection = atomsSection,
            bondsSection = bondsSection,
            anglesSection = anglesSection,
            dihedralsSection = dihedralsSection,
            impropersSection = impropersSection
        )
        return fileString

    @classmethod
    def fromStream(cls,fileContent):
        raise NotImplementedError
    
    def toStream(self):
        raise NotImplementedError