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

#ifndef SHADER_PROGRAM_H
#define SHADER_PROGRAM_H

/** Shader program implementation
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include "morsel/morsel.h"

#include <map>

#include <shader.h>

class ShaderProgram {
PUBLISHED:
  /** Constructors
    */
  ShaderProgram(std::string filename = "");
  ShaderProgram(const ShaderProgram& src);

  /** Destructor
    */
  virtual ~ShaderProgram();

  const std::string& getFilename() const;
  std::string getLanguage() const;
  bool isEmpty() const;
  
  bool load(std::string filename);
  PointerTo<Shader> make();
  void define(std::string variable, std::string value = "");
  void undefine(std::string variable);
protected:
  std::string filename;
  std::string text;
  
  std::map<std::string, std::string> definitions;

  void preprocess(std::string& text);
  size_t preprocessConditionals(std::string& text, size_t pos = 0);
};

#endif
