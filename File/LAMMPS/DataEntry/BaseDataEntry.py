class BaseDataEntry:
    def __init__(self,atomID,atomType,x,y,z):
        self.atomID = atomID
        self.atomType = atomType
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError