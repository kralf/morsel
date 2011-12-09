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

#include "shader_program.h"

#include <fstream>
#include <stdexcept>

using namespace std;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

ShaderProgram::ShaderProgram(string filename) {
  if (!filename.empty())
    load(filename);
}

ShaderProgram::ShaderProgram(const ShaderProgram& src) :
  filename(src.filename),
  text(src.text),
  definitions(src.definitions) {
}

ShaderProgram::~ShaderProgram() {
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

const string& ShaderProgram::getFilename() const {
  return filename;
}

string ShaderProgram::getLanguage() const {
  if (text.find("//") == 0)
    return string(text, 2, text.find_first_of(" \n", 2)-2);
  else
    throw runtime_error("Shader language not specified");
}

bool ShaderProgram::isEmpty() const {
  return text.empty();
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

bool ShaderProgram::load(string filename) {
  text.clear();

  ifstream file;
  file.open(filename.c_str(), ios::in);
  
  if (file.is_open()) {
    this->filename = filename;
    text.append((istreambuf_iterator<char>(file)),
      istreambuf_iterator<char>());
    return true;
  }
  else {
    this->filename.clear();
    return false;
  }

}

void ShaderProgram::define(string variable, string value) {
  definitions[variable] = value;
}

void ShaderProgram::undefine(std::string variable) {
  map<string, string>::iterator it = definitions.find(variable);
  if (it != definitions.end())
    definitions.erase(it);
}

PointerTo<Shader> ShaderProgram::make() {
  string language = getLanguage();
  if (language == "GLSL") {
    string vshader = text;
    define("BUILDING_VSHADER");
    preprocess(vshader);
    undefine("BUILDING_VSHADER");
    
    string fshader = text;
    define("BUILDING_FSHADER");
    preprocess(fshader);
    undefine("BUILDING_FSHADER");
    
    return Shader::make(Shader::SL_GLSL, vshader, fshader);
  }
  else if (language == "Cg") {
    string shaders = text;
    preprocess(shaders);
    return Shader::make(shaders, Shader::SL_Cg);
  }
  else
    throw runtime_error("Bad shader language");
}

void ShaderProgram::preprocess(string& text) {
  preprocessConditionals(text);
  
  for (map<string, string>::iterator it = definitions.begin();
      it != definitions.end(); ++it) {
    size_t varpos = text.find(it->first);
    while (varpos != string::npos) {
      text.replace(varpos, it->first.length(), it->second);
      varpos = text.find(it->first, varpos+it->second.length());
    }
  }
}

size_t ShaderProgram::preprocessConditionals(string& text, size_t pos) {
  size_t ifpos = text.find("#ifdef", pos);

  while (ifpos != string::npos) {
    size_t varpos = text.find_first_not_of(" ", ifpos+6);
    size_t endvarpos = text.find_first_of(" \n", varpos);
    string var(text, varpos, endvarpos-varpos);

    size_t endifpos = text.find("#endif", endvarpos);
    if (text.find("#ifdef", endvarpos) < endifpos)
      endifpos = text.find("#endif", preprocessConditionals(text,
        endvarpos));

    if (endifpos != string::npos) {
      if (definitions.find(var) != definitions.end()) {
        text.erase(ifpos, endvarpos-ifpos+1);
        endifpos -= endvarpos-ifpos+1;
        text.erase(endifpos, 7);
      }
      else {
        text.erase(ifpos, endifpos-ifpos+7);
        endifpos = ifpos;
      }
    }
    else
      throw runtime_error("Missing #endif in shader program");

    ifpos = text.find("#ifdef", endifpos);
  }

  return pos;
}
