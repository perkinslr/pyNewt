#!/usr/bin/pypy

import cffi, re, subprocess, os
pattern=re.compile('[a-zA-Z0-0]+[\*]? ([a-zA-Z0-9]+) ?\(')
t=subprocess.Popen(['gcc','-E',"%s/Newton.h"%os.environ.get('NEWTONINCLUDE','/usr/local/include')],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
txt = []
while t.poll() is None:
    txt.append(t.stdout.read())

txt.append(t.stdout.read())

def loadLibrary(libname, ffi):
    print "Looking for", libname
    try:
        t=subprocess.Popen((r'ld -o /dev/null --verbose -l%s'%libname).split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        t.wait()
        p=t.stdout.read().split('-l%s'%libname)[1].split('(')[1].split(')')[0]
        print "Results:",p
        return ffi.dlopen(p,ffi.RTLD_GLOBAL)
    except:
        r = ffi.dlopen(libname, ffi.RTLD_GLOBAL)
        print "Auto Loaded"
        return r
    

data = str.join('',txt)
data = data.replace('{} Newton',' Newton')
data = re.sub('__attribute__\(\(.*?\)\).*?\n.*?\n.*?\n.*?\}','', data)
data = re.sub('__attribute__\(\(.*?\)\).*;','', data)
data = data.replace('', '')



ffi=cffi.FFI()

ffi.cdef(data)

ffi.dlopen(None, ffi.RTLD_GLOBAL)
loadLibrary('rt',ffi)
loadLibrary('stdc++', ffi)
loadLibrary('pthread', ffi)
newton=loadLibrary('Newton', ffi)



matches=pattern.findall(data)

for match in matches:
    try:
        globals()[match]=getattr(newton, match)
    except:
        pass

del txt
del pattern
del match
del matches
del t
del subprocess
del os
del re
del loadLibrary
del data


__version__=[0,0,1,'newton: %i'%NewtonWorldGetVersion()]


class NewtonWorld:
    def __init__(self):
        self._world=NewtonCreate()
        self._selfvp = ffi.new_handle(self)
        NewtonWorldSetUserData(self._world, self._selfvp)
    def __del__(self):
        NewtonDestroy(self._world)
    def Update(self, td):
        NewtonUpdate(self._world, td)


