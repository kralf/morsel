panda3d_interrogate(
  sensors
  COMMAND ${PANDA3D_INTERROGATE_EXECUTABLE}
  MODULE morsel
)

remake_add_library(sensors)
remake_add_headers(INSTALL sensors)
