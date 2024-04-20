def link_attributes(cls):
    """
    Decorator that bring up the properties of data 
    object set in the _attributes variable to the
    level of its holder.

    for instance, if the data object has .K attribute,
    a .eq property, and _attributes equals {"Kr":"K"}, 
    the following two propertiese will be bound to the wrapper:
        @property
        def Kr(self):
            return self.data.K

        @Kr.setter
        def Kr(self,newValue):
            self.data.K = newValue

    input:  can be either list of attributes in string
            when the property name does not change, or
            a dict of {attrName:dataAttrName} if the names
            are different.
    """
    attr = cls._attributes

    if isinstance(attr,list):
        attr = dict([(item,item) for item in attr])

    elif not isinstance(attr,dict):
        return cls
    
    for attrName,attrFunc in attr.items():
        def getMethod(self,attrFunc=attrFunc):
            #watch out the late binding
            return getattr(self.data,attrFunc)
            
        def setMethod(self,newValue,attrFunc=attrFunc):
            #watch out the late binding
            setattr(self.data,attrFunc,newValue=newValue)
        setattr(cls,attrName,property(getMethod,setMethod))
    
    return cls

class DataWrapInterface:
    _attributes = None
    def __init__(self,data=None):
        self.data = data

    @classmethod
    def attributes(cls):
        """
        name of attributes being wrapped
        """
        if isinstance(cls._attributes,dict):
            attr = list(cls._attributes.keys())
        else:
            #assume the _attrLink is a list of attributes
            attr = list(cls._attributes)

        attr.sort()
        return attr