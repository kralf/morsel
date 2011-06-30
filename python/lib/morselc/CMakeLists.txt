panda3d_python_package(
  COMMAND ${PANDA3D_GEN_PYCODE_EXECUTABLE}
  NAME morsel.morselc
)
remake_python_distribute(NAME morsel.morselc PACKAGES morsel.morselc
  DESCRIPTION "Python bindings")
