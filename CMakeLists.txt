cmake_minimum_required(VERSION 2.6)

include(ReMake)
include(Panda3D)

remake_project(
  Morsel
  VERSION 1.4
  RELEASE beta
  SUMMARY "MObile Robot Simulator."
  AUTHOR "Ralf Kaestner"
  AUTHOR "Dizan Vasquez"
  CONTACT "ralf.kaestner@gmail.com"
  HOME "http://github.com/kralf/morsel"
  LICENSE "GNU General Public License (GPL)"
  INSTALL /usr
)

remake_add_directories(
  python
)
remake_add_directories(
  data
  COMPONENT data
)
remake_doc(
  html
)

remake_pack_deb(
  DEPENDS panda3d
)
remake_pack_deb(
  COMPONENT dev
  DESCRIPTION "development headers"
  DEPENDS morsel panda3d-dev
)
remake_pack_deb(
  COMPONENT python
  DEPENDS morsel panda3d-python
)
remake_pack_deb(
  ARCH all
  COMPONENT data
  DESCRIPTION "data"
  DEPENDS morsel panda3d-models
)
remake_pack_deb(
  ARCH all
  COMPONENT blender
  DESCRIPTION "blender scripts"
  DEPENDS blender panda3d-blender
)

remake_distribute_deb(
  DISTRIBUTION lucid
  SECTION python
  UPLOAD ppa:kralf/asl
  DEPENDS panda3d-dev panda3d-python panda3d-models panda3d-blender
    remake pkg-config doxygen
  PASS CMAKE_BUILD_TYPE MORSEL_GIT_REVISION
  EXCLUDE "[.]blend$"
)
remake_distribute_deb(
  DISTRIBUTION precise
  SECTION python
  UPLOAD ppa:kralf/asl
  DEPENDS panda3d-dev panda3d-python panda3d-models panda3d-blender
    remake pkg-config doxygen
  PASS CMAKE_BUILD_TYPE MORSEL_GIT_REVISION
  EXCLUDE "[.]blend$"
)
