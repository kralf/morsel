from node import Node

#-------------------------------------------------------------------------------

class Geometry(Node):
  def __init__(self, **kargs):
    self._mesh = None
    
    super(Geometry, self).__init__(**kargs)

#-------------------------------------------------------------------------------

  def getMesh(self):
    return self._mesh
  
  mesh = property(getMesh)

#-------------------------------------------------------------------------------

  def fit(self, node):
    self.clearTransform(node)
    self.stash()
    
    p_min, p_max = node.getBounds(self.parent)
    
    x = 0.5*(p_min[0]+p_max[0])
    y = 0.5*(p_min[1]+p_max[1])
    z = 0.5*(p_min[2]+p_max[2])
    self.position = [x, y, z]
    
    q_min = self.getRelativePoint(self.parent, p_min)
    q_max = self.getRelativePoint(self.parent, p_max)
    
    s_x = abs(q_max[0]-q_min[0])
    s_y = abs(q_max[1]-q_min[1])
    s_z = abs(q_max[2]-q_min[2])    
    self.scale = [s_x, s_y, s_z]
    
    self.unstash()
    