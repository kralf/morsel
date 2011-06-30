panda3d_interrogate_module(
  morselc
  COMMAND ${PANDA3D_INTERROGATE_MODULE_EXECUTABLE}
  MODULE morsel
)

remake_add_library(
  morselc PREFIX panda3d- LINK morsel ${PANDA3D_PANDA_LIBRARY}
)
