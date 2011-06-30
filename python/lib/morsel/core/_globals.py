from framework import *

#-------------------------------------------------------------------------------

#fullscreen( False )
windowSize( 1024, 768 )
panda.loadPrcFileData( "", "background-color 0.5 0.5 0.8" )
panda.loadPrcFileData( "", "show-buffers 0" ) # Crashes when set to 1
panda.loadPrcFileData( "", "prefer-parasite-buffer 0" )
panda.loadPrcFileData( "", "prefer-texture-buffer 1" )
panda.loadPrcFileData( "", "framebuffer-stereo 0" )
panda.loadPrcFileData( "", "depth-bits 16" )
panda.loadPrcFileData( "", "direct-gui-edit 1" )
