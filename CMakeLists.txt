cmake_minimum_required(VERSION 2.6)

include(ReMake)
include(Panda3D)

remake_project(
  Morsel
  VERSION 1.3
  RELEASE beta
  SUMMARY "MObile Robot Simulator."
  AUTHOR "Ralf Kaestner"
  AUTHOR "Dizan Vasquez"
  CONTACT "ralf.kaestner@gmail.com"
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
  panda3d
)
remake_pack_deb(
  COMPONENT dev
  DESCRIPTION "development headers"
  morsel panda3d-dev
)
remake_pack_deb(
  COMPONENT python
  morsel panda3d-python
)
remake_pack_deb(
  ARCH all
  COMPONENT data
  DESCRIPTION "data"
  morsel
)
remake_pack_deb(
  ARCH all
  COMPONENT blender
  DESCRIPTION "blender scripts"
  blender
)

remake_distribute_deb(
  DISTRIBUTION lucid
  SECTION python
  UPLOAD ppa:kralf/asl
  DEPENDS remake panda3d-dev panda3d-python
  PASS CMAKE_BUILD_TYPE MORSEL_SUBVERSION_REVISION
  EXCLUDE "[.]blend$"
)
