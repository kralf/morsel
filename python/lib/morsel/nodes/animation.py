from node import Node
from panda3d.direct.actor.Actor import Actor

import math

#-------------------------------------------------------------------------------

class Animation(Node):
  def __init__(self, world, name, mesh, animation = None, startFrame = 0,
      endFrame = None, loop = True, parent = None, **kargs):
    Node.__init__(self, world, name, parent = mesh.model, **kargs)

    self.mesh = mesh
    self.animation = animation
    self.startFrame = startFrame
    self.endFrame = endFrame
    self.loop = loop
    
    self.actor = Actor(mesh.model)

    if not self.animation:
      self.animation = self.actor.getAnimNames()[0]
    if not self.endFrame:
      self.endFrame = self.actor.getNumFrames(self.animation)-1
    self.numFrames = (self.endFrame-self.startFrame)+1
    self.duration = self.actor.getDuration(self.animation)

#-------------------------------------------------------------------------------

  def getActor(self):
    return self._actor

  def setActor(self, actor):
    self._actor = actor
    self._actor.reparentTo(self.mesh.model)

  actor = property(getActor, setActor)

#-------------------------------------------------------------------------------

  def updateGraphics(self):
    if self.loop:
      time = self.world.time-math.floor(self.world.time/
        self.duration)*self.duration
    else:
      time = min(self.world.time, self.duration)
      
    frame = self.startFrame+round(self.numFrames*time/self.duration)
    self.actor.pose(self.animation, frame)
    