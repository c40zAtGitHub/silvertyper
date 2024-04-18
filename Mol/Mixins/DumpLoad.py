import pickle
class DumpLoadMixin:
    """
    Grant the class ability to:
    1. dump its instances as a binary file
        (a instance method)
    2. load its instances from binary files
        (a class method)
    """
    def dump(self,bFileName):
        with open(bFileName,'wb+') as bfile:
            pickle.dump(self,bfile)

    @classmethod
    def load(cls,bFileName):
        with open(bFileName,'rb') as bfile:
            bObj = pickle.load(bfile)

        if type(bObj) is cls:
            return bObj
        
        else:
            ErrMessage = "Object in binary file {} is not an instance of {}".format(
                bFileName,cls
                )
            
            raise TypeError(ErrMessage)

