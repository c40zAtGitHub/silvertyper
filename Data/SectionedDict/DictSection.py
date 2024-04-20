from __future__ import annotations
import collections
from copy import deepcopy

class EntryHolder:
    def __init__(self,entry):
        self.entry = entry

class Section:
    """
    Section that is efficient in query
    and deficient in insertion
    """
    
    def __init__(self,name):
        self.parent = None

        self.name = name
        self._data = [] #store data 
        self._keyIdx = {} #store key-index relationship
        self._idxKey = {} #store index-key relationship
        self._supportedIndexType = {
            int:self._itemByIndex,
            str:self._itemByKey
        }

    def __len__(self):
        return len(self._data)

    def __getitem__(self,identifier):
        idType = type(identifier)
        if idType in self._supportedIndexType.keys():
            #for int or string input
            accessFunction = self._supportedIndexType[idType]
            return accessFunction(identifier)

        elif isinstance(identifier,collections.abc.Iterable):
            #for list of indices or keys
            return self._itemByIterable(identifier)
        
        elif isinstance(identifier,slice):
            start = identifier.start
            stop = identifier.stop
            step = identifier.step

            if start is None:
                start = 0
            if stop is None:
                stop = len(self)
            if step is None:
                step = 1

            indices = [x for x in range(start,stop,step)]
            return self._itemByIterable(indices)
        
        else:
            #for any concrete key objects
            #will raise a key error if the id is not found
            return self._itemByKey(identifier)
        
    # def __setitem__(self,identifier,entry):
    #     holder = self[identifier]
    #     holder.entry = entry
         
    def _itemByIndex(self,index):
        return self._data[index].entry
    
    def _itemByKey(self,key):
        index = self._keyIdx[key]
        return self._itemByIndex(index)
    
    def _itemByIterable(self,iterable):
        #assumes all elements from iterable are of the same type
        idIterator = iter(iterable)
        firstIndex = next(idIterator)
        idType = type(firstIndex)
        accessFunction = self._supportedIndexType[idType]
        entries = [accessFunction(firstIndex)]
        for item in idIterator:
            entries.append(accessFunction(item))
        return entries

    def entries(self,copy=False):
        for item in self._data:
            if copy is False:
                yield item.entry
            else:
                yield deepcopy(item.entry)

    def keyEntries(self,copy=False):
        for index,item in enumerate(self._data):
            key = self._idxKey[index]
            if copy is False:
                yield (key,item.entry)
            else:
                yield (key,deepcopy(item.entry))
    
    def keys(self):
        return self._keyIdx.keys()
    
    def keyLengths(self):
        try:
            firstKey = next(self.keys())
            return len(firstKey)
        except StopIteration:
            #the section is empty
            return 0

    def indices(self):
        return self._idxKey.keys()
    
    def keyOfIndex(self,index):
        return self._idxKey[index]
    
    def keyOfEntry(self,entry):
        return entry.type
    
    def indexOfKey(self,key):
        return self._keyIdx[key]
    
    def indexOfEntry(self,entry):
        key = self.keyOfEntry(entry)
        index = self.indexOfKey(key)
        return index
    
    def addEntry(self,key,newEntry):
        holder = EntryHolder(newEntry)
        newID = len(self)
        self._data.append(holder)
        self._idxKey[newID] = key
        self._keyIdx[key] = newID