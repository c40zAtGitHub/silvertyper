#Mixins of the ObMolWrapper class
from .ObMolConstructor import ObMolConstructor
from .ObMolConverter import ObMolConverter
from .ObSmartSearch import ObSmartSearch
from .ObSubmol import ObSubmol



class ObMolWrapper(ObMolConstructor,
                   ObMolConverter,
                   ObSmartSearch,
                   ObSubmol):
    """
    The openbabel OBMol wrapper with the 
    following functions:
    #   ObMolCreation
    #   construction from XYZFile
    #   conversion to a GraphMol object

    #   Search
    #   Search fragments based on given pattern
    """
    def __init__(self,obmolObj):
        self.obmol = obmolObj

    def __getstate__(self):
        state = self.toDict()
        return state

    def __setstate__(self,state):
        mol = ObMolConstructor.fromDict(state)
        self.obmol = mol.obmol


    