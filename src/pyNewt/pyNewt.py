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


class NewtonObject(object):
    def search(self, key):
        return [i for i in dir(self) if key in i]
    @classmethod
    def clsSearch(cls, key):
        return [i for i in dir(cls) if key in i]

def convert(args):
    out = []
    for arg in args:
        if isinstance(arg, NewtonObject):
            out.append(arg._wrapped)
        else:
            out.append(arg)
    return out

def wrap(f):
    def wrapped(*a):
        ret=f(*a)
        if repr(ret).startswith("<cdata 'NewtonBody *'"):
            ret = ffi.from_handle(NewtonBodyGetUserData(ret))
        elif repr(ret).startswith("<cdata 'NewtonWorld *'"):
            ret = ffi.from_handle(NewtonWorldGetUserData(ret))
        elif repr(ret).startswith("<cdata 'NewtonJoint *'"):
            ret = ffi.from_handle(NewtonJointGetUserData(ret))
        elif repr(ret).startswith("<cdata 'NewtonCollision *'"):
            ret = ffi.from_handle(NewtonCollisionGetUserData(ret))
        elif repr(ret).startswith("<cdata 'void *'"):
            try:
                ret = ffi.from_handle(ret)
            except:
                pass
        return ret
    return wrapped
