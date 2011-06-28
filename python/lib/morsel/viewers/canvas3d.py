from panda3d.pandac.Modules import GeomNode
from panda3d.pandac.Modules import GeomVertexFormat
from panda3d.pandac.Modules import GeomVertexData
from panda3d.pandac.Modules import GeomVertexWriter
from panda3d.pandac.Modules import GeomTriangles
from panda3d.pandac.Modules import Geom

class Canvas3D( GeomNode ):
  def __init__( self, name ):
    GeomNode.__init__( self, name )
    self.geometries = []
    self.format = GeomVertexFormat.getV3c4()

#-------------------------------------------------------------------------------

  def triangle( self, v1, v2, v3 ):
    triangle    = GeomTriangles( Geom.UHStatic )
    triangle.addVertex( v1 )
    triangle.addVertex( v2 )
    triangle.addVertex( v3 )
    return triangle

#-------------------------------------------------------------------------------

  def rectangle( self, geometry, v1, v2, v3, v4 ):
    geometry.addPrimitive( self.triangle( v1, v2, v3) )
    geometry.addPrimitive( self.triangle( v3, v4, v1) )

#-------------------------------------------------------------------------------

  def addBox( self, x1, y1, z1, x2, y2, z2, color ):
    geomdata     = GeomVertexData( 'rectangle', self.format, Geom.UHStatic )
    vertexWriter = GeomVertexWriter( geomdata, 'vertex' )
    colorWriter  = GeomVertexWriter( geomdata, 'color' )

    vertexWriter.addData3f( x1, y1, z1  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x1, y1, z2  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x1, y2, z1  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x1, y2, z2  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x2, y1, z1  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x2, y1, z2  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x2, y2, z1  )
    colorWriter.addData4f( *color )
    vertexWriter.addData3f( x2, y2, z2  )
    colorWriter.addData4f( *color )

    geometry = Geom( geomdata )
    self.rectangle( geometry, 0, 1, 3, 2 )
    self.rectangle( geometry, 4, 5, 7, 6 )
    self.rectangle( geometry, 0, 1, 5, 4 )
    self.rectangle( geometry, 2, 3, 7, 6 )
    self.rectangle( geometry, 1, 3, 7, 5 )
    self.addGeom( geometry )
