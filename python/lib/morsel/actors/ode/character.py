from morsel.nodes.ode.facade import Solid, Body, Joint
from morsel.actors.character import Character as Base
from morsel.nodes.ode.actor import Actor

#-------------------------------------------------------------------------------

class Character(Actor, Base):
  def __init__(self, bodySolid = None, bodyBody = None, bodyMass = 1,
      **kargs):
    super(Character, self).__init__(**kargs)
    
    self.actuator.stash()
    self.solid = Solid(type = bodySolid)
    self.body = Body(type = bodyBody, mass = bodyMass)
    self.actuator.unstash()
        
    self.joint = Joint(type = "Fixed", objects = [self, self.actuator])
