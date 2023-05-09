import data_class
import copy



obj1 = data_class.Data()
obj1.measure = 1
sobj1 = copy.copy(obj1)
dobj1 = copy.deepcopy(obj1)

obj1.measure = 2
print(obj1.measure, " ", sobj1.measure, " ", dobj1.measure)
sobj1.measure = 3
print(obj1.measure, " ", sobj1.measure, " ", dobj1.measure)
dobj1.measure = 4
print(obj1.measure, " ", sobj1.measure, " ", dobj1.measure)