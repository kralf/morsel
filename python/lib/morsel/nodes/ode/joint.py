from morsel.panda import *
from morsel.nodes.ode.object import Object
from morsel.nodes.node import Node

#-------------------------------------------------------------------------------

class Joint(Node):
  def __init__(self, name = "Joint", type = None, objects = None,
      feedback = False, **kargs):
    self._object = None
    self._mesh = None
    self._task = None
    
    super(Joint, self).__init__(name = name, **kargs)

    self._joint = type(self.world._world)
    if objects:
      self.objects = objects
    self.feedback = feedback
    
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

  def getFeedback(self):
    if self._joint.getFeedback():
      return True
    else:
      return False

  def setFeedback(self, feedback):
    self._joint.setFeedback(feedback)
    
  feedback = property(getFeedback, setFeedback)
    
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

  def getForces(self, node = None):
    if not isinstance(node, list):
      node = [node]*2
    
    feedback = self._joint.getFeedback()
    
    if feedback:
      if not node[0]:
        node[0] = self
      force1 = node[0].getRelativeVector(render, feedback.getForce1())
      if not node[1]:
        node[1] = self
      force2 = node[1].getRelativeVector(render, feedback.getForce2())
      
      return [[force1[0], force1[1], force1[2]],
              [force2[0], force2[1], force2[2]]]
    else:
      return None
  
  forces = property(getForces)
  
#-------------------------------------------------------------------------------

  def getGlobalForces(self):
    return self.getForces(render)

  globalForces = property(getGlobalForces)

#-------------------------------------------------------------------------------

  def getTorques(self, node = None):
    if not isinstance(node, list):
      node = [node]*2
    
    feedback = self._joint.getFeedback()
    
    if feedback:
      if not node[0]:
        node[0] = self
      torque1 = node[0].getRelativeVector(render, feedback.getTorque1())
      if not node[1]:
        node[1] = self
      torque2 = node[1].getRelativeVector(render, feedback.getTorque2())
      
      return [[torque1[0], torque1[1], torque1[2]],
              [torque2[0], torque2[1], torque2[2]]]
    else:
      return None
  
  torques = property(getTorques)
  
#-------------------------------------------------------------------------------

  def getGlobalTorques(self):
    return self.getTorques(render)

  globalTorques = property(getGlobalTorques)

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

  def reattach(self):
    objects = self.objects
    
    self._joint.detach()
    
    if objects[1]:
      self._joint.attach(objects[0].body._body, objects[1].body._body)
    else:
      self._joint.attach(objects[0].body._body, None)

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
    