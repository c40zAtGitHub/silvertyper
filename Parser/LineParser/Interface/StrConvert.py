class StrConvertInterface:
    _strTemplate = ""
    def __str__(self):
        raise NotImplementedError
    
    @classmethod
    def fromString(cls,entryString):
        raise NotImplementedError