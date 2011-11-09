/***************************************************************************
 *   Copyright (C) 2011 by Ralf Kaestner                                   *
 *   ralf.kaestner@gmail.com                                               *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifndef LASER_VIEW_H
#define LASER_VIEW_H

/** Laser view implementation
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include <nodePath.h>

class RangeSensor;

class LaserView :
  public NodePath {
PUBLISHED:
  /** Constructors
    */
  LaserView(std::string name, NodePath& sensor, const Colorf& color,
    bool showPoints = true, bool showLines = false, bool showColors = false,
    bool showLabels = false);

  /** Destructor
    */
  virtual ~LaserView();

  bool update(double time);
protected:
  RangeSensor& sensor;
  Colorf color;
  bool showPoints;
  bool showLines;
  bool showColors;
  bool showLabels;
  PointerTo<Shader> pointShader;

  std::vector<GeomNode*> nodes;
  std::vector<GeomVertexData*> geomData;
  
  void setupRendering();
};

#endif
