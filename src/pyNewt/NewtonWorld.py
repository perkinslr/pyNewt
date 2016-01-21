import pyNewt
ffi=pyNewt.ffi

o=[]

class BaseNewtonWorld(pyNewt.NewtonObject):
    i=n=None
    for i in dir(pyNewt):
        if i.startswith('NewtonGet'):
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(i.replace('NewtonGet', 'get'), i))
        elif i.startswith('NewtonWorld'):
            n = i.replace('NewtonWorld', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        elif i.startswith('NewtonSet'):
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(i.replace('NewtonSet', 'set'), i))
        elif i in ['NewtonUpdate']:
            n = i.replace('Newton', '')
            exec('@pyNewt.wrap\ndef %s(self, *args): return pyNewt.%s(self._wrapped, *pyNewt.convert(args))'%(n[0].lower()+n[1:], i))
        else:
            o.append(i)
    del i
    del n


class NewtonWorld(BaseNewtonWorld):
    def __init__(self):
        self._wrapped=pyNewt.NewtonCreate()
        self._selfvp = ffi.new_handle(self)
        pyNewt.NewtonWorldSetUserData(self._wrapped, self._selfvp)
    def __del__(self):
        pyNewt.NewtonDestroy(self._wrapped)
    
