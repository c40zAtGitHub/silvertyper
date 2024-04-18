class DataWrapInterface:
    def __init__(self,
                 data=None,
                 attrToBeLinked = None):
        if attrToBeLinked is None:
            attrToBeLinked = []
        self.data = data
        self._linkDataAttributes(attrToBeLinked)

    def _linkDataAttributes(self,attributes):
        """
        Bring up the attributes of data object to
        the level of its holder.

        for instance, if the data object has .Kr attribute,
        a .Kr property that is equivalent to the following
        code will be bound to the wrapper:
            @property
            def Kr(self):
                return self.data.Kr

            @Kr.setter
            def Kr(self,newValue):
                self.data.Kr = newValue

        input:  can be either list of attributes in string
                when the property name does not change, or
                a dict of {attrName:dataAttrName} if the names
                are different.
        """
        if isinstance(attributes,list):
            attributes = dict([(item,item) for item in attributes])
        
        for attrName,attrFunc in attributes.items():
            def getMethod(self):
                return getattr(self.data,attrFunc)
                
            def setMethod(self,newValue):
                setattr(self.data,attrFunc,newValue)

            setattr(self,attrName,property(getMethod,setMethod))

    @classmethod
    def getDataAttrs(cls):
        """
        name of attributes being wrapped
        """
        if isinstance(cls._attrLink,dict):
            attr = list(cls._attrLink.keys())
        else:
            #assume the _attrLink is a list of attributes
            attr = list(cls._attrLink)

        attr.sort()
        return attr
