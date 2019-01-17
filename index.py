from Memory import *
from Prim import *
from Obj import *

m = Memory("m.txt")
# m._util_resize(200)

# this is the memory taken index. Note, should be sorted
# Will look like: 0,5,7,14. Highlights the start and stop bytes of used memory
m.writeObj(TypeArray([Integer(0),Integer(8)]))
print(m.toString())

class MemWriter:
    def __init__(self, mem):
        self.mem = mem
        self.mem_size = len(mem.data)
        self.mem.pointer = 0
        print(self._util_getIndex().toString())
    def _util_getIndex(self):
        old_pointer = self.mem.pointer
        self.mem.pointer = 0
        returnable = self.mem.readObj()
        self.mem.pointer = old_pointer
        return returnable

writer = MemWriter(m)
