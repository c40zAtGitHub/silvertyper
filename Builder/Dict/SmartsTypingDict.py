from __future__ import annotations

from silvertyper.Parser.General import SmartsRuleLineParser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from silvertyper.File.SmartsRuleFile import SmartsRuleFile
class SmartsRuleDictBuilder:
    def __init__(self,fileObj:SmartsRuleFile):
        self.file = fileObj
        self.ruleDict = []

    def build(self):
        for line in self.file.rulelines:
            ruleEntry = SmartsRuleLineParser.fromString(line)
            self.ruleDict.append(ruleEntry.data)
        return self.ruleDict
