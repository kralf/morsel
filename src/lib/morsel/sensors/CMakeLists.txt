panda3d_interrogate_include(
  ${PANDA3D_PANDA_HEADERS}
  ${PANDA3D_PANDA_HEADERS}/parser-inc
)
panda3d_interrogate(
  sensors
  COMMAND ${PANDA3D_INTERROGATE_EXECUTABLE}
  SOURCES ${REMAKE_PROJECT_SOURCE_DIR}/lib
  MODULE morsel
)

remake_add_library(sensors)
remake_add_headers(INSTALL sensors)
