"""
Basic functions for AMBER .dat parsers

contains components specific for .dat file parsing
"""
class AmberEntry:
    _keyLength = None
    
    def __init__(self,description):
        self.description = description

    @classmethod 
    def keyElements(cls,line):
        key = line[:cls._keyLength]
        elements = line[cls._keyLength:].split()
        return (key,elements)