from morsel.panda import *
from morsel.nodes.ode.object import Object
from morsel.nodes.node import Node

#-------------------------------------------------------------------------------

class Joint(Node):
  def __init__(self, name = "Joint", type = None, objects = None, **kargs):
    self._object = None
    self._mesh = None
    self._task = None
    
    super(Joint, self).__init__(name = name, **kargs)

    if type:
      self._joint = type(self.world._world)
    if objects:
      self.objects = objects
    
    self.hide(panda.BitMask32.allOn())

#-------------------------------------------------------------------------------

  def getObjects(self):
    if isinstance(self.parent, Object):
      return [self.parent, self._object]
    else:
      return None
      
  def setObjects(self, objects):
    if objects:
      if isinstance(objects, list):
        self.attach(objects[0], objects[1])
      else:
        self.attach(objects)
    else:
      self.detach()
      
  objects = property(getObjects, setObjects)

#-------------------------------------------------------------------------------

  def getBodies(self):
    objects = self.objects
    
    if objects:
      if objects[1]:
        return [objects[0].body, objects[1].body]
      else:
        return [objects[0].body, None]
    else:
      return None
      
  bodies = property(getBodies)

#-------------------------------------------------------------------------------

  def getMesh(self):
    return self._mesh
  
  mesh = property(getMesh)
  
#-------------------------------------------------------------------------------

  def attach(self, *objects):
    self.detach()
    
    if not isinstance(objects, tuple):
      objects = (objects, None)
    
    if not objects[0].body:
      framework.error("Object '"+objects[0].name+
        "' requires a body to be joined.")
    if objects[1] and not objects[1].body:
      framework.error("Object '"+objects[1].name+
        "' requires a body to be joined.")
    
    self.parent = objects[0]
    self._object = objects[1]
    
    objects[0]._joints.append(self)
    if objects[1]:
      objects[1]._joints.append(self)
      self._joint.attach(objects[0].body._body, objects[1].body._body)
    else:
      self._joint.attach(objects[0].body._body, None)

#-------------------------------------------------------------------------------

  def detach(self):
    objects = self.objects
    
    if objects:
      objects[0]._joints.remove(self)
      if objects[1]:
        objects[1]._joints.remove(self)

    self.detachNode()
    self._object = None
    
    if self._joint:
      self._joint.detach()
    if self._mesh:
      self._mesh.detachNode()
      self._mesh = None

#-------------------------------------------------------------------------------

  def show(self, cameraMask = None):
    mesh = self.mesh
    
    if mesh:
      mesh.color = [1, 0, 0, 0.5]
      mesh.setTextureOff(1)
      mesh.setTransparency(panda.TransparencyAttrib.MAlpha)
      
      self.draw()
    
    if cameraMask != None:
      Node.show(self, cameraMask)
    else:
      Node.show(self)
      
    if not self._task:
      self._task = framework.scheduler.addTask(self.name+"/Update",
        self.update)

#-------------------------------------------------------------------------------

  def hide(self, cameraMask = None):
    if self._task:
      framework.scheduler.removeTask(self._task)
      self._task = None
    
    if cameraMask != None:
      Node.hide(self, cameraMask)
    else:
      Node.hide(self)
      
#-------------------------------------------------------------------------------

  def update(self, time):
    self.draw()
    return True

#-------------------------------------------------------------------------------

  def draw(self):
    pass
    