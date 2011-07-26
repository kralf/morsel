from node import Node

#-------------------------------------------------------------------------------

class Iterator(object):
  def __init__(self, node, type = Node):
    object.__init__(self)
    
    self.node = node
    self.type = type

    self.generator = self.breadthFirst(self.node)

#-------------------------------------------------------------------------------

  def breadthFirst(self, root):
    type = root.getPythonTag("type")
    if type and issubclass(type, self.type):
      yield root.getPythonTag("this")
      
    for child in root.getChildren():
      for node in self.breadthFirst(child):
        type = node.getPythonTag("type")
        if type and issubclass(type, self.type):
          yield node.getPythonTag("this")

#-------------------------------------------------------------------------------

  def next(self):
    return self.generator.next()
