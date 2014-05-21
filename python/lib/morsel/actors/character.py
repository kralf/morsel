from morsel.nodes.facade import Actuator, Object, Mesh
from morsel.nodes.actor import Actor

#-------------------------------------------------------------------------------

class Character(Actor):
  def __init__(self, name = None, actuator = None, bodyMesh = None,
      bodyAnimation = None, **kargs):
    super(Character, self).__init__(name = name, **kargs)

    if bodyMesh:
      self.mesh = Mesh(filename = bodyMesh, animation = bodyAnimation,
        flatten = True)
    self.actuator = Actuator(type = actuator, **kargs)
    