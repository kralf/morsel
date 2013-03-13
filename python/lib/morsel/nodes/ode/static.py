from morsel.panda import *
from morsel.nodes.static import Static as Base

#-------------------------------------------------------------------------------

class Static(Base):
  def __init__(self, world, name, mesh, solid = None, **kargs):
    Base.__init__(self, world, name, mesh, **kargs)

    if not solid:
      solid = "Empty"

    if isinstance(solid, dict):
      self.solid = []
      for part in solid.keys():
        partModel = self.mesh.find("**/"+part)
        if not partModel.isEmpty():
          partMesh = Mesh(name = name+"Mesh", model = partModel,
            parent = self.mesh.parent)
          partSolid = Solid(name = name+"Solid", type = solid[part],
            mesh = partMesh, parent = self.world.scene.solid)
            
          self.solid.append(partSolid)
        else:
          framework.error("Part model '"+part+"' not found")
    else:
      self.solid = Solid(name = name+"Solid", type = solid, mesh = self.mesh,
        parent = self.world.scene.solid)
    