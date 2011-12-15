from morsel.panda import *
from label import Label

#-------------------------------------------------------------------------------

class SceneDisplay(Label):
  def __init__(self, gui, name = "SceneDisplay", anchor = ["Center", "Bottom"],
      origin = [0, -1], margin = [0.5, 0.3], hidden = True, **kargs):

    Label.__init__(self, gui, name, anchor = anchor, origin = origin,
      margin = margin, hidden = hidden, **kargs)
  
#-------------------------------------------------------------------------------

  def setHidden(self, hidden):
    if self.hidden and not hidden:
      if framework.world and framework.world.scene:
        scene = framework.world.scene
        analyzer = panda.SceneGraphAnalyzer()
        analyzer.addNode(scene.node())
        
        text = "Scene: %s / Layer: %s\n" % (scene.name,
          framework.layers[scene.activeLayer])
        text += ("(Nodes: %d, Vertices: %d, Faces: %d, Memory: %.2f MB)" %
          (analyzer.getNumNodes(), analyzer.getNumVertices(),
          analyzer.getNumTris(), (analyzer.getVertexDataSize()+
          analyzer.getTextureBytes())/float(2**20)))
      else:
        text = "Scene statistics n/a"

      self.text = text
      
    Label.setHidden(self, hidden)
    
  hidden = property(Label.getHidden, setHidden)
  