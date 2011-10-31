from morsel.panda import *
from node import Node
from morsel.math import Quaternion

#-------------------------------------------------------------------------------

class Path(Node):
  def __init__(self, world, name, filename = None, **kargs):
    Node.__init__(self, world, name, **kargs)

    self.filename = None
    self.positions = []
    self.orientations = []
    self.cyclic = False
    
    self.geometryData = panda.GeomVertexData(name+"Data",
      panda.GeomVertexFormat.getV3(), panda.Geom.UHDynamic)
    self.linestrips = panda.GeomLinestrips(panda.Geom.UHStatic)
    self.geometry = panda.Geom(self.geometryData)
    self.geometry.addPrimitive(self.linestrips)
    self.geometryNode = panda.GeomNode(name+"Geometry")
    self.geometryNode.addGeom(self.geometry)
    self.geometryNode.adjustDrawMask(panda.PandaNode.getAllCameraMask(),
      panda.BitMask32(1), panda.BitMask32(0));

    self.hide()
    self.attachNewNode(self.geometryNode)

    if filename:
      self.load(filename)

#-------------------------------------------------------------------------------

  def getNumWaypoints(self):
    return len(self.positions)

  numWaypoints = property(getNumWaypoints)

#-------------------------------------------------------------------------------

  def getClosestWaypoint(self, position, index = 0):
    point = panda.Point3(*position)
    minDistance = -1

    for i in range(index, self.numWaypoints):
      vector = panda.Vec3(*self.positions[i])-point
      distance = vector.lengthSquared()

      if minDistance >= 0:
        if distance < minDistance:
          minDistance = distance
          minIndex = i
      else:
        minDistance = distance
        minIndex = i

    return minIndex

#-------------------------------------------------------------------------------

  def load(self, filename):
    self.positions = []
    self.orientations = []
    self.cyclic = False
    self.linestrips.clearVertices()
    
    file = open(filename, "r")
    writer = panda.GeomVertexWriter(self.geometryData, "vertex")
    
    while file:
      line = file.readline()
      if line:
        split = line.split()
        position = [float(split[0]), float(split[1]), float(split[2])]
        self.positions.append(position)
        
        if len(self.positions) > 1:
          heading = (panda.Point3(*self.positions[-1])-
            panda.Point3(*self.positions[-2]))
          quaternion = Quaternion(heading)
          orientation = quaternion.getHpr()
          
          self.orientations.append([orientation[0], orientation[1],
            orientation[2]])
        
        writer.addData3f(*position)
        self.linestrips.addVertex(len(self.positions)-1)
      else:
        self.linestrips.closePrimitive()
        break

    file.close()
    self.filename = filename

    if self.positions:
      self.cyclic = (self.positions[0] == self.positions[-1])
      if self.cyclic:
        self.positions.pop(-1)
      else:
        self.orientations.append(self.orientations[-1])
