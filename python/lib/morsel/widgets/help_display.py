from label import Label

#-------------------------------------------------------------------------------

class HelpDisplay(Label):
  def __init__(self, anchor = ["Center", "Center"], origin = [0, 0], margin = 
      [1, 0.05], align = "Left", hidden = True, **kargs):
    super(HelpDisplay, self).__init__(anchor = anchor, origin = origin,
      margin = margin, align = align, hidden = hidden, **kargs)
      
#-------------------------------------------------------------------------------

  def setHidden(self, hidden):
    if self.hidden and not hidden:
      text = "%s [Build: %s on %s %s]\n\n" % (
        framework.configuration.fullName,
        framework.configuration.buildType,
        framework.configuration.buildSystem,
        framework.configuration.buildArchitecture)
      text += "Author(s): %s (%s)\n" % (
        framework.configuration.authors,
        framework.configuration.contact)
      text += "License: %s\n\n" % framework.configuration.license
      
      text += "You may use the following keyboard shortcuts:\n"
      for key in sorted(framework.shortcuts.iterkeys()):
        description = framework.shortcuts[key]
        text += "* "+key.upper()+": "+description+"\n"
        
      self.text = text
      
    Label.setHidden(self, hidden)
    
  hidden = property(Label.getHidden, setHidden)
  