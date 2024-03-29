from __future__ import annotations
from copy import deepcopy

from silvertyper.File.LAMMPS.LAMMPSDataFile import LAMMPSDataFile
from silvertyper.File.LAMMPS.LAMMPSParaFile import LAMMPSParameterFile

#for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.IO.LAMMPS.LAMMPSBadiData import LAMMPSBadiData
    from silvertyper.IO.LAMMPS.LAMMPSBadiData import LAMMPSBadiEntry
    from silvertyper.IO.LAMMPS.AtomDataEntry.Charge import ChargeEntry
    from silvertyper.ForcefieldTyper.Dict.STBadiDict import STBadiDict
    from silvertyper.ForcefieldTyper.Dict.STBadiDict import STParaDictEntry


abadiName = ['atom','bond','angle','dihedral','improper']

class LAMMPSInputGen:

    def __init__(self,
                dataObj:LAMMPSBadiData,
                paraDict:STBadiDict):
        self.data = dataObj
        self.paraDict = paraDict
        #determines if all forcefield parameters are included in the input
        self.fullPara = True
        #determine if string ID are used
        #If False,  use numeric IDs instead
        self.stringID = False
        self._aMasses = []
        self._initAtomMasses()

        self._abadiTypeMap = {}
        self._initAbadiTypeMapping()

    def _initAtomMasses(self):
        atypeDict = self.data['atom'].type
        for atypeKey,atypeID in atypeDict.items():
            atypeEntry:STParaDictEntry = self.paraDict.findInSection(atypeKey,'atom')
            #structure for mass para: 
            #   (amass,polarizability,type description)
            amass = atypeEntry.para[0]
            if self.stringID is True:
                self._aMasses.append((atypeKey,amass))
            else:
                self._aMasses.append((atypeID,amass))

    def _initAbadiTypeMapping(self):
        #generate (dataTypeID,keyTypeID,paraID) mapping

        for sectionName in abadiName:
            dTypeDict = self.data[sectionName].type
            dTypeMap = []
            for typeKey,typeID in dTypeDict.items():
                paraEntry:STParaDictEntry = self.paraDict.findInSection(typeKey,sectionName)
                paraID = paraEntry.index
                dTypeMap.append((typeID,typeKey,paraID))
            self._abaidTypeMap[sectionName] = dTypeMap
        
    def _typeID(self,typeKey,section):
        entry = [entry for entry in self._baidTypeMap[section]\
                if entry[1] == typeKey][0]
        if self.stringID is True:
            return entry[1]
        elif self.fullPara is True:
            return entry[2]
        else:
            return entry[0]
        
    def _genAbadiDLines(self,section):
        sectionLines = []
        for entry in self.data[section].data:
            entryCopy:LAMMPSBadiEntry = deepcopy(entry)
            entryTypeID = entryCopy.entryTypeID
            entryTypeKey = self.data[section].type[entryTypeID]
            extTypeID = self._typeID(entryTypeKey,section)
            entryCopy.entryTypeID = extTypeID
            entryLine = str(entryCopy)
            sectionLines.append(entryLine)
        return sectionLines
    
    def gen_BadivPLines(self,section):
        sectionLines = []
        if self.fullPara is True:
            #write all para lines
            pass
        else:
            #write selected para lines
            pass
        return sectionLines


    def genDataParaFile(self):
        #data para lists 2b established at this step
        #all lists are section content lines in string
        #data list

        #gen Masses section lines
        amassDLines = []
        amassDTemplate = "\t{atype}\t{amass}"
        for item in self._aMasses:
            atype,amass = item
            amassLine = amassDTemplate.format(atype=atype,amass=amass)
            amassDLines.append(amassLine)
        
        #gen atomDLines
        atomDLines = self._genAbadiDLines('atom')
        bondDLines = self._genAbadiDLines('bond')
        angleDLines = self._genAbadiDLines('angle')
        dihedralDLines = self._genAbadiDLines('dihedral')
        improperDLines = self._genAbadiDLines('improper')

        #para list
        #   bondPLines
        #   anglePLines
        #   dihedralPLines
        #   improperPLines
        #   vdwPLines
        if self.fullPara is True:
            #generate all parameter lines
            #set type id of data to that of para
            pass
        else:
            #generate partial parameter lines
            #set type id of para to that of data
            pass

        #generate entry lines

        # amassEntries = [entry for entry in self.data.] 
        # atomEntries = [entry for entry in self.data.atoms]  
        # bondEntries = [entry for entry in self.data.bonds]  
        # angleEntries = [entry for entry in self.data.angles] 
        # dihedralEntries = [entry for entry in self.data.atoms]  
        # improperEntries = [entry for entry in self.data.atoms]  

            

        #initialize data and para file object
        self.dataFile = LAMMPSDataFile()
        self.paraFile = LAMMPSParameterFile()
    
    def writeData(self,dafaFileName):
        pass
    
    def writePara(self,paraFileName):
        pass