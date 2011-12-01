remake_project_header(config.h.remake)
remake_include(
  ${CMAKE_CURRENT_BINARY_DIR}/..
)

remake_add_directories()

remake_add_library(
  morsel PREFIX OFF
  LINK sensors views input output utils ${PANDA3D_PANDA_LIBRARY}
)
remake_add_headers()
