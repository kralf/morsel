from actuated import Actuated

#-------------------------------------------------------------------------------

class Platform(Actuated):
  def __init__(self, **kargs):
    super(Platform, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def getPose(self, node = None):
    pose = self.getPosition(node)
    pose.extend(self.getOrientation(node))

    return pose

  def setPose(self, pose, node = None):
    self.setPosition(pose[0:3], node)
    self.setOrientation(pose[3:3], node)
    
  pose = property(getPose, setPose)
