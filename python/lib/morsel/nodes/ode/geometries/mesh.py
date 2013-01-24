from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Mesh(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], **kargs):
    Geometry.__init__(self, world, name, solid, **kargs)
      
    data = Node(name+"Data", scale = self.globalScale)
    solid.mesh.copyTo(data)
    data.flattenStrong()
    data.clearTransform(solid.mesh)
    self.data = panda.OdeTriMeshData(data)
    
    self.geometry = panda.OdeTriMeshGeom(world.space, self.data)
    
    data.removeNode()

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    display = Node(self.name+"Display")
    self.solid.mesh.copyTo(display)
    display.flattenStrong()

    return display
