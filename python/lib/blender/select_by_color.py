#!BPY

"""
Name: 'Select by Color'
Blender: 241
Group: 'Object'
Tooltip: 'Select all objects sharing the color of the selected object'
"""

############################################################################
#    Copyright (C) 2011 by Ralf Kaestner                                   #
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
from Blender import Object
from Blender import Draw

def error(what):
  Blender.Draw.PupMenu("Error: "+what)

def notice(what):
  Blender.Draw.PupMenu("Notice: "+what)

def selectObjects(material):
  for object in Object.Get():
    materials = object.getData(mesh = 1).materials

    for mat in materials:
      if (mat.getRGBCol() == material.getRGBCol()):
        object.select(True)
      else:
        object.select(False)

if __name__ == '__main__':
  selected = Object.GetSelected()

  if selected:
    materials = selected[0].getData(mesh = 1).materials
    if materials:
      selectObjects(materials[0])
    else:
      error("Selected object has no material")
  else:
    error("No object selected")

  notice("%d objects selected" % (len(Object.GetSelected())))
