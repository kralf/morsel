from morsel.panda import *
from morsel.nodes.ode.geometry import Geometry
from morsel.nodes import Node

#-------------------------------------------------------------------------------

class Mesh(Geometry):
  def __init__(self, world, name, solid, position = [0, 0, 0],
      scale = [1, 1, 1], parent = None, **kargs):
    data = Node(name+"Data", parent = parent)
    solid.mesh.copyTo(data)
    data.clearTransform(solid.mesh)
    data.flattenStrong()
    self.data = panda.OdeTriMeshData(data)
    geometry = panda.OdeTriMeshGeom(world.space, self.data)
    data.removeNode()

    Geometry.__init__(self, world, name, solid, geometry = geometry,
      parent = parent, **kargs)

#-------------------------------------------------------------------------------

  def makeDisplay(self):
    display = Node(self.name+"Display")
    self.solid.mesh.copyTo(display)
    display.flattenStrong()

    return display
