panda3d_interrogate(
  views
  COMMAND ${PANDA3D_INTERROGATE_EXECUTABLE}
  MODULE morsel
)

remake_add_library(views)
remake_add_headers(INSTALL views)
