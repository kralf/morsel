from morsel.nodes.ode.facade import Solid, Body, Joint
from morsel.platforms.wheeled import Wheeled as Base
from morsel.nodes.ode.platform import Platform

#-------------------------------------------------------------------------------

class Wheeled(Platform, Base):
  def __init__(self, bodySolid = None, bodyBody = None, bodyMass = 1,
      bodyMassOffset = None, **kargs):
    super(Wheeled, self).__init__(**kargs)

    self.actuator.stash()
    self.solid = Solid(type = bodySolid)
    self.body = Body(type = bodyBody, mass = bodyMass, massOffset =
      bodyMassOffset)
    self.actuator.unstash()
    
    self.joint = Joint(type = "Fixed", objects = [self, self.actuator])
    