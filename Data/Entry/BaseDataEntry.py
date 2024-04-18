class BaseDataEntry:
    def __init__(self,etype):
        self.type = etype

    #support for quickly creating a list of
    #all parameters passing which as positional
    #arguments to the class will restore the instance
    def __iter__(self):
        yield self.type

    @property
    def parameters(self):
        return tuple(self)
    