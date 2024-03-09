import networkx as nx

from .STMolGraphIter import STSerialMGIter

from silvertyper.Utilities.AtomicMassData import atomSymbols

class STAtomEntry:

    def __init__(self,
                 anum,
                 atype=None,
                 charge=None,
                 ):
        self.atomNum = anum
        self.atomSymbol = atomSymbols[anum-1]
        self.type = atype
        self.ffname = None
        
        if charge is None:
            self.charge = 0.0
        else:
            self.charge = charge

class STMolGraph:
    def __init__(self):
        self._graph = nx.Graph()

    def __len__(self):
        return len(self._graph)
    
    def __getitem__(self,index):
        return self._graph.nodes[index]['data']

    #data insertion
    def addAtom(self,aIndex,aNum,atype=None,charge=None):
        newEntry = STAtomEntry(aNum,atype=atype,charge=charge)
        self._graph.add_node(aIndex,data=newEntry)

    def addBond(self,aIndex1,aIndex2):
        self._graph.add_edge(aIndex1,aIndex2)

    #data access and iteration
    #use obj.atoms[index] or obj[index] to access a specific data node
    def __iter__(self):
        return self.atoms
    
    @property
    def atoms(self):
        return STSerialMGIter(self)

    @property
    def bonds(self):
        return self._graph.edges
    
    def neighbors(self,index):
        return self._graph.neighbors(index)
    
    @property
    def components(self):
        return nx.connected_components(self._graph)

