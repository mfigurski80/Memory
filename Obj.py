from Prim import *

# Object object
# Will be used as an interface by larger, safer Objects
class Obj:
    def __init__(self, type, val):
        self.type = type
        self.val = val
    def toBin(self):
        return C(self.type).toBin()
    def fromBin(self, bin):
        self.val = None
        return C().fromBin(bin[0:8])
    def fromMem(self, mem):
        return None

# Object for Integer
# Size 24 bit. Safe for storage in Memory
# Max Val: 65535
class Integer(Obj):
    def __init__(self, val=0):
        self.type = "i"
        self.val = val
    def toBin(self):
        return C(self.type).toBin() + I(self.val).toBin()
    def fromBin(self, bin):
        self.val = I().fromBin(bin[8:24])
        return self.val
    def fromMem(self, mem):
        # pointer is already past type
        self.val = I().fromBin(mem._util_getNextBits(16))
        return self.val

# Object for Character
# Size 16 bit. Safe for storage in Memory
# Max Val: any ASCII
class Character(Obj):
    def __init__(self, val=" "):
        self.type = "c"
        self.val = val
    def toBin(self):
        return C(self.type).toBin() + C(self.val).toBin()
    def fromBin(self, bin):
        self.val = C().fromBin(bin[8:16])
        return self.val
    def fromMem(self, mem):
        self.val = C().fromBin(mem._util_getNextBits(8))
        return self.val

# Object for String
# Size 24bit-Infinity. Safe for storage in Memory
# Max Val: 65535 characters
class String(Obj):
    def __init__(self, val=" "):
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
        return self.val
    def fromMem(self, mem):
        self.val = ""
        length = I().fromBin(mem._util_getNextBits(16))
        for i in range(length):
            self.val += C().fromBin(mem._util_getNextBits(8))
        return self.val
