from .GAFFKey import GAFFKey

class GAFFParameterDict:
    #a static class that defines
    #   the interaction between various atom types
    def __init__(self,typeDict,
                 bondDict,angleDict,dihedralDict,improperDict,vdwDict):
        #GAFF component
        #Bond Angle Dihedral Improper vdw
        self.atomTypes = typeDict
        self.bondPara = bondDict
        self.anglePara = angleDict
        self.dihedralPara = dihedralDict
        self.improperPara = improperDict
        self.vdwPara = vdwDict

        self._dictOfKeyLength = {
            1:self.vdwPara,
            2:self.bondPara,
            3:self.anglePara,
            4:self.dihedralPara
        }

    @classmethod
    def fromDatFile(cls,parameterFile):
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
        with open(parameterFile) as gaffdat:
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

        #construct dict from each section
        typeDict = {}
        for line in typeSection:
            lineElements = line.split()
            atype,amass,apol = lineElements[:3]
            typeDesp = ' '.join(lineElements[3:])
            amass = float(amass)
            apol = float(apol)
            typeDict[atype] = (amass,apol,typeDesp)

        bondDict = {}
        for line in bondSection:
            key = line[:5]
            Kf,re = line[5:].split()[:2]
            key = GAFFKey(key)
            Kf = float(Kf)
            re = float(re)
            bondDict[key] = (Kf,re)

        angleDict = {}
        for line in angleSection:
            key = line[:8]
            Kt,te = line[8:].split()[:2]
            key = GAFFKey(key)
            Kt = float(Kt)
            te = float(te)
            angleDict[key] = (Kt,te)

        dihedralDict = {}
        for line in dihedralSection:
            key = line[:12].strip()
            div,Vn,gamma,n = line[12:].split()[:4]
            key = GAFFKey(key)
            div = float(div)
            Vn = float(Vn)
            gamma = float(gamma)
            n = abs(float(n))

            #one dihedral entry may have multiple series
            if key in dihedralDict.keys():
                dihedralDict[key].append((div,Vn,gamma,n))
            else:
                dihedralDict[key] = [(div,Vn,gamma,n)]

        improperDict = {}
        for line in improperSection:
            key = line[:12].strip()
            Vn,gamma,n = line[12:].split()[:3]
            key = GAFFKey(key)
            Vn = float(Vn)
            gamma = float(gamma)
            n = float(n)
            improperDict[key] = (Vn,gamma,n)

        vdwDict = {}
        for line in vdwSection:
            key,Re,sigma = line.split()[:3]
            key = GAFFKey(key)
            Re = float(Re)
            sigma = float(sigma)
            vdwDict[key] = (Re,sigma)

        return cls(typeDict,bondDict,angleDict,dihedralDict,improperDict,vdwDict)

    def find(self,key,improper=False):
        #if find an entry, return entry
        #if multiple entry hits, find the one that has least wild cards
        #otherwise return none
        if type(key) is str:
            gaffkey = GAFFKey(key)
        else:
            gaffkey = GAFFKey('-'.join(key))

        keyLength = len(gaffkey)
        if improper is False:
            desigDict = self._dictOfKeyLength[keyLength]
        else:
            desigDict = self.improperPara

        paraToReturn = None
        for key in desigDict.keys():
            if gaffkey.matches(key):
                if key.hasWildcard:
                    paraToReturn = desigDict[key]
                else:
                    return desigDict[key]
        return paraToReturn
    
    @property
    def bonds(self):
        for key in self.bondPara.keys():
            yield (str(key),self.bondPara[key])

    @property
    def angles(self):
        for key in self.anglePara.keys():
            yield (str(key),self.anglePara[key])

    @property
    def dihedrals(self):
        for key in self.dihedralPara.keys():
            yield (str(key),self.dihedralPara[key])

    @property
    def impropers(self):
        for key in self.improperPara.keys():
            yield (str(key),self.improperPara[key])

    @property
    def vdw(self):
        for key in self.vdwPara.keys():
            yield (str(key),self.vdwPara[key])

