from pyNewt import NewtonWorld, NewtonCollision, NewtonBody, pyNewt

identity = [
    1,0,0,0,
    0,1,0,0,
    0,0,1,0,
    0,0,0,1
]

w = NewtonWorld()
c = NewtonCollision.createSphere(w,1,1,pyNewt.ffi.NULL)
b = NewtonBody.createDynamicBody(w,c,identity)
mass=pyNewt.ffi.new('float[1]')
xx=pyNewt.ffi.new('float[1]')
yy=pyNewt.ffi.new('float[1]')
zz=pyNewt.ffi.new('float[1]')

b.setMassProperties(1, c)

b.getMassMatrix(mass,xx,yy,zz)
b.setLinearDamping(0)
print 19, mass[0],xx[0],yy[0],zz[0]

b.setVelocity([0,1,0])
for i in range(61):
    f=pyNewt.ffi.new('float[3]')
    w.update(1/60.)
    b.getPosition(f)
    print list(f)
    import time
    time.sleep(1/60.)
