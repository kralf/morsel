from object_selector         import ObjectSelector
from morsel.core                    import *

from panda3d.direct.gui.DirectGui    import DirectFrame, DGG
from panda3d.direct.gui.DirectGui    import DirectOptionMenu
from panda3d.direct.gui.OnscreenText import OnscreenText
from panda3d.direct.showbase         import DirectObject


from panda3d.pandac     import TextNode
from panda3d.pandac     import Mat4

class ObjectProperties( DirectObject.DirectObject ):
  ''' Gui for object selection and displaying basic proerties.'''
  V_SPACING   = 1.3
  H_SPACING   = 1.3
  FRAME_COLOR = ( 200, 200, 200, 0.5 )
  TEXT_COLOR  = ( 0.8, 0.8, 0.8, 0.8 )
  NO_COLOR    = ( 0, 0, 0, 0 )
  HL_COLOR    = ( 0.65, 0.65, 0.65, 1 )
  SCALE       = 0.05

#-------------------------------------------------------------------------------

  def __init__( self, toggleKey = "f9" ):
    self.top = 0.5 / self.SCALE
    self.frame   = DirectFrame( 
      relief     = DGG.GROOVE, 
      frameColor = self.FRAME_COLOR,
      frameSize  = ( 0, 0.8 / self.SCALE, 0, self.top ),
      pos        = ( -0.5, 0, -0.5 ),
      scale      = self.SCALE
    )
    self.label( "Current Object", 1, 1 )
    self.objectMenu = DirectOptionMenu( 
      parent         = self.frame,
      items          = [],
      initialitem    = 0,
      command        = self.objectMenuSelect,
      textMayChange  = 1
    )
    self.layout( self.objectMenu, 8, 1 )
    self.label ( "Position", 1, 2, )
    self.positionLabel = self.label( "", 8, 2 )
    self.label ( "Orientation", 1, 3, )
    self.orientationLabel = self.label( "", 8, 3 )
    
    self.frame.hide()
    self.accept( 'window-event', self.windowEvent )
    self.camera_poses = {}
    scheduler.addTask( "objectProperties", self.update )
    
#-------------------------------------------------------------------------------
  def label( self, text, x, y ):
    result = OnscreenText( 
      parent    = self.frame, 
      mayChange = True,
      text      = text,
      scale     = 1,
      fg        = self.TEXT_COLOR,
      align     = TextNode.ALeft
    ) 
    result.setPos( x, self.top - y * self.V_SPACING )
    return result

#-------------------------------------------------------------------------------

  def layout( self, widget, x, y ):
    widget["scale"]          = 1
    widget["text_fg"]        = self.TEXT_COLOR
    widget["text_align"]     = TextNode.ALeft
    widget["highlightColor"] = self.HL_COLOR,
    widget.setPos( x, 0, self.top - y * self.V_SPACING )
    widget.resetFrameSize()

#-------------------------------------------------------------------------------

  def objectMenuSelect( self, item ):
    mat = Mat4( base.camera.getMat() )
    mat.invertInPlace()
    key = base.camera.getParent().getName()
    self.camera_poses[key] = mat
    base.camera.reparentTo( meshes[item] )
    if self.camera_poses.has_key( item ):
      mat = self.camera_poses[item]
      base.mouseInterfaceNode.setMat( mat )
    else:
      base.camera.setPos( -10, -5, 5 )
      base.camera.lookAt( 5, 0, 0 )
      mat = Mat4( base.camera.getMat() )
      mat.invertInPlace()
      base.mouseInterfaceNode.setMat( mat )
    self.objectMenuUpdate()

#-------------------------------------------------------------------------------

  def toggle( self ):
    self.frame.toggleVis()
    if not self.frame.isHidden():
      self.update()
    self.frame.setPos( 0, 0, 0 )
    self.windowEvent( base.win )

#-------------------------------------------------------------------------------

  def update( self, task = None ):
    if not self.frame.isHidden():
      self.objectPropertiesUpdate()
    if not task:
      self.objectMenuUpdate()
    return True

#-------------------------------------------------------------------------------

  def objectPropertiesUpdate( self ):
    current = base.camera.getParent()
    pos = current.getPos()
    self.positionLabel.setText( "%.2f, %.2f, %.2f" % ( pos[0], pos[1], pos[2] ) )
    hpr = current.getHpr()
    self.orientationLabel.setText( "%.2f, %.2f, %.2f" % ( hpr[0], hpr[1], hpr[2] ) )

#-------------------------------------------------------------------------------

  def objectMenuUpdate( self ):
    items = self.objectMenu["items"]
    del items[:]
    i = 0
    selected = 0
    for k, v in meshes.iteritems():
      items.append( k )
      if k == base.camera.getParent().getName():
        selected = i
      i = i + 1
    self.objectMenu["items"] = items
    if len( items ) > 0:
      self.objectMenu.set( selected, 0 )
      self.objectMenu["text_align"] = TextNode.ALeft
      self.objectMenu.resetFrameSize()
      
  def windowEvent( self, window ):
    self.frame.setPos( -0.5, 0, -0.5 )
    