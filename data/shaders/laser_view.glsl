//GLSL

#ifdef BUILDING_VSHADER
uniform vec4 rangeLimits;
uniform sampler2D p3d_Texture0;
#ifdef HAVE_COLOR
uniform sampler2D p3d_Texture1;
#endif

void main() {
  vec4 position = vec4(0.0, 0.0, 0.0, 1.0);
  gl_FrontColor = gl_Color;

  if (gl_Vertex[2] > 0.0) {
    float depth = texture2D(p3d_Texture0, gl_MultiTexCoord0.st).r;
    float range = rangeLimits[1]*rangeLimits[0]/(rangeLimits[1]-
      depth*(rangeLimits[1]-rangeLimits[0]));

    if ((range > rangeLimits[0]) && (range < rangeLimits[1])) {
      position = vec4(range*gl_Vertex[0], range, range*gl_Vertex[1], 1.0);
#ifdef HAVE_COLOR
      gl_FrontColor = texture2D(p3d_Texture1, gl_MultiTexCoord0.st);
#endif
      gl_FrontColor[3] = 1.0-range/rangeLimits[1];
    }
    else
      gl_FrontColor[3] = 0.0;
  }

  gl_Position = gl_ModelViewProjectionMatrix*position;
}
#endif

#ifdef BUILDING_FSHADER
void main() {
  gl_FragColor = gl_Color;
}
#endif
