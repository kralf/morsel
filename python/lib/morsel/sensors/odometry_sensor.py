from morsel.core.framework import *

from drives.differential import *

from panda3d.pandac.Modules import NodePath

from math import *

class OdometrySensor( NodePath ):
  def __init__( self, name, parent, period = 0.02):
    NodePath.__init__( self, name )
    self.name   = name
    self.parent = parent
    self.period = period
   
    # delta values
    self.dL     = 0
    self.dR     = 0

    self.dX     = 0
    self.dY     = 0
    self.dZ     = 0

    self.dPhi   = 0
    self.dTheta = 0
    self.dPsi   = 0

    # cumulated values
    self.cL     = 0
    self.cR     = 0

    self.cX     = 0
    self.cY     = 0
    self.cZ     = 0

    self.cPhi   = 0
    self.cTheta = 0
    self.cPsi   = 0

    # previous values (for calculating the delta values)
    self.pL     = 0
    self.pR     = 0

    self.pX     = self.parent.position[0]
    self.pY     = self.parent.position[1]
    self.pZ     = self.parent.position[2]

    self.pPhi   = self.parent.orientation[2]
    self.pTheta = self.parent.orientation[0]
    self.pPsi   = self.parent.orientation[1]

    scheduler.addTask( name + "Task", self.step, period  )

#-------------------------------------------------------------------------------

  def step( self, time ):

    ## in world coordinates:
    _dx = self.parent.position[0]    - self.pX
    _dy = self.parent.position[1]    - self.pY
    _dz = self.parent.position[2]    - self.pZ

    _dTheta = self.parent.orientation[0] - self.pTheta
    _dPhi   = self.parent.orientation[2] - self.pPhi
    _dPsi   = self.parent.orientation[1] - self.pPsi

    ## delta values
    self.dL     = 0    - self.pL
    self.dR     = 0    - self.pR

    self.dX     = sqrt(_dx*_dx+_dy*_dy)
    self.dY     = 0
    self.dZ     = _dz

    self.dPhi   = _dPhi
    self.dTheta = _dTheta
    self.dPsi   = _dPsi

    ## past values
    self.pL     = 0
    self.pR     = 0

    self.pX     = self.parent.position[0]
    self.pY     = self.parent.position[1]
    self.pZ     = self.parent.position[2]

    self.pPhi   = self.parent.orientation[2]
    self.pTheta = self.parent.orientation[0]
    self.pPsi   = self.parent.orientation[1]

    ## cumulative values
    self.cL     = self.cL     + self.dL
    self.cR     = self.cR     + self.dR

    self.cX     = self.cX     + self.dX*cos(self.cTheta)
    self.cY     = self.cY     + self.dX*sin(self.cTheta)
    self.cZ     = self.cZ     + self.dZ

    self.cPhi   = self.cPhi   + self.dPhi
    self.cTheta = self.cTheta + self.dTheta
    self.cPsi   = self.cPsi   + self.dPsi

    return True

#-------------------------------------------------------------------------------
