remake_project_set(BLENDER_SCRIPT_DESTINATION
  ${CMAKE_INSTALL_PREFIX}/share/blender/scripts
  CACHE STRING "Install destination of project Blender scripts.")

remake_project_get(BLENDER_SCRIPT_DESTINATION DESTINATION)
remake_add_files(*.py INSTALL ${BLENDER_SCRIPT_DESTINATION})
