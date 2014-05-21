from morsel.nodes.panda.facade import Solid
from morsel.actuators.differential_drive import DifferentialDrive as Base
from morsel.actuators.panda.wheel_drive import WheelDrive

#-------------------------------------------------------------------------------

class DifferentialDrive(WheelDrive, Base):
  def __init__(self, casterCrankSolids = None, **kargs):
    super(DifferentialDrive, self).__init__(**kargs)

    if not isinstance(casterCrankSolids, list):
      casterCrankSolids = [casterCrankSolids]*len(self.casterCranks)
      
    for i in range(len(self.casterCranks)):
      self.casterWheels[i].stash()
      self.casterCranks[i].solid = Solid(type = casterCrankSolids[i])
      self.casterWheels[i].unstash()
      