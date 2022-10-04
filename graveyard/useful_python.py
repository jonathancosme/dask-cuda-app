dataDict = {
    "a":{
        "r": 1,
        "s": 2,
        "t": 3
        },
    "b":{
        "u": 1,
        "v": {
            "x": 1,
            "y": 2,
            "z": 3
        },
        "w": 3
        }
}    

maplist = ["a", "r"]

maplist = ["b", "v", "y"]


from functools import reduce  # forward compatibility for Python 3
import operator

def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

getFromDict(dataDict, ["a", "r"])
getFromDict(dataDict, ["b", "v", "y"])
setInDict(dataDict, ["b", "v", "w"], 4)

Use reduce() to traverse the dictionary:

from functools import reduce  # forward compatibility for Python 3
import operator

def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)
and reuse getFromDict to find the location to store the value for setInDict():

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
All but the last element in mapList is needed to find the 'parent' dictionary to add the value to, then use the last element to set the value to the right key.

Demo:

>>> getFromDict(dataDict, ["a", "r"])
1
>>> getFromDict(dataDict, ["b", "v", "y"])
2
>>> setInDict(dataDict, ["b", "v", "w"], 4)
>>> import pprint
>>> pprint.pprint(dataDict)
{'a': {'r': 1, 's': 2, 't': 3},
 'b': {'u': 1, 'v': {'w': 4, 'x': 1, 'y': 2, 'z': 3}, 'w': 3}}
Note that the Python PEP8 style guide prescribes snake_case names for functions. The above works equally well for lists or a mix of dictionaries and lists, so the names should really be get_by_path() and set_by_path():

from functools import reduce  # forward compatibility for Python 3
import operator

def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value

def del_by_path(root, items):
    """Delete a key-value in a nested object in root by item sequence."""
    del get_by_path(root, items[:-1])[items[-1]]

get_by_path(dataDict, maplist)
get_by_path(dataDict, ["a", "r"])
set_by_path(dataDict, maplist, 4)

class Dog:
 
    # Class Variable
    animal = 'dog'
 
    # The init method or constructor
    def __init__(self, breed):
 
        # Instance Variable
        self.breed = breed
 
    # Adds an instance variable
    def setColor(self, color):
        self.color = color
 
    # Retrieves instance variable
    def getColor(self):
        return self.color
 