from canvas3d import *
from morsel.core.framework import *
from panda3d.pandac import PandaNode
from panda3d.pandac import BitMask32

class DetectionViewer:
  def __init__( self, detector ):
    scheduler.addTask( detector.name + "Viewer", self.step )
    self.detector = detector
    self.nodes  = {}
    
  def getNode( self, obj ):
    if not self.nodes.has_key( obj ):
      canvas   = Canvas3D( self.detector.name + obj.getName() + "Viewer" )
      canvas.adjustDrawMask( PandaNode.getAllCameraMask(), BitMask32( '001' ), BitMask32( '0' ) )

      b = self.detector.getBounds( obj )
      canvas.addBox( b[0][0], b[0][1], b[0][2], b[1][0], b[1][1], b[1][2], [1, 1, 0, 0.3] )

      node     = obj.attachNewNode( canvas )
      node.setTwoSided( 1 )
      node.setTransparency( 1 )
      self.nodes[obj] = node
    return self.nodes[obj]
    
  def step( self, time ):
    for n in self.nodes.values():
      n.hide()
    for p in self.detector.detections:
      n = self.getNode( p[1] )
      n.show()
    return True