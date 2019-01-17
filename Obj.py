from Prim import *

# Object object
# Will be used as an interface by larger, safer Objects
# Safe for storage in Memory, because holds type
class Obj:
    def __init__(self, type, val):
        self.type = type
        self.val = val
        # self.bin_length = 0
    def toBin(self):
        return C(self.type).toBin()
    def fromBin(self, bin):
        self.val = None
        return C().fromBin(bin[0:8])
    def fromMem(self, mem):
        return None
    def toString(self):
        return str(self.val)

# Object for Integer
# Size: 24 bit
# Max Val: 65535
class Integer(Obj):
    def __init__(self, val=0):
        self.type = "i"
        self.val = val
        # self.bin_length = 24
    def toBin(self):
        return C(self.type).toBin() + I(self.val).toBin()
    def fromBin(self, bin):
        self.val = I().fromBin(bin[8:24])
        return self
    def fromMem(self, mem):
        # pointer is already past type
        self.val = I().fromBin(mem._util_getNextBits(16))
        return self

# Object for Character
# Size: 16 bit
# Max Val: any ASCII
class Character(Obj):
    def __init__(self, val=" "):
        self.type = "c"
        self.val = val
        # self.bin_length = 16
    def toBin(self):
        return C(self.type).toBin() + C(self.val).toBin()
    def fromBin(self, bin):
        self.val = C().fromBin(bin[8:16])
        return self
    def fromMem(self, mem):
        self.val = C().fromBin(mem._util_getNextBits(8))
        return self

# Object for Reference
# Size: 24 bit
# Max Val: byte num 65535
class Reference(Obj):
    def __init__(self, val=0):
        self.type = "r"
        self.val = val # this is an int pointing to a byte location
    def toBin(self):
        return C(self.type).toBin() + I(self.val).toBin()
    def fromBin(self, bin):
        self.val = I().fromBin(bin[8:24])
        return self
    def fromMem(self, mem):
        self.val = I().fromBin(mem._util_getNextBits(16))
        return self
    def resolve(self, mem):
        old_pointer = mem.pointer
        mem.pointer = self.val * 8
        returnable =  mem.readObj() # return the object being pointed to
        mem.pointer = old_pointer # return pointer
        return returnable
    def toString(self): # overload toString method
        return "rf" + str(self.val)

# Object for String
# Size 24bit - Infinity
# Max Val: 65535 characters
class String(Obj):
    def __init__(self, val=""):
        self.type = "s"
        self.val = val
    def toBin(self):
        bin = C(self.type).toBin() + I(len(self.val)).toBin()
        for char in self.val:
            bin += C(char).toBin()
        return bin
    def fromBin(self, bin):
        length = I().fromBin(bin[8:24])
        for i in range(length):
            self.val = C().fromBin(bin[i*8 + 24: i*8 + 24 + 8])
        return self
    def fromMem(self, mem):
        self.val = ""
        length = I().fromBin(mem._util_getNextBits(16))
        for i in range(length):
            self.val += C().fromBin(mem._util_getNextBits(8))
        return self

# Object for Array
# Size: 24bit - Infinity
# Max Val: 65535 items
class Array(Obj):
    def __init__(self, val=[]):
        self.type="a"
        self.val = val
    def toBin(self):
        returnable = C(self.type).toBin() + I(len(self.val)).toBin()
        for item in self.val:
            returnable += item.toBin()
        return returnable
    def fromBin(self, bin):
        self.val = []
        length = I().fromBin(bin[8:24])
        bits_passed = 24
        for i in range(length):
            next_type = C().fromBin(bin[bits_passed:bits_passed+8])
            next = objects[next_type]().fromBin(bin[bits_passed+8:])
            bits_passed += len(next.toBin())
            self.val.append(next)
        return self
    def fromMem(self, mem):
        self.val = []
        length = I().fromBin(mem._util_getNextBits(16))
        for i in range(length): # read in next object to fill length
            self.val.append(mem.readObj())
        return self
    def toString(self):
        return "[" + ", ".join([item.toString() for item in self.val]) + "]"

# Object for Array with specific type -- saves space over normal array, doesn't need type on children
# Size: 32bit - Infinity
# Max Val: 65535 items
class TypeArray(Obj):
    def __init__(self, val=[], val_type="i"):
        self.type = "t"
        self.val = val
        self.val_type = val_type
    def toBin(self):
        returnable = C(self.type).toBin() + C(self.val_type).toBin() + I(len(self.val)).toBin()
        for item in self.val:
            returnable += item.toBin()[8:] # cut out type
        return returnable
    def fromBin(self, bin):
        self.val = []
        self.val_type = C().fromBin(bin[8:16])
        self.length = I().fromBin(bin[16:32])
        bits_passed = 32
        for i in range(length):
            next = objects[self.val_type]().fromBin(bin[bits_passed+8:])
            bits_passed += len(next.toBin())
            self.val.append(next)
        return self
    def fromMem(self, mem):
        self.val = []
        self.val_type = C().fromBin(mem._util_getNextBits(8)) # grab val_type
        length = I().fromBin(mem._util_getNextBits(16)) # grab length
        for i in range(length):
            self.val.append(objects[self.val_type]().fromMem(mem))
        return self
    def toString(self):
        return "<" + self.val_type + ">[" + ", ".join([item.toString() for item in self.val]) + "]"



objects = {
    "i": Integer,
    "c": Character,
    "s": String,
    "r": Reference,
    "a": Array,
    "t": TypeArray
}
