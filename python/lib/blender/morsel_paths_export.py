#!BPY

"""
Name: 'Morsel Path (.pth)...'
Blender: 241
Group: 'Export'
Tooltip: 'Export to Morsel Path file format (.pth)'
"""

############################################################################
#    Copyright (C) 2007 by Ralf 'Decan' Kaestner                           #
#    ralf.kaestner@gmail.com                                               #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

__author__ = "Ralf Kaestner"

import Blender
from Blender import Scene
from Blender.Scene import *
from Blender import Object
from Blender.Object import *
from Blender import Curve
from Blender.Curve import *
import BPyMesh

import os, string

""" Blender Morsel Path export script
    @author Ralf Kaestner SU Computer Science Dept.
"""

def exportPath(curve, filename):
  print "Exporting curve "+curve.name+" to "+filename
  
  mesh = BPyMesh.getMeshFromObject(curve)
  mesh.transform(curve.matrixWorld)
  numVertices = len(mesh.verts)

  file = open(filename, "w")
  for i in range(0, numVertices):
    vertex = mesh.verts[i]
    file.write("%g %g %g\n" % (vertex.co[0], vertex.co[1], vertex.co[2]))
  if curve.data.isCyclic():
    vertex = mesh.verts[0]
    file.write("%g %g %g\n" % (vertex.co[0], vertex.co[1], vertex.co[2]))    
  file.close()

def exportPaths(filename):
  dirname = os.path.dirname(filename)
  scene = Scene.GetCurrent()

  for object in scene.objects:
    if object.type == "Curve":
      name = string.lower(object.name)
      exportPath(object, dirname+"/"+name+".pth")

if __name__ == "__main__":
  Blender.Window.FileSelector(exportPaths, "Export Morsel Paths", "*.pth")
