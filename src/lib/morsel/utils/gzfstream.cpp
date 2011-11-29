/***************************************************************************
 *   Copyright (C) 2010 by Ralf Kaestner, Nikolas Engelhard, Yves Pilat    *
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
 *   59 Temple Place-Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#include "gzfstream.h"

#include <string.h>
#include <cstdio>

using namespace std;

/*****************************************************************************/
/* Statics                                                                   */
/*****************************************************************************/

size_t gzstreambuf::bufferSize = BUFSIZ;

/*****************************************************************************/
/* Constructors and Destructor                                               */
/*****************************************************************************/

gzstreambuf::gzstreambuf() :
    opened(0) {
  buffer = new char[bufferSize];
  setp(buffer, buffer+(bufferSize-1));
  setg(buffer+4, buffer+4, buffer+4);
}

gzstreambase::gzstreambase() {
  init(&buf);
}

gzstreambase::gzstreambase(const char* name, int mode) {
  init(&buf);
  open(name, mode);
}

gzifstream::gzifstream() :
  istream(&buf) {
}

gzifstream::gzifstream(const char* name, int open_mode) :
  gzstreambase(name, open_mode),
  istream(&buf) {
}

gzofstream::gzofstream() :
  ostream(&buf) {
}

gzofstream::gzofstream(const char* name, int mode) :
  gzstreambase(name, mode),
  ostream(&buf) {
}

gzstreambuf::~gzstreambuf() {
  close();
  delete[] buffer;
}

gzstreambase::~gzstreambase() {
  buf.close();
}

gzifstream::~gzifstream() {
}

gzofstream::~gzofstream() {
}

/*****************************************************************************/
/* Accessors                                                                 */
/*****************************************************************************/

int gzstreambuf::is_open() const {
  return opened;
}

streampos gzstreambuf::tell() {
  if (is_open())
    return gztell(file);
  return -1;
}

size_t gzstreambuf::filesize() const {
  return size;
}

int gzstreambase::is_open() const {
  return buf.is_open();
}

size_t gzstreambase::filesize() const {
  return buf.filesize();
}

streampos gzifstream::tellg() {
  return buf.tell();
}

streampos gzofstream::tellp() {
  return buf.tell();
}

/*****************************************************************************/
/* Methods                                                                   */
/*****************************************************************************/

gzstreambuf* gzstreambuf::open(const char* name, int open_mode) {
  if (is_open())
    return (gzstreambuf*)0;
  size = 0;
  mode = open_mode;
  // no append nor read/write mode
  if ((mode & ios::ate) || (mode & ios::app) ||
      ((mode & ios::in) && (mode & ios::out)))
    return (gzstreambuf*)0;
  char  fmode[10];
  char* fmodeptr = fmode;
  if (mode & ios::in)
      *fmodeptr++ = 'r';
  else if (mode & ios::out)
      *fmodeptr++ = 'w';
  *fmodeptr++ = 'b';
  *fmodeptr = '\0';
  file = gzopen(name, fmode);
  if (file == 0)
    return (gzstreambuf*)0;
  opened = 1;

  unsigned int size_buffer = 0;
  FILE* gzfile = fopen(name, "r");
  fseek(gzfile, -sizeof(size_buffer), SEEK_END);
  size_t numRead = fread(&size_buffer, sizeof(size_buffer), 1, gzfile);
  fclose(gzfile);
  size = size_buffer;

  return this;
}

gzstreambuf * gzstreambuf::close() {
  if (is_open()) {
    sync();
    opened = 0;
    size = 0;
    setg(0, 0, 0);
    if (gzclose(file) == Z_OK)
      return this;
  }
  return (gzstreambuf*)0;
}

void gzstreambuf::rewind() {
  if (is_open()) {
    setg(0, 0, 0);
    gzrewind(file);
  }
}

int gzstreambuf::overflow(int c) { // used for output buffer only
  if (!(mode & ios::out) || !opened)
    return EOF;
  if (c != EOF) {
    *pptr() = c;
    pbump(1);
  }
  if (flush_buffer() == EOF)
    return EOF;
  return c;
}

int gzstreambuf::underflow() { // used for input buffer only
  if (gptr() && (gptr() < egptr()))
    return *reinterpret_cast<unsigned char *>(gptr());

  if (!(mode & ios::in) || !opened)
    return EOF;
  // Josuttis' implementation of inbuf
  int n_putback = gptr()-eback();
  if (n_putback > 4)
    n_putback = 4;
  memcpy(buffer+(4-n_putback), gptr()-n_putback, n_putback);

  int num = gzread(file, buffer+4, bufferSize-4);
  if (num <= 0) // ERROR or EOF
    return EOF;

  // reset buffer pointers
  setg(buffer+(4-n_putback),   // beginning of putback area
    buffer+4,                 // read position
    buffer+4+num);          // end of buffer

  // return next character
  return * reinterpret_cast<unsigned char *>(gptr());
}

int gzstreambuf::sync() {
  // Changed to use flush_buffer() instead of overflow(EOF)
  // which caused improper behavior with endl and flush(),
  // bug reported by Vincent Ricard.
  if (pptr() && pptr() > pbase()) {
    if (flush_buffer() == EOF)
      return -1;
  }
  return 0;
}

int gzstreambuf::flush_buffer() {
  // Separate the writing of the buffer from overflow() and
  // sync() operation.
  int w = pptr()-pbase();
  if (gzwrite(file, pbase(), w)) {
    setp(pbase(), epptr()-1);
    return w;
  }
  return EOF;
}

void gzstreambase::open(const char* name, int open_mode) {
  if (!buf.open(name, open_mode))
    clear(rdstate() & ios::badbit);
}

void gzstreambase::close() {
  if (buf.is_open())
    if (!buf.close())
      clear(rdstate() & ios::badbit);
}

void gzstreambase::rewind() {
  buf.rewind();
}

gzstreambuf* gzstreambase::rdbuf() {
  return &buf;
}

void gzifstream::open(const char* name, int open_mode) {
  gzstreambase::open(name, open_mode);
}

gzstreambuf* gzifstream::rdbuf() {
  return gzstreambase::rdbuf();
}

void gzofstream::open(const char* name, int open_mode) {
  gzstreambase::open(name, open_mode);
}

gzstreambuf* gzofstream::rdbuf() {
  return gzstreambase::rdbuf();
}
