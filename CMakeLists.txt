cmake_minimum_required(VERSION 2.6)

include(ReMake)

remake_project(
  Morsel
  VERSION 1.3
  RELEASE beta
  SUMMARY "MObile Robot Simulator."
  AUTHOR "Dizan Vasquez"
  CONTACT "vasquez@mavt.ethz.ch"
  HOME "http://aslforge.ethz.ch/projects/morsel"
  LICENSE "GNU General Public License (GPL)"
  INSTALL /usr
)

remake_python()
remake_add_directories(
  data
  COMPONENT data
)
remake_doc(
  html
)

remake_pack_deb(
  panda3d-python
)
remake_pack_deb(
  ARCH all
  COMPONENT data
  DESCRIPTION "data"
  morsel
)
