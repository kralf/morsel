from morsel.nodes.panda.solids import Box

#-------------------------------------------------------------------------------

class Mesh(Box):
  def __init__(self, **kargs):
    super(Mesh, self).__init__(**kargs)
