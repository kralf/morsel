from morsel.nodes import Scene as Base

#-------------------------------------------------------------------------------

class Scene(Base):
  def __init__(self, world, name, **kargs):
    Base.__init__(self, world, name, **kargs)
