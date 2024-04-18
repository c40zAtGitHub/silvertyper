from __future__ import annotations

from collections import deque

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .MolGraph import MolGraph
    
class SerialMGIter:
    def __init__(self,parent : MolGraph):
        self.parent = parent

    def __iter__(self):
        self.cur = 0
        self.max = len(self.parent)
        return self

    def __next__(self):
        if self.cur == self.max:
            raise StopIteration
        else:
            data =  self.parent[self.cur]
            self.cur += 1
            return data
        
class BFSFloodMGIter:
    """
        A custom bfs iterator over nodes of MolGraph
        starting with certain node indices initialized
        in queue in order given in startingPoints

        This iterator is used to manually align 
        two fragments
    """
    def __init__(self,
                 graph : MolGraph,
                 startIndices : list[int]):
        self._graph = graph
        self._visited = list(startIndices)
        self._dq = deque(startIndices)
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._dq) == 0:
            raise StopIteration
        else:
            dqpop = self._dq.popleft()
            newNeighbrs = [node for node in self._graph.neighbors(dqpop)\
                            if node not in self._visited]
            for neighbr in newNeighbrs:
                self._dq.append(neighbr)
                self._visited.append(neighbr)
            return self._graph[dqpop]

