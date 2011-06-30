from morsel.core import *
from math import pi
from panda3d.pandac import NodePath

class Arm( NodePath ):
  def __init__( self, name, joint_info, debug = False ):
    NodePath.__init__( self, name )
    self.debug      = debug
    self.joints     = []
    self.joint_info = joint_info

    self.root = NodePath( name + "root" )
    self.root.reparentTo( self )
    self.root.setH( -90 )
    #self.root.setP( 1 )

    for joint in joint_info:
      if not joint.get( "boxes" ):
        joint["boxes"] = []
      if not joint.get( "color" ):
        joint["color"] = [1, 1, 1, 1]
      self.add_joint( joint["position"], joint["rotation"], joint["boxes"], joint["color"] )


  #-----------------------------------------------------------------------------

  def get_configuration( self ):
    conf = [0.0] * len( self.joint_info )
    for i in xrange( len( conf ) ):
      axis = self.joint_info[i]["axis"]
      if axis == "x":
        conf[i] = self.joints[i].getP() * pi / 180
      elif axis == "y":
        conf[i] = self.joints[i].getR() * pi / 180
      elif axis == "z":
        conf[i] = self.joints[i].getH() * pi / 180
      elif axis == "x-":
        conf[i] = - self.joints[i].getP() * pi / 180
      elif axis == "y-":
        conf[i] = - self.joints[i].getR() * pi / 180
      elif axis == "z-":
        conf[i] = - self.joints[i].getH() * pi / 180
    return conf

  #-----------------------------------------------------------------------------

  def set_configuration( self, conf ):
    for i in xrange( len( conf ) ):
      axis = self.joint_info[i]["axis"]
      if axis == "x":
        self.joints[i].setP( conf[i] * 180 / pi )
      elif axis == "y":
        self.joints[i].setR( conf[i] * 180 / pi )
      elif axis == "z":
        self.joints[i].setH( conf[i] * 180 / pi )
      elif axis == "x-":
        self.joints[i].setP( -conf[i] * 180 / pi )
      elif axis == "y-":
        self.joints[i].setR( -conf[i] * 180 / pi )
      elif axis == "z-":
        self.joints[i].setH( -conf[i] * 180 / pi )

  #-----------------------------------------------------------------------------

  def add_joint( self, position, rotation, boxes, color = [1, 1, 1, 1] ):
    joint_idx = len( self.joints )
    joint     = NodePath( "%sj%i" % ( self.getName(), joint_idx) )
    if joint_idx > 0:
      joint.reparentTo( self.joints[ joint_idx - 1 ] )
    else:
      joint.reparentTo( self.root )
    joint.setHpr( *rotation)
    joint.setPos( *position )

    self.joints.append( joint )
    if self.debug:
      axis  = loadMesh(
        name     = "%sorigin%i" % ( self.getName(), joint_idx ),
        filename = "symbols/zup-axis.egg"
      )
      axis.setScale( 0.02 )
      axis.reparentTo( joint )

    for box_idx in xrange( len( boxes ) ):
      box  = loadMesh(
        name     = "%sbox%i%i" % ( self.getName(), joint_idx, box_idx ),
        filename = "geometry/cube.bam"
      )
      current = boxes[box_idx]
      box.setScale( *current["size"] )
      box.reparentTo( joint )
      box.setHpr( 0, 0, 0 )
      box.setPos( *current["position"] )
      if current.get( "rotation" ):
        box.setHpr( current["rotation"] )
      box.setColor( *color )