class SmartsRuleEntry:
    """
    Entry that contains the following properties on atom typing:
        smarts: the SMARTS pattern that fits a particular structure
        atypes:  list of string atom type labels that corresponds to 
                the highlighted atoms in the pattern
        description: additional description on the current typing rule
    """
    def __init__(self,
                 smarts:str,
                 atypes:list[str],
                 description:str = ""):
        self.smarts = smarts
        self.atypes = atypes
        self.description = description
        
    def __iter__(self):
        yield self.smarts
        yield self.atypes
        