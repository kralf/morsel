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

#ifndef GZFSTREAM_H
#define GZFSTREAM_H

/** Gzip file stream
  * @author Ralf Kaestner ETHZ Autonomous Systems Lab.
  */

#include <iostream>
#include <fstream>
#include <zlib.h>

class gzstreambuf : public std::streambuf {
public:
  /** Constructors
    */
  gzstreambuf();

  /** Destructor
    */
  ~gzstreambuf();
  
  int is_open() const;
  std::streampos tell();
  size_t filesize() const;

  gzstreambuf* open(const char* name, int open_mode);
  gzstreambuf* close();
  void rewind();

  virtual int overflow(int c = EOF);
  virtual int underflow();
  virtual int sync();
protected:
  static size_t bufferSize;  // size of data buff

  void* file;                // file handle for compressed file
  char* buffer;              // data buffer
  char opened;               // open/close state of stream
  int mode;                  // I/O mode
  size_t size;

  int flush_buffer();
};

class gzstreambase : virtual public std::ios {
public:
  /** Constructors
    */
  gzstreambase();
  gzstreambase(const char* name, int open_mode);

  /** Destructor
    */
  ~gzstreambase();
  
  int is_open() const;
  size_t filesize() const;

  void open(const char* name, int open_mode);
  void close();
  void rewind();
  gzstreambuf* rdbuf();
protected:
  gzstreambuf buf;
};

class gzifstream : public gzstreambase, public std::istream {
public:
  /** Constructors
    */
  gzifstream();
  gzifstream(const char* name, int open_mode = std::ios::in);

  /** Destructor
    */
  ~gzifstream();

  std::streampos tellg();

  void open(const char* name, int open_mode = std::ios::in);
  gzstreambuf* rdbuf();
};

class gzofstream : public gzstreambase, public std::ostream {
public:
  /** Constructors
    */
  gzofstream();
  gzofstream(const char* name, int mode = std::ios::out);

  /** Destructor
    */
  ~gzofstream();

  std::streampos tellp();
    
  void open(const char* name, int open_mode = std::ios::out);
  gzstreambuf* rdbuf();
};

#endif
