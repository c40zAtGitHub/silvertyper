from . import link_attributes
from .LineParser import LineParser

@link_attributes
class AtomMassLineParser(LineParser):
    _attributes = ["type","mass"]

@link_attributes
class AtomMassPolarLineParser(LineParser):
    _attributes = ["type","mass","polarizability"]