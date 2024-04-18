from .LineParser import LineParser

class BondLineParser(LineParser):
    _attrLink = {"type":"type","Kr":"K","re":"eq"}

class AngleLineParser(LineParser):
    _attrLink = {"type":"type","Kt":"K","te":"eq"}

class DihedralLineParser(LineParser):
    _attrLink = ["type","Vn","d","gamma","n"]

class FourierImproperLineParser(LineParser):
    _attrLink = ["type","Vn","gamma","n"]

class CvffImproperLineParser(LineParser):
    _attrLink = ["type","Vn","gamma","n"]