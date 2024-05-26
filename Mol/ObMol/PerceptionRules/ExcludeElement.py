from silvertyper.Utilities.AtomicMassData import atomSymbols
from .PerceptionRule import PerceptionRule

class ExcludeElement(PerceptionRule):
    """
    Omits bond formation among atoms of certain element
    """
    def __init__(self,
                 conElements = None,
                 orderElements = None):
        super().__init__()

        if conElements is None:
            conElements = []
        if orderElements is None:
            orderElements = []

        self.conElements = conElements
        self.orderElements = orderElements

    def __con__(self,obatom):
        """
        Judgement function that determines whether an atom
        should be included in atom connection determination
        returns True or False
        """
        aNum = obatom.GetAtomicNum()
        symbol = atomSymbols[aNum-1]
        if symbol in self.conElements:
            return False
        else:
            return True

    def __order__(self,obatom):
        """
        Judgement function that determines whether an atom
        should be included in bond order determination
        returns True or False
        """
        aNum = obatom.GetAtomicNum()
        symbol = atomSymbols[aNum-1]
        if symbol in self.orderElements:
            return False
        else:
            return True