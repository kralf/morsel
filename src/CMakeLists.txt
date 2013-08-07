remake_find_package(panda3d CONFIG)
remake_find_package(ZLIB)
remake_find_package(PythonLibs)

remake_find_executable(panda3d-interrogate)
remake_find_executable(panda3d-interrogate_module)
remake_find_executable(panda3d-gen_pycode)

remake_project_header(config.h.remake INSTALL)
remake_include(
  lib metalib
  ${PYTHON_INCLUDE_PATH}
  ${PANDA3D_INCLUDE_DIRS}
)
panda3d_interrogate_include(
  ${PANDA3D_INCLUDEDIR}
  ${PANDA3D_INCLUDEDIR}/parser-inc
)

remake_add_directories(lib)
remake_add_directories(metalib)
remake_pkg_config_generate(REQUIRES panda3d)
