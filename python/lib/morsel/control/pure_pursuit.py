from morsel.panda import *
from morsel.math import *
from morsel.nodes.controller import Controller
from morsel.nodes.facade import Path

#-------------------------------------------------------------------------------

class PurePursuit(Controller):
  def __init__(self, world, name = "PathFollow", path = None, velocity = 1,
      lookAhead = 1, waypoint = None, kidnap = True, epsilon = 1e-6, **kargs):
    Controller.__init__(self, world, name = name, **kargs)
    
    self.path = Path(name = name+"Path", filename = path, parent = self)
    
    self.velocity = velocity
    self.waypoint = waypoint
    self.lookAhead = lookAhead
    self.kidnap = kidnap
    self.epsilon = epsilon

    if self.waypoint == None:
      self.waypoint = self.getClosestWaypoint()

    if self.kidnap:
      self.actuator.setPosition(self.path.positions[self.waypoint], self)
      self.actuator.setOrientation(self.path.orientations[self.waypoint], self)

#-------------------------------------------------------------------------------

  def getLookAheadDistance(self, position):
    origin = panda.Point3(*self.actuator.getPosition(self))
    lookAhead = panda.Point3(*position)-origin
    
    return lookAhead.length()

#-------------------------------------------------------------------------------

  def getLookAheadAngle(self, position):
    origin = panda.Point3(*self.actuator.getPosition(self))
    heading = panda.Vec3(*self.actuator.getHeading(self))
    lookAhead = panda.Point3(*position)-origin
    lookAhead.normalize()

    return heading.signedAngleRad(lookAhead, panda.Vec3(0, 0, 1))*180/pi    

#-------------------------------------------------------------------------------

  def getLookAheadThreshold(self):
    return self.lookAhead*self.actuator.translationalVelocity[0]

  lookAheadThreshold = property(getLookAheadThreshold)

#-------------------------------------------------------------------------------

  def getArcDistance(self, position):
    lookAheadDistance = self.getLookAheadDistance(position)
    lookAheadAngle = self.getLookAheadAngle(position)

    if abs(sin(lookAheadAngle*pi/180)) >= self.epsilon:
      return lookAheadDistance/sin(lookAheadAngle*pi/180)*lookAheadAngle*pi/180
    else:
      return lookAheadDistance

#-------------------------------------------------------------------------------

  def getNextWaypoint(self, waypoint):
    origin = panda.Point3(*self.actuator.getPosition(self))
    for i in range(waypoint, self.path.numWaypoints):
      vector = panda.Vec3(*self.path.positions[i])-origin
      if vector.length() > self.lookAheadThreshold:
        return i
      
    if self.path.cyclic:
      return self.getNextWaypoint(0)
    else:
      return waypoint

#-------------------------------------------------------------------------------

  def getClosestWaypoint(self):
    closestWaypoint = 0
    minDistance = -1
    
    for i in range(0, self.path.numWaypoints):
      distance = self.getArcDistance(self.path.positions[i])
      if (minDistance < 0) or (distance < minDistance):
        closestWaypoint = i
        minDistance = distance

    return closestWaypoint

#-------------------------------------------------------------------------------

  def getInterpolatedPosition(self, waypoint):
    if (waypoint > 0) or self.path.cyclic:
      l_t = self.lookAheadThreshold
      if self.getLookAheadDistance(self.path.positions[self.waypoint-1]) < l_t:
        p_0 = panda.Point3(*self.actuator.getPosition(self))
        p_1 = panda.Point3(*self.path.positions[waypoint-1])
        p_2 = panda.Point3(*self.path.positions[waypoint])
        
        v_1 = p_2-p_0
        v_2 = p_1-p_0
        v_0 = p_2-p_1
        
        l_0 = v_0.length()
        l_1 = v_1.length()
        l_2 = v_2.length()
        
        v_0.normalize()
        v_2.normalize()
        alpha_1 = pi-v_0.angleRad(v_2)
        beta_2 = asin(l_2*sin(alpha_1)/l_t)
        beta_0 = pi-alpha_1-beta_2
        l_s = l_2*sin(beta_0)/sin(beta_2)
        p_s = p_1+v_0*l_s

        return [p_s[0], p_s[1], p_s[2]]

    return self.path.positions[waypoint]

#-------------------------------------------------------------------------------

  def updateCommand(self, period):
    self.waypoint = self.getNextWaypoint(self.waypoint)
    position = self.getInterpolatedPosition(self.waypoint)
    lookAheadDistance = self.getLookAheadDistance(position)
    lookAheadAngle = self.getLookAheadAngle(position)

    rotationalVelocity = 0
    if abs(sin(lookAheadAngle*pi/180)) >= self.epsilon:
      radius = 0.5*(lookAheadDistance/sin(lookAheadAngle*pi/180))
      if abs(radius) >= self.epsilon:
        rotationalVelocity = (self.actuator.translationalVelocity[0]/
          radius*180/pi)
  
    self.actuator.translationalVelocity = [self.velocity, 0, 0]
    self.actuator.rotationalVelocity = [rotationalVelocity, 0, 0]
