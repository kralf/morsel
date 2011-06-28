from morsel.core.framework import *

from panda3d.pandac.Modules import BitMask32
from panda3d.pandac.Modules import NodePath
from panda3d.pandac.Modules import PandaNode

from panda3d.pandac.Modules import Geom
from panda3d.pandac.Modules import GeomLines
from panda3d.pandac.Modules import GeomVertexFormat
from panda3d.pandac.Modules import GeomVertexData
from panda3d.pandac.Modules import GeomVertexWriter
from panda3d.pandac.Modules import GeomNode


class LaserViewer( NodePath ):

#-------------------------------------------------------------------------------

  def __init__( self, name, laser, color = [0, 1, 1, 1] ):
    NodePath.__init__( self, name  )
    self.name  = name
    self.laser = laser
    self.color = color
    self._node = GeomNode( name + "GeomNode" )
    self.attachNewNode( self._node )
    self._node.adjustDrawMask( PandaNode.getAllCameraMask(), BitMask32( '001' ), BitMask32( '0' ) )
    self.setupRendering()
    
#-------------------------------------------------------------------------------

  def setupRendering( self ):
    format = GeomVertexFormat.getV3c4()
    self.geomdata   = GeomVertexData( 'scan', format, Geom.UHDynamic )
    vertex = GeomVertexWriter( self.geomdata, 'vertex' )
    color  = GeomVertexWriter( self.geomdata, 'color' )
    
    vertex.addData3f( 0, 0, 0 )
    color.addData4f( 0, 0, 0, 0 )
    for i in range( 0, self.laser.rayCount ):
      vertex.addData3f( 10, i - self.laser.rayCount / 2, 0 )
      color.addData4f( 0, 1, 1, 1 )
      
    line    = GeomLines( Geom.UHStatic )
    for i in range( 1, self.laser.rayCount + 1):
      line.addVertex( 0 )
      line.addVertex( i )
      line.closePrimitive()
    
    geom = Geom( self.geomdata )
    geom.addPrimitive( line )
    self._node.addGeom( geom )
    self.setTwoSided( 1 )
    self.setDepthWrite( 0 )
    self.setTransparency( 1 )

    scheduler.addTask( self.name + "ViewerTask", self.update )
  
#-------------------------------------------------------------------------------
  
  def update( self, time):
    if not self.isHidden(): # and len( self.laser.rays[0] ) > 0:
      self.updateRays()
    return True

#-------------------------------------------------------------------------------

  def updateRays( self ):
    v = GeomVertexWriter( self.geomdata, 'vertex' )
    v.setRow( 1 )
    c = GeomVertexWriter( self.geomdata, 'color' )
    c.setRow( 1 )
    for ri in range( self.laser.rayCount ):
      ray = self.laser.rays[ri]
      x = ray[2]
      y = ray[3]
      z = ray[4]
      r = ray[5]
      val = 1 - r / self.laser.rayRange[1]
      if r <= 0:
        val = 0
        x   = 0
        y   = 0
      v.setData3f( x, y, z )
      c.setData4f( self.color[0], self.color[1], self.color[2],  val )