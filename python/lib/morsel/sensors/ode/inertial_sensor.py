from morsel.panda import *
from morsel.math import *
from morsel.nodes.ode.facade import Solid, Body
from morsel.sensors.inertial_sensor import InertialSensor as Base
from morsel.nodes.ode.sensor import Sensor

#-------------------------------------------------------------------------------

class InertialSensor(Sensor, Base):
  def __init__(self, solid = None, body = None, mass = 1, **kargs):
    super(InertialSensor, self).__init__(**kargs)

    self.solid = Solid(type = solid)
    self.body = Body(type = body, mass = mass)

#-------------------------------------------------------------------------------

  def updateVelocity(self, period):
    self.linearVelocity = self.body.getLinearVelocity(self)
    self.angularVelocity = self.body.getAngularVelocity(self)
    
  