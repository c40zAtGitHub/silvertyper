from .Interface.DataWrap import DataWrapInterface as DataWrap
from .Interface.StrConvert import StrConvertInterface as StrConvert

class LineParser(DataWrap,StrConvert):
    _strTemplate = None
    _attrLink = {}
    def __init__(self,data):
        DataWrap.__init__(self,data,self._attrLink)

    @classmethod
    def nullParser(cls):
        return cls(None)
    
    
    
    
