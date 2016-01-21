import pyNewt
ffi=pyNewt.ffi

o=[]

class BaseNewtonJoint(pyNewt.NewtonObject):
    i=n=None
    for i in dir(pyNewt):
        if i.startswith('NewtonConstraintCreate'):
            n = i.replace('NewtonConstraintCreate', '')
            exec('@classmethod\ndef %s(cls, *args): return cls(pyNewt.%s(*pyNewt.convert(args)))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonJoint'):
            n = i.replace('NewtonJoint', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonContactJoint'):
            n = i.replace('NewtonContactJoint', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonConstraint'):
            n = i.replace('NewtonConstraint', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        else:
            o.append(i)
    del i
    del n


class NewtonJoint(BaseNewtonJoint):
    def __init__(self, mesh):
        self._wrapped=mesh
        self._selfvp = ffi.new_handle(self)
        pyNewt.NewtonJointSetUserData(self._wrapped, self._selfvp)
    def __del__(self):
        pyNewt.NewtonDestroyJoint(self._wrapped)
    
