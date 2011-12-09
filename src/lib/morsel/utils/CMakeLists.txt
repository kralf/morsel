panda3d_interrogate_include(
  ${PANDA3D_PANDA_HEADERS}
  ${PANDA3D_PANDA_HEADERS}/parser-inc
)
panda3d_interrogate(
  utils
  COMMAND ${PANDA3D_INTERROGATE_EXECUTABLE}
  MODULE morsel
)

remake_add_library(utils LINK ${ZLIB_LIBRARY})
remake_add_headers(INSTALL utils)
