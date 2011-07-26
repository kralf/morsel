from node import Node

#-------------------------------------------------------------------------------

class Collection(Node):
  def __init__(self, world, name, **kargs):
    Node.__init__(self, world, name, **kargs)
    
#-------------------------------------------------------------------------------

  def getNodes(self):
    children = panda.NodePath.getChildren(self)

    nodes = []
    for i in range(len(children)):
      if children[i].hasPythonTag("this"):
        nodes.append(children[i].getPythonTag("this"))
      else:
        nodes.append(children[i])

    return nodes

  nodes = property(getNodes)
