from .GAFFKey import GAFFKey
from silvertyper.ForcefieldTyper.Dict.STBadiDict import STParaDictEntry,STBadiDict

def line2Dict(lines:list[str],
              head:int,
              lineProcFunc,
              duplicateLines = False):
    """
    Routine to convert lines of .dat content to
    preferred dictinary objects
    lines           - list of lines for each section
    head            - length of key section
    lineProcFunc    - process function that converts each
                      line element to its proper format
    duplicateLines  - a flag that indicates if one key hits
                      multiple lines 
    """
    lineDict = {}
    lineNumOffset = 0
    for lineNum,line in enumerate(lines):
        lineNum -= lineNumOffset
        keyStr = line[:head]
        otherElements = line[head:].split()
        allElements = list(keyStr) + otherElements
        lineItems = lineProcFunc(allElements)
        key = lineItems[0]
        para = tuple(lineItems[1:])
        if duplicateLines is False:
            lineDict[key] = STParaDictEntry(lineNum,key,para)
        elif key in lineDict.keys():
            lineNumOffset += 1
            if type(lineDict[key].para) is dict:
                lineDict[key].para.append(para)
            else:
                firstPara = lineDict[key].para
                lineDict[key].para = [firstPara,para]
        else:
            lineDict[key] = STParaDictEntry(lineNum,key,para)
            
    return lineDict


class GAFFParameterDict(STBadiDict):
    #a static class that defines
    #   the interaction between various atom types
    def __init__(self,typeDict,
                 bondDict,angleDict,dihedralDict,improperDict,vdwDict):
        super().__init__(bondDict,angleDict,dihedralDict,improperDict)
        #GAFF component
        #Bond Angle Dihedral Improper vdw
        self.section['atom'] = typeDict
        self.section['vdw'] = vdwDict
        self.sectionOfKeyLength[1] = ['atom','vdw']
        self._DefaultKey = GAFFKey

    @classmethod
    def fromFile(cls,fileName):
        #parse the gaff.dat file
        #atom types (atomType, atomicMass in amu, polarizability in A3)
        #bond - in (key, force constant in kcal/mol/A2, re in A)
        #        followed by reliability data (source, numStructure to fit, rmsd)
        #angle - in (key, force constant in kcal/mol/rad2, θe in rad)
        #        followed by reliability data (source, numStructure to fit, rmsd)
        #dihedral - in (key, divider, Vn (kcal/mol, actual barrier divided by 2), γ(rad), n)
        #        followed by reliability data (source, numStructure to fit, rmsd)
        #           E(φ) = Vn/divider * (1+ cos(n*φ - γ))
        #improper -   in (key, Vn (kcal/mol, actual barrier divided by 2), γ(rad), n)
        #           note that in key, the center atom is the THIRD
        #vdw - in (atomSymbol, re_i/2 in Angstrom, epsilon_i in kcal/mol)
        #       the pairwise re and epsilon is combined as
        #       re_ij = 1/2 * (re_i + re_j);    eps_ij = sqrt(eps_i*eps_j)
        #       see https://ambermd.org/vdwequation.pdf for details
        with open(fileName) as gaffdat:
            gaffdatContent = gaffdat.read()
        gaffSection = gaffdatContent.split('\n\n') #sections are separated by blank lines
        gaffSection = [section.strip() for section in gaffSection]
        #fine trimming for individual sections based on the file structure
        #the useful sections are 0,1,2,3,4,6. Ohter sections are mostly comments
        typeSection = gaffSection[0].splitlines()[1:]
        bondSection = gaffSection[1].splitlines()[1:]
        angleSection = gaffSection[2].splitlines()
        dihedralSection = gaffSection[3].splitlines()
        improperSection = gaffSection[4].splitlines()
        vdwSection = gaffSection[6].splitlines()[1:]

        #construct dict from each section via the line2Dict routine
        typeLineProcFunc = lambda items:(
            GAFFKey(items[0]),  #atom type
            float(items[1]),    #atomic mass
            float(items[2]),    #atom polarizability
            ' '.join(items[3:]) #atom type description
                                         )
        typeDict = line2Dict(typeSection,2,typeLineProcFunc)

        bondLineProcFunc = lambda items:(
            GAFFKey(items[0]),  #bond type
            float(items[1]),    #bond force constant, Kf
            float(items[2]),    #bond equilibrium distance, re
        )
        bondDict = line2Dict(bondSection,5,bondLineProcFunc)

        angleLineProcFunc = lambda items:(
            GAFFKey(items[0]),  #angle type
            float(items[1]),    #angle force constant, Kt
            float(items[2])     #Equilibrium angle, te
        )
        angleDict = line2Dict(angleSection,8,angleLineProcFunc)

        dihedralLineProcFunc = lambda items:(
            GAFFKey(items[0]),      #dihedral type
            float(items[1]),        #common divisor, div
            float(items[2]),        #barrier height, Vn
            float(items[3]),        #gamma
            abs(float(items[4]))    #the period fold, n
        )
        dihedralDict = line2Dict(dihedralSection,12,dihedralLineProcFunc,
                                 duplicateLines=True)

        improperLineProcFunc = lambda items:(
            GAFFKey(items[0]),  #improper type
            float(items[1]),    #Vn
            float(items[2]),    #gamma
            float(items[3])     #n
        )
        improperDict = line2Dict(improperSection,12,improperLineProcFunc)

        vdwLineProcFunc = lambda items:(
            GAFFKey(items[0]),  #improper type
            float(items[1]),    #Re
            float(items[2]),    #sigma
        )
        vdwDict = line2Dict(vdwSection,2,vdwLineProcFunc)
        return cls(typeDict,bondDict,angleDict,dihedralDict,improperDict,vdwDict)