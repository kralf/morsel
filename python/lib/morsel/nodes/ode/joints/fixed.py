from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Mesh
from morsel.nodes.ode.joint import Joint

#-------------------------------------------------------------------------------

class Fixed(Joint):
  def __init__(self, **kargs):
    super(Fixed, self).__init__(type = panda.OdeFixedJoint, **kargs)

#-------------------------------------------------------------------------------

  def attach(self, *objects):
    Joint.attach(self, *objects)
    
    self._joint.set()

#-------------------------------------------------------------------------------

  def getMesh(self):
    if not self._mesh:
      self._mesh = Node(name = "Mesh", parent = self)
      self._cylinder = Mesh(name = "Cylinder", filename =
        "geometry/cylinder.bam", orientation = [0, 90, 0], parent = self._mesh)
      self._cube = Mesh(name = "Cube", filename = "geometry/cube.bam",
        parent = self._mesh)
      
    return self._mesh
    
  mesh = property(getMesh)

#-------------------------------------------------------------------------------

  def draw(self):
    bodies = self.bodies    
    if not bodies[1]:
      bodies[1] = render
      
    d_xyz = bodies[1].getPos(self)-bodies[0].getPos(self)
    
    length = d_xyz.length()
    position = bodies[0].getPos(self)+d_xyz*0.5
    quaternion = Quaternion()
    quaternion.lookAt(d_xyz)
    
    self._mesh.position = [position[0], position[1], position[2]]
    self._mesh.quaternion = quaternion
    self._cylinder.scale = [0.01*length, 0.01*length, length]
    self._cube.scale = 0.1*length
  