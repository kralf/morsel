from node import Node
from panda3d.direct.actor.Actor import Actor

import math

#-------------------------------------------------------------------------------

class Animation(Node):
  def __init__(self, name, mesh, animation = None, startFrame = 0,
      endFrame = None, loop = True, parent = None, **kargs):
    Node.__init__(self, name, parent = mesh.model, **kargs)

    self.mesh = mesh
    self.animation = animation
    self.startFrame = startFrame
    self.endFrame = endFrame
    self.loop = loop

    for layer in self.mesh.layers:
      actor = Actor(self.mesh.getModel(layer))
      self.setActor(actor, layer)
      if not self.animation:
        self.setAnimation(actor.getAnimNames()[0])
      
    if not self.endFrame:
      self.endFrame = self.actor.getNumFrames(self.animation)-1
    self.numFrames = (self.endFrame-self.startFrame)+1
    self.duration = self.actor.getDuration(self.animation)

#-------------------------------------------------------------------------------

  def getActor(self, layer = None):    
    if layer:
      return self._actor[layer]
    else:
      return self._actor

  def setActor(self, actor, layer = None):
    if layer:
      if not hasattr(self, "_actor"):
        self._actor = {}
      self._actor[layer] = actor
      actor.reparentTo(self.mesh.getModel(layer))
    else:
      self._actor = actor
      actor.reparentTo(self.mesh.model)

  actor = property(getActor, setActor)

#-------------------------------------------------------------------------------

  def getActors(self):
    if isinstance(self._actor, dict):
      return self._actor.itervalues()
    else:
      return [self._actor]

  actors = property(getActors)

#-------------------------------------------------------------------------------

  def getAnimation(self, layer = None):
    if layer:
      return self._animation[layer]
    else:
      return self._animation

  def setAnimation(self, animation, layer = None):
    if layer:
      if not hasattr(self, "_animation"):
        self._animation = {}
      self._animation[layer] = animation
    else:
      self._animation = animation

  animation = property(getAnimation, setAnimation)

#-------------------------------------------------------------------------------

  def getAnimations(self):
    if isinstance(self._animation, dict):
      return self._animation.itervalues()
    else:
      return [self._animation]

  animations = property(getAnimations)

#-------------------------------------------------------------------------------

  def step(self, time):
    if self.loop:
      time = time-math.floor(time/self.duration)*self.duration
    else:
      time = min(time, self.duration)
      
    frame = self.startFrame+round(self.numFrames*time/self.duration)

    for layer in self.mesh.layers:
      self.getActor(layer).pose(self.getAnimation(layer), frame)
    