import math
from Prim import *
from Obj import *

class Memory:
    def __init__(self, filename):
        self.filename = filename
        self.pointer = 0
        self._util_load()

    def _util_save(self):
        file = open(self.filename, "w")
        file.write("".join(self.data))
        file.close()

    def _util_load(self):
        file = open(self.filename, "r")
        self.data = [char for char in file.read()]
        file.close()
        self.pointer = 0

    def _util_resize(self, newByteSize):
        self.data = ["0" for i in range(newByteSize * 8)]
        self._util_save()

    def _util_writeBinString(self, bin):
        for char in bin: # add it
            self.data[self.pointer] = char
            self.pointer += 1

    def _util_getNextBits(self, bits):
        returnable = self.data[self.pointer : self.pointer + bits]
        self.pointer += bits
        returnable = "".join(returnable)
        if len(returnable) != bits:
            print("[Mem] reached end of memory")
            raise SystemExit
        return returnable

    def _util_toString(self):
        bytesPerLine = 8
        numOfLines = math.ceil(len(self.data) / (bytesPerLine * 8)) # 4 bytes per line
        retString = ""
        for i in range(numOfLines):
            lineData = self.data[i*bytesPerLine*8:i*bytesPerLine*8+bytesPerLine*8]
            retString += "\n% 3d :"%(i*bytesPerLine)
            for byte in range(bytesPerLine):
                byteData = lineData[byte*8:byte*8+8]
                retString += " " + "".join(byteData)
        return retString


    # WRITING
    def writeObj(self, obj):
        self._util_writeBinString(obj.toBin())

    # READING
    def readObj(self):
        type_bin = self._util_getNextBits(8)
        # check for empty memory?
        while I().fromBin(2*type_bin) == 0:
            type_bin = self._util_getNextBits(8)

        type = C().fromBin(type_bin)
        if type == "i": # Integer
            return Integer().fromMem(self)
        if type == "c": # Character
            return Character().fromMem(self)
        if type == "s": # String
            return String().fromMem(self)
        else:
            print("[Mem] found unknown type: " + type)
            raise SystemExit





if __name__ == "__main__":
    a = Memory("mem.txt")

    a.writeObj(Integer(14))
    a.writeObj(Character("s"))
    a.writeObj(String("Hello World"))
    a.pointer = 0 # reset to read stuff!
    while True:
        try:
            print(a.readObj())
        except:
            break

    print(a._util_toString())
