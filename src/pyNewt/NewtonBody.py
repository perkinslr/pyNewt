import pyNewt
ffi=pyNewt.ffi

o=[]

class BaseNewtonBody(pyNewt.NewtonObject):
    i=n=None
    for i in dir(pyNewt):
        if i.startswith('NewtonCreate') and i.endswith('Body'):
            n = i.replace('Newton', '')
            exec('@classmethod\ndef %s(cls, *args): return cls(pyNewt.%s(*pyNewt.convert(args)))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonBody'):
            n = i.replace('NewtonBody', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        else:
            o.append(i)
    del i
    del n


class NewtonBody(BaseNewtonBody):
    def __init__(self, mesh):
        self._wrapped=mesh
        self._selfvp = ffi.new_handle(self)
        pyNewt.NewtonBodySetUserData(self._wrapped, self._selfvp)
    def __del__(self):
        pyNewt.NewtonDestroyBody(self._wrapped)
    
