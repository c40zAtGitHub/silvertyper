from .FileInterface import File
class SmartsRuleFile(File):
    def __init__(self,rules):
        self.rulelines = []

    @classmethod
    def fromStream(cls,fileContent):
        flines = fileContent.splitlines()
        rulelines = [line for line in flines if line.startswith("atom")]
        return cls(rulelines)
        
    def toStream(self):
        return "\n".join(self.rulelines)