from morsel.panda import *
from morsel.math import *
from morsel.nodes.facade import Object, Mesh
from morsel.actuators.drive import Drive

#-------------------------------------------------------------------------------

class WheelDrive(Drive):
  def __init__(self, frameMesh = None, wheelMeshes = [], **kargs):
    self.wheels = []
    self.wheelRadii = []
    self.wheelRates = []
    
    super(WheelDrive, self).__init__(mesh = frameMesh, **kargs)
  
    for wheelMesh in wheelMeshes:
      wheelMesh = Mesh(filename = wheelMesh, flatten = True)
      wheel = Object(name = "Wheel%d" % (len(self.wheels)+1), mesh =
        wheelMesh, parent = self)
      
      p_min, p_max = wheel.bounds
      d_x = abs(p_max[0]-p_min[0])
      d_z = abs(p_max[2]-p_min[2])
      wheelRadius = 0.5*max(d_x, d_z)
        
      self.wheels.append(wheel)
      self.wheelRadii.append(wheelRadius)
      self.wheelRates.append(0)
      
#-------------------------------------------------------------------------------

  def getWheelCircumference(self, i):
    return 2.0*pi*self.wheelRadii[i]
    
#-------------------------------------------------------------------------------

  def getWheelDistance(self, i, j):
    vector = self.wheels[i].getPos(render)-self.wheels[j].getPos(render)
    return vector.length()

#-------------------------------------------------------------------------------

  def getWheelTrack(self, i):
    return self.wheels[i].getPos(self).dot(panda.Vec3(0, 1, 0))

#-------------------------------------------------------------------------------

  def move(self, period):
    for i in range(len(self.wheels)):
      self.wheels[i].pitch = positiveAngle(self.wheels[i].pitch+
        self.wheelRates[i]*period)
  