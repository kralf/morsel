remake_add_directories(config morsel)
remake_python_distribute(PACKAGES morsel morsel.config)
remake_add_directories(morselc)

remake_add_directories(
  blender
  COMPONENT blender
)
