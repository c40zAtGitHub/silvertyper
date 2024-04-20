from .LineParser import LineParser
from . import link_attributes

@link_attributes
class BondLineParser(LineParser):
    _attributes = {"type":"type","Kr":"K","re":"eq"}

@link_attributes
class AngleLineParser(LineParser):
    _attributes = {"type":"type","Kt":"K","te":"eq"}

@link_attributes
class DihedralLineParser(LineParser):
    _attributes = ["type","Vn","d","gamma","n"]

@link_attributes
class FourierImproperLineParser(LineParser):
    _attributes = ["type","Vn","gamma","n"]

@link_attributes
class CvffImproperLineParser(LineParser):
    _attributes = ["type","Vn","gamma","n"]

@link_attributes
class VdWLineParser(LineParser):
    _attributes = ["type","epsilon","re"]