remake_project_get(CONFIGURATION_DESTINATION DESTINATION)
remake_project_get(FILE_DESTINATION DESTINATION)

remake_file_configure(*.remake)
remake_python_package(NAME morsel.config
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
