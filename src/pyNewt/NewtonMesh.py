import pyNewt
ffi=pyNewt.ffi

o=[]

class BaseNewtonMesh(pyNewt.NewtonObject):
    i=n=None
    for i in dir(pyNewt):
        if i.startswith('NewtonMeshCreate'):
            n = i.replace('NewtonMesh', '')
            exec('@classmethod\ndef %s(cls, *args): return cls(pyNewt.%s(*pyNewt.convert(args)))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonMesh'):
            n = i.replace('NewtonMesh', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        else:
            o.append(i)
    del i
    del n


class NewtonMesh(BaseNewtonMesh):
    def __init__(self, mesh):
        self._wrapped=mesh
    def __del__(self):
        pyNewt.NewtonMeshDestroy(self._wrapped)
    
