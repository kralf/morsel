from morsel.core.framework        import *
from panda3d.direct.gui.DirectGui  import DirectOptionMenu
from panda3d.direct.showbase       import DirectObject
from panda3d.pandac   import Mat4

class ObjectSelector( DirectObject.DirectObject ):
  def __init__( self ):
    self.menu = DirectOptionMenu( 
      text = "Attach camera to", 
      scale = 0.05,
      items = [],
      initialitem = 0,
      highlightColor = (0.65,0.65,0.65,1),
      command = self.select,
      textMayChange = 1
    )
    self.visible = False
    self.menu.hide()
    self.camera_poses = {}
    
  def select( self, item ):
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
    self.toggle()
    
  def toggle( self ):
    self.visible = not self.visible
    if self.visible:
      items = self.menu["items"]
      del items[:]
      i = 0
      selected = 0
      for k, v in meshes.iteritems():
        items.append( k )
        if k == base.camera.getParent().getName():
          selected = i
        i = i + 1
      self.menu["items"] = items
      self.menu.set( selected, 0 )
      self.menu.show()
    else:
      self.menu.hide()

