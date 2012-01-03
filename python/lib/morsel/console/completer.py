import re, __builtin__

#-------------------------------------------------------------------------------

class Completer(object):
  def __init__(self, locals):
    object.__init__(self)
    self.locals = locals
    
#-------------------------------------------------------------------------------

  def getMatches(self, text):
    words = text.split(".")
    matches = {}

    if len(words) > 2:
      object = words[0]
      prefix = ".".join(words[1:-1])
      if object in self.locals:
        exec("symbols = dir(self.locals[object].%s)" % prefix)
      else:
        exec("symbols = dir(__builtin__.__dict__[object].%s)" % prefix)
      for i in range(len(symbols)):
        symbols[i] = "%s.%s.%s" % (object, prefix, symbols[i])
    elif len(words) > 1:
      object = words[0]
      if object in self.locals:
        symbols = dir(self.locals[object])
      else:
        symbols = dir(__builtin__.__dict__[object])
      for i in range(len(symbols)):
        symbols[i] = "%s.%s" % (object, symbols[i])
    else:
      object = None
      symbols = __builtin__.__dict__.keys()
      symbols.extend(self.locals.keys())

    search = re.compile("^%s.*$" % text)

    for symbol in symbols:
      if re.match(search, symbol):
        if object:
          attributes = symbol.split(".")
          if object in self.locals:
            matches[symbol] = self.locals[object]
          else:
            matches[symbol] = __builtin__.__dict__[object]
          for i in range(1, len(attributes)):
            try:
              matches[symbol] = getattr(matches[symbol], attributes[i])
            except:
              del matches[symbol]
              break
        else:
          if symbol in self.locals:
            matches[symbol] = self.locals[symbol]
          else:
            matches[symbol] = getattr(__builtin__, symbol)
        
    return matches
