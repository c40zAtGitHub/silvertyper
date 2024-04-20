class GaffDatFile:
    def __init__(self,typeSection,
                 bondSection,
                 angleSection,
                 dihedralSection,
                 improperSection,
                 vdwSection):
        self.typeSection = typeSection
        self.bondSection = bondSection
        self.angleSection = angleSection
        self.dihedralSection = dihedralSection
        self.improperSection = improperSection
        self.vdwSection = vdwSection

    @classmethod
    def fromStream(cls,fileContent):
        gaffSection = fileContent.split('\n\n') #sections are separated by blank lines
        gaffSection = [section.strip() for section in gaffSection]
        #fine trimming for individual sections based on the file structure
        #the useful sections are 0,1,2,3,4,6. Ohter sections are mostly comments
        typeSection = gaffSection[0].splitlines()[1:]
        bondSection = gaffSection[1].splitlines()[1:]
        angleSection = gaffSection[2].splitlines()
        dihedralSection = gaffSection[3].splitlines()
        improperSection = gaffSection[4].splitlines()
        vdwSection = gaffSection[6].splitlines()[1:]
        return cls(typeSection,
                   bondSection,
                   angleSection,
                   dihedralSection,
                   improperSection,
                   vdwSection)
    
    def toStream(self):
        pass