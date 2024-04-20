from .Interface.DataWrap import DataWrapInterface as DataWrap
from .Interface.StrConvert import StrConvertInterface as StrConvert

class LineParser(DataWrap,StrConvert):
    def __init__(self,data):
        DataWrap.__init__(self,data)

    @classmethod
    def nullParser(cls):
        return cls()
    
    
    
    
