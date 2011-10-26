remake_project_set(BLENDER_DESTINATION ${CMAKE_INSTALL_PREFIX}/share/blender
  CACHE STRING "Install destination of project Blender scripts.")
remake_project_get(BLENDER_DESTINATION DESTINATION)
remake_add_files(*.py INSTALL ${BLENDER_DESTINATION}/scripts)
