class STSmartsDict:
    class PtnTypePair:
        def __init__(self,index,atypes,pattern):
            #the larger the index, the higher the priority
            self.index = index
            self.atomTypes = atypes.split(',')
            self.pattern = pattern
        def __str__(self):
            return "Atom type: {}, pattern: {}".format(self.atomType,self.pattern)

    def __init__(self):
        self._ptnList = []

    def __getitem__(self,index):
        return self._ptnList[index]

    def __iter__(self):
        return iter(self._ptnList)

    def _appendData(self,newData):
        index = newData[0]
        pattern = newData[1]
        atype = newData[2]
        newEntry = self.PtnTypePair(index,atype,pattern)
        self._ptnList.append(newEntry)

    @classmethod
    def fromPrmFile(cls,prmFile):
        newList = cls()
        with open(prmFile) as prm:
            gaffContent = prm.read()
        #initialize atom type assignment dict
        gaffATypeLines = [line for line in gaffContent.splitlines() if line.startswith("atom")]
        for index,line in enumerate(gaffATypeLines):
            entryElement = [index] + line.split()[1:3]
            ptData = tuple(entryElement)
            newList._appendData(ptData)
        return newList

