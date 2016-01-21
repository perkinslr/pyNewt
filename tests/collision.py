import sys
import pyNewt

@pyNewt.pyNewt.ffi.callback('void(*)(NewtonBody *, float *, int)')
def transformCallback(b, f, I):
    print 12,
    print b,
    print [f[i] for i in range(16)]

@pyNewt.pyNewt.ffi.callback('int (NewtonMaterial *, NewtonBody *, NewtonBody *, int)')
def UserOnAABBOverlap(*a):
    print 'in overlap'
    return 1


@pyNewt.pyNewt.ffi.callback('void(*)(NewtonJoint *, float, int)')
def UserContactFriction (contactJoint, timestep, threadIndex):
    print 'colliding'




def __main__(argv=sys.argv):
    world=pyNewt.NewtonWorld()
    
    defaultMaterialID = pyNewt.pyNewt.NewtonMaterialGetDefaultGroupID (world._wrapped)
    pyNewt.pyNewt.NewtonMaterialSetCollisionCallback (world._wrapped, defaultMaterialID, defaultMaterialID, pyNewt.pyNewt.ffi.NULL, UserOnAABBOverlap, UserContactFriction);
    
    collision=pyNewt.NewtonCollision.createBox(world,10,3,10,1,pyNewt.pyNewt.ffi.NULL)
    collision2=pyNewt.NewtonCollision.createBox(world,1,1,1,2,pyNewt.pyNewt.ffi.NULL)
    
    box1=pyNewt.NewtonBody.createDynamicBody(world, collision, [0]*16)
    box1.setCollidable(True)
    box1.setTransformCallback(transformCallback)
    box1.setMatrix([1.0, 0.0, 0.0, 0.0, 
                    0.0, 1.0, 0.0, 0.0, 
                    0.0, 0.0, 1.0, 0.0, 
                    0.0, 1.0, 0.0, 1.0])
    
    box2=pyNewt.NewtonBody.createDynamicBody(world, collision2, [0]*16)
    box2.setTransformCallback(transformCallback)
    box2.setVelocity([0,3,0])
    box2.setCollidable(True)
    
    
    for i in range(20):
        f=pyNewt.pyNewt.ffi.new('float[3]')
        world.update(1)
        import time
        time.sleep(1)
        box2.getPosition(pyNewt.pyNewt.ffi.addressof(f)[0])
        print f[0]
        print f[1]
        print f[2]
    

if __name__=='__main__':
    __main__()
