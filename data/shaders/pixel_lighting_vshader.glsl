varying vec3 vertex;
varying vec3 normal;

void main() {
  vertex = vec3(gl_ModelViewMatrix*gl_Vertex);
  normal = normalize(gl_NormalMatrix*gl_Normal);

  gl_Position = ftransform();
}
