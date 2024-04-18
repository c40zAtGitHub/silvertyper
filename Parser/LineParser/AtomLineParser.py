from .LineParser import LineParser

class AtomicLineParser(LineParser):
    _attrLink = ["type","x","y","z"]

class ChargeLineParser(LineParser):
    _attrLink = ["type","x","y","z","charge","q"]