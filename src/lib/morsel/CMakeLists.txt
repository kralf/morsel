remake_project_header(config.h.remake)
remake_include(
  ${CMAKE_CURRENT_BINARY_DIR}/..
)

remake_add_directories()

remake_add_library(morsel PREFIX OFF)
remake_add_headers()
