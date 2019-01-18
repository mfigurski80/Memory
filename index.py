from Memory import *
from Prim import *
from Obj import *

m = Memory("m.txt")

# m.writeObj(TypeArray([
#     Array([String("Mik"), Integer(18), String("ATL")]),
#     Array([String("Nat"), Integer(18), String("PHL")]),
#     Array([String("Nas"), Integer(19), String("TUN")]),
#     Array([String("Fin"), Integer(19), String("ENG")])
# ]))
m.writeObj(DataStr([["s","i","s"],
    ["Mik",18,"ATL"],
    ["Nat",18,"PHL"],
    ["Nas",19,"TUN"],
    ["Roh",18,"CALI"],
    ["Fin",19,"ENG"],
    ["Rand",523,"a"],
]))


print(m.toString())

# Read out the entire memory
print("\n**** Written Memory Dump ****")
m.pointer = 0
while True:
    try:
        print(m.readObj().toString())
    except:
        break

print("\n**** Char Memory Dump ****")
m.pointer = 0
while True:
    try:
        print(C().fromBin(m._util_getNextBits(8)), end=".")
    except:
        break
