# Primitive object
# Will be used as an interface by other primitive types
class Prim:
    def __init__(self, val):
        self.val = val
    def toBin(self):
        return "00000000"
    def fromBin(self, bin):
        self.val = None
        return self.val

# Primitive for (I)ntegers!
# Size: 16bit
# Max Value: 65535
class I(Prim):
    def __init__(self, val=0):
        self.val = val
    def toBin(self):
        return "%016d"%int(str(bin(self.val))[2:]) # convert content to 16bit
    def fromBin(self, bin):
        self.val = int(bin[0:16],2)
        return self.val

# Primitive for (C)haracters!
# Size: 8bit
# Max Value: any valid ASCII
class C(Prim):
    # ord(char) == toASCII
    # chr(int) == toChar
    def __init__(self, val=" "):
        self.val = val
    def toBin(self):
        return "%08d"%int(str(bin(ord(self.val)))[2:])
    def fromBin(self, bin):
        self.val = chr(int(bin, 2))
        return self.val
