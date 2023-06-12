import six

class M_A(type):
    def __str__(self):
        return "M_A"
    
@six.add_metaclass(M_A)
class A(object):
    def print(self):
        print("This is a member of A")

class M_B(type(A)):
    def __str__(self):
        return "M_B"
    
@six.add_metaclass(M_B)
class B(A):
    pass

print(A)
print(B)
B().print()