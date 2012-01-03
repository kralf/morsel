from pipe import Pipe
from completer import Completer

from code import InteractiveConsole

import sys, os, inspect, string
import __builtin__

#-------------------------------------------------------------------------------

class Console(InteractiveConsole):
  def __init__(self, locals = __builtin__.globals()):
    InteractiveConsole.__init__(self, locals)

    self.stdout = sys.stdout
    self.stderr = sys.stderr
    
    self.pipe = Pipe()
    self.completer = Completer(locals)

#-------------------------------------------------------------------------------

  def redirectOutput(self, stdout, stderr):
    sys.stdout = stdout
    sys.stderr = stderr

#-------------------------------------------------------------------------------

  def push(self, input):
    self.redirectOutput(self.pipe, self.pipe)
    InteractiveConsole.push(self, input)
    self.redirectOutput(self.stdout, self.stderr)

    output = self.pipe.flush()

    return output

#-------------------------------------------------------------------------------

  def complete(self, input):
    completed = input
    candidates = []
    
    words = input.split(" ")
    matches = self.completer.getMatches(words[-1])

    for match in matches:
      if callable(matches[match]):
        candidates.append(match+"()")
      else:
        candidates.append(match)

    if len(matches) == 1:
      match = matches.iterkeys().next()
      words = words[0:-1]
      words.append(match)

      completed = " ".join(words)
      if callable(matches[match]):
        completed += "("

    return completed, candidates
  
#-------------------------------------------------------------------------------

  def help(self, input):
    text = None
    
    doc = self.push("%s.__doc__" % input)
    if ("Traceback" in doc) or ("SyntaxError" in doc):
      doc = None
    
    self.push("import inspect")
    src = self.push("inspect.getsourcelines(%s)[0][0:6]" % input)
    if ("Traceback" in src) or ("SyntaxError" in src):
      src = None
    
    if doc:
      exec("text = ''.join(%s)" % doc)
    elif src:
      exec("text = ''.join(%s)" % src)

    if text:
      text = text.strip(os.linesep)
    return text
