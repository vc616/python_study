class A(object):
    attr = 4
class B(A):
    def __init__(self,b):
        self.x = b
class C(B):
    x = 6
print(C(34).x)