import data_class
import copy



# obj1 = data_class.Data()
# obj1.measure = 1
# sobj1 = copy.copy(obj1)
# dobj1 = copy.deepcopy(obj1)

# obj1.measure = 2
# print(obj1.measure, " ", sobj1.measure, " ", dobj1.measure)
# sobj1.measure = 3
# print(obj1.measure, " ", sobj1.measure, " ", dobj1.measure)
# dobj1.measure = 4
# print(obj1.measure, " ", sobj1.measure, " ", dobj1.measure)

# # Testing if a class constant can be overwritten by a subclass.
# # It can.

# class Obj:

#     CONST = "Obj"

#     def PrintConst(self):
#         print(self.CONST)

# class SubObj(Obj):

#     CONST = "SubObj"

#     def PrintSuperConst(self):
#         print(super().CONST)

# print()
# obj = Obj()
# obj.PrintConst()
# subobj = SubObj()
# subobj.PrintConst()
# subobj.PrintSuperConst()

# Testing which is more efficient, a dict commands list or Constants for each command

import timeit

class ConstObj:

    def __init__(self):
        if not hasattr(self, "CONST1"):
            self.CONST1 = "Const1"
        if not hasattr(self, "CONST2"):
            self.CONST2 = "Const2"
        if not hasattr(self, "CONST3"):
            self.CONST3 = "Const3"
        if not hasattr(self, "CONST4"):
            self.CONST4 = "Const4"
    

    def PrintConsts(self):
        print(self.CONST1)
        print(self.CONST2)
        print(self.CONST3)
        print(self.CONST4)

    def GetConsts(self):
        self.CONST1
        self.CONST2
        self.CONST3
        self.CONST4

class SubConstObj(ConstObj):

    CONST1 = "SubConst1"
    CONST2 = "SubConst2"
    # CONST3 = "SubConst3"  # Commented for testing
    # CONST4 = "SubConst4"

class DictObj:

    def __init__(self):
        if not hasattr(self, "CONSTS"):
            self.CONSTS = {"CONST1": "Const1", "CONST2": "Const2", "CONST3": "Const3", "CONST4": "Const4"}
        else:
            tempCONSTS = {"CONST1": "Const1", "CONST2": "Const2", "CONST3": "Const3", "CONST4": "Const4"}
            for key in tempCONSTS:
                if key not in self.CONSTS:
                    self.CONSTS[key] = tempCONSTS[key]
        

    def PrintConsts(self):
        print(self.CONSTS["CONST1"])
        print(self.CONSTS["CONST2"])
        print(self.CONSTS["CONST3"])
        print(self.CONSTS["CONST4"])

    def GetConsts(self):
        self.CONSTS["CONST1"]
        self.CONSTS["CONST2"]
        self.CONSTS["CONST3"]
        self.CONSTS["CONST4"]

class SubDictObj(DictObj):

    CONSTS = {"CONST1": "SubConst1", "CONST2": "SubConst2"
            #   , "CONST3": "SubConst3", "CONST4": "SubConst4"  # Commented for testing
              }

# cobj = ConstObj()
# cobj.PrintConsts()
# subcobj = SubConstObj()
# subcobj.PrintConsts()
# dobj = DictObj()
# dobj.PrintConsts()
# subdobj = SubDictObj()
# subdobj.PrintConsts()

# Testing creation times

timer = timeit.timeit(stmt="obj = ConstObj()", setup="from __main__ import ConstObj", number=1000000)
print(timer)
timer = timeit.timeit(stmt="obj = SubConstObj()", setup="from __main__ import SubConstObj", number=1000000)
print(timer)
timer = timeit.timeit(stmt="obj = DictObj()", setup="from __main__ import DictObj", number=1000000)
print(timer)
timer = timeit.timeit(stmt="obj = SubDictObj()", setup="from __main__ import SubDictObj", number=1000000)
print(timer)

# Testing usage times

timer = timeit.timeit(stmt="obj.GetConsts()", setup="from __main__ import ConstObj; obj = ConstObj()", number=1000000)
print(timer)
timer = timeit.timeit(stmt="obj.GetConsts()", setup="from __main__ import SubConstObj; obj = SubConstObj()", number=1000000)
print(timer)
timer = timeit.timeit(stmt="obj.GetConsts()", setup="from __main__ import DictObj; obj = DictObj()", number=1000000)
print(timer)
timer = timeit.timeit(stmt="obj.GetConsts()", setup="from __main__ import SubDictObj; obj = SubDictObj()", number=1000000)
print(timer)