"""
The interface for a file object
"""
class File:
    @classmethod
    def fromFile(cls,fileName):
        with open(fileName,'r') as fhdler:
            fcontent = fhdler.read()

        fobj = cls.fromStream(fcontent)
        return fobj
    
    @classmethod
    def fromStream(cls,fileContent):
        raise NotImplementedError
    
    def toStream(self):
        raise NotImplementedError