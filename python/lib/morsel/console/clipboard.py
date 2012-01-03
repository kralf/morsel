import gtk, pygtk
import os
import sys

pygtk.require('2.0')

#-------------------------------------------------------------------------------

class Clipboard(object):
  def __init__(self):
    object.__init__(self)
    self.clipboard = gtk.clipboard_get()

#-------------------------------------------------------------------------------

  def getText(self):
    return self.clipboard.wait_for_text()
    
  def setText(self, text):
    self.clipboard.set_text(text)
    self.clipboard.store()

  text = property(getText, setText)
  