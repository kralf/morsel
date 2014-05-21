from morsel.nodes.ode.facade import Solid, Body, Joint
from morsel.actuators.differential_drive import DifferentialDrive as Base
from morsel.actuators.ode.wheel_drive import WheelDrive

#-------------------------------------------------------------------------------

class DifferentialDrive(WheelDrive, Base):
  def __init__(self, casterCrankSolids = None, casterCrankBodies = None,
      casterCrankMasses = 1, **kargs):
    super(DifferentialDrive, self).__init__(**kargs)
    
    self.casterCrankJoints = []
    
    if not isinstance(casterCrankSolids, list):
      casterCrankSolids = [casterCrankSolids]*len(self.casterCranks)
    if not isinstance(casterCrankBodies, list):
      casterCrankBodies = [casterCrankBodies]*len(self.casterCranks)
      
    for i in range(len(self.casterCranks)):
      self.casterWheels[i].stash()
      self.casterCranks[i].solid = Solid(type = casterCrankSolids[i])
      self.casterCranks[i].body = Body(type = casterCrankSolids[i])
      self.casterCranks[i].collisionMasks = self.collisionMasks
      self.casterWheels[i].unstash()
      
      casterCrankAnchor = self.casterCranks[i].body.getPosition(self)
      casterCrankJoint = Joint(type = "Hinge", objects = [self,
        self.casterCranks[i]], anchor = casterCrankAnchor, axis = [0, 0, 1],
        stopERP = 0.9, stopCFM = 0)
      self.casterCrankJoints.append(casterCrankJoint)
      
    for i in range(len(self.wheels)):
      if self.isCasterWheel(self.wheels[i]):
        j = self.casterWheels.index(self.wheels[i])
        wheelAnchor = self.wheels[i].body.getPosition(self.casterCranks[j])
        
        self.wheelJoints[i].attach(self.casterCranks[j], self.wheels[i])
        self.wheelJoints[i].anchor = wheelAnchor
    
    self.casterCrankMasses = casterCrankMasses
    
#-------------------------------------------------------------------------------

  def getCasterCrankMasses(self):
    casterCrankMasses = [0]*len(self.casterCranks)
    
    for i in range(len(self.casterCranks)):
      casterCrankMasses[i] = self.casterCranks[i].mass
    
    return casterCrankMasses
    
  def setCasterCrankMasses(self, casterCrankMasses):
    if not isinstance(casterCrankMasses, list):
      casterCrankMasses = [casterCrankMasses]*len(self.casterCranks)
      
    for i in range(len(self.casterCranks)):
      self.casterCranks[i].body.mass = casterCrankMasses[i]
  
  casterCrankMasses = property(getCasterCrankMasses, setCasterCrankMasses)
  
#-------------------------------------------------------------------------------

  def move(self, period):
    WheelDrive.move(self, period)
