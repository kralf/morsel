from morsel.nodes.panda.facade import Solid
from morsel.actuators.wheel_drive import WheelDrive as Base
from morsel.actuators.panda.drive import Drive

#-------------------------------------------------------------------------------

class WheelDrive(Drive, Base):
  def __init__(self, frameSolid = None, wheelSolids = None, **kargs):
    super(WheelDrive, self).__init__(solid = frameSolid, **kargs)        

    if not isinstance(wheelSolids, list):
      wheelSolids = [wheelSolids]*len(self.wheels)      
    for i in range(len(self.wheels)):
      self.wheels[i].solid = Solid(type = wheelSolids[i])
      self.wheels[i].collisionMasks = self.collisionMasks
    