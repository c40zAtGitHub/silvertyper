class BaseDataEntry:
    def __init__(self,atomID,atomTypeID,x,y,z):
        self.atomID = atomID
        self.atomTypeID = atomTypeID
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError
    
    @property
    def entryTypeID(self):
        return self.atomTypeID
    
    @entryTypeID.setter
    def entryTypeID(self,newID):
        self.atomTypeID = newID