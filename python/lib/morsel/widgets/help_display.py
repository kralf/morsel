from label import Label

#-------------------------------------------------------------------------------

class HelpDisplay(Label):
  def __init__(self, gui, name = "HelpDisplay", anchor = ["Center", "Center"],
      origin = [0, 0], margin = [1, 1], align = "Left", hidden = True,
      **kargs):

    Label.__init__(self, gui, name, anchor = anchor, origin = origin,
      margin = margin, align = align, hidden = hidden, **kargs)
      
#-------------------------------------------------------------------------------

  def setHidden(self, hidden):
    if self.hidden and not hidden:
      text = "Framework keyboard shortcuts:\n\n"
      for (key, description) in framework.shortcuts.iteritems():
        text += key.upper()+": "+description+"\n"
        
      self.text = text
      
    Label.setHidden(self, hidden)
    
  hidden = property(Label.getHidden, setHidden)
  