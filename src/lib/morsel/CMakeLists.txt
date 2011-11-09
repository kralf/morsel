remake_add_directories()

remake_add_library(
  morsel PREFIX OFF
  LINK sensors views output utils ${PANDA3D_PANDA_LIBRARY}
)
remake_add_headers()
