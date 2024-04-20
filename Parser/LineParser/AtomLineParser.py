from . import link_attributes
from .LineParser import LineParser

@link_attributes
class AtomicLineParser(LineParser):
    _attributes = ["type","x","y","z"]

@link_attributes
class ChargeLineParser(LineParser):
    _attributes = ["type","x","y","z","charge","q"]