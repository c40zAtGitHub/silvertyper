class LAMMPSDataFile:
    _template = """LAMMPS Data File

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

def __init__(self,refDicts):
    self.aTypes = []
    self.atoms = []
    self.bonds = []
    self.angles = []
    self.dihedrals = []
    self.impropers = []
    self.vdws = []

def __str__(self):
    pass

def addAtom(self,atom):
    pass

def addBond(self,bond):
    pass

def addAngle(self,angle):
    pass

def addDihedral(self,dihedral):
    pass

def addImproper(self,improper):
    pass

def addVdw(self,vdw):
    pass

    

@classmethod
def fromSTFragment(cls,stFrag):
    pass