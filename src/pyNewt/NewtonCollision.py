import pyNewt
ffi=pyNewt.ffi

o=[]

class BaseNewtonCollision(pyNewt.NewtonObject):
    i=n=None
    for i in dir(pyNewt):
        if i.startswith('NewtonCreate') and not i.endswith('Body'):
            n = i.replace('Newton', '')
            exec('@classmethod\ndef %s(cls, *args): return cls(pyNewt.%s(*pyNewt.convert(args)))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonCollision'):
            n = i.replace('NewtonCollision', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        else:
            o.append(i)
    del i
    del n


class NewtonCollision(BaseNewtonCollision):
    def __init__(self, c):
        self._wrapped=c
        self._selfvp = ffi.new_handle(self)
        pyNewt.NewtonCollisionSetUserData(self._wrapped, self._selfvp)
    def __del__(self):
        pyNewt.NewtonDestroyCollision(self._wrapped)
    
