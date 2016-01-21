import sys
import pyNewt
identity = [
    1,0,0,0,
    0,1,0,0,
    0,0,1,0,
    0,0,0,1
]




@pyNewt.pyNewt.ffi.callback('void(*)(NewtonJoint*, float, int)')
def UserContactFriction (contactJoint, timestep, threadIndex):
    print 'colliding'




def __main__(argv=sys.argv):
    world=pyNewt.NewtonWorld()
    pyNewt.pyNewt.NewtonMaterialSetCollisionCallback(world._wrapped, 0, 0, pyNewt.pyNewt.ffi.NULL, pyNewt.pyNewt.ffi.NULL, UserContactFriction)

    defaultMaterialID = pyNewt.pyNewt.NewtonMaterialGetDefaultGroupID (world._wrapped)
    
    collision=pyNewt.NewtonCollision.createBox(world,10,3,10,1,pyNewt.pyNewt.ffi.NULL)
    collision2=pyNewt.NewtonCollision.createBox(world,1,1,1,2,pyNewt.pyNewt.ffi.NULL)
    
    box1=pyNewt.NewtonBody.createDynamicBody(world, collision, identity)
    box1.setCollidable(True)
    
    box1.setMassProperties(1, collision)
    box1.setLinearDamping(0)
    
    box2=pyNewt.NewtonBody.createDynamicBody(world, collision2, identity)
    box2.setMassProperties(1, collision2)
    
    box2.setCollidable(True)
    box2.setVelocity([0,60,0])
    box2.setLinearDamping(0)
    
    for i in range(10):
        f=pyNewt.pyNewt.ffi.new('float[3]')
        world.update(1/60.)
        import time
        time.sleep(1/60.)
        box2.getPosition(f)
        print f[1]
    box2.setVelocity([0,-6,0])
    for i in range(100):
        f=pyNewt.pyNewt.ffi.new('float[3]')
        world.update(1/60.)
        import time
        time.sleep(1/60.)
        box2.getPosition(f)
        print f[1]
    

if __name__=='__main__':
    __main__()
