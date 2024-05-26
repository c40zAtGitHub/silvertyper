from silvertyper.Data.Entry.Typing.SmartsTyping import SmartsRuleEntry
from ..LineParser import LineParser,link_attributes

@link_attributes
class SmartsRuleLineParser(LineParser):
    """
    Parses a rule line composed of smarts pattern and
    the corresponding atom type labeled in the pattern
    """
    _attributes = ["smarts","atypes","description"]
    _strTemplate = "{}\t{}\t\"{}\""

    def __init__(self, smarts,atypes,description):
        data = SmartsRuleEntry(smarts,atypes,description=description)
        super().__init__(data)

    def __str__(self):
        atypesStr = ",".join(self.atypes)
        return self._strTemplate.format(
            self.smarts,
            atypesStr,
            self.description
            )
    
    @classmethod
    def fromString(cls,entryString):
        """
        entrySt
        """
        elements = entryString.split()
        smarts = elements[1]
        atypes = elements[2].split(',')
        try:
            description = ' '.join(elements[3:])
            #remove quotation
            description = description.replace('"','')
        except IndexError:
            description = ""
        return cls(smarts,atypes,description=description)
