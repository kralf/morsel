from morsel.actuators.planar_drive import PlanarDrive as Base
from morsel.actuators.panda.drive import Drive

#-------------------------------------------------------------------------------

class PlanarDrive(Drive, Base):
  def __init__(self, bearingSolid = None, **kargs):
    super(PlanarDrive, self).__init__(solid = bearingSolid, **kargs)        
    