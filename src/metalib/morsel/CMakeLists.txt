panda3d_interrogate_module(
  morselc
  COMMAND ${PANDA3D_INTERROGATE_MODULE_EXECUTABLE}
  MODULE morsel
)

remake_add_library(
  morselc *.cpp PREFIX panda3d-
  FORCE_LINK input output sensors utils views ${PANDA3D_LIBRARIES}
)
remake_add_headers(*.h)
