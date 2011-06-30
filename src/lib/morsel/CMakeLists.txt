remake_add_directories()

remake_add_library(
  morsel PREFIX OFF
  LINK sensors ${PANDA3D_PANDA_LIBRARY}
)
remake_add_headers()
