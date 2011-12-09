//GLSL

varying vec3 vertex;
varying vec3 normal;

#ifdef BUILDING_VSHADER
void main() {
  vertex = vec3(gl_ModelViewMatrix*gl_Vertex);
  normal = normalize(gl_NormalMatrix*gl_Normal);

  gl_Position = ftransform();
}
#endif

#ifdef BUILDING_FSHADER
const vec4 ambientBlack = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 diffuseBlack = vec4(0.0, 0.0, 0.0, 0.0);
const vec4 specularBlack = vec4(0.0, 0.0, 0.0, 0.0);

float attenuation(in int i, in float dist) {
  return(1.0/(gl_LightSource[i].constantAttenuation+
    gl_LightSource[i].linearAttenuation*dist+
    gl_LightSource[i].quadraticAttenuation*dist*dist));
}

void directionalLight(in int i, in vec3 n, in float shininess,
    inout vec4 ambient, inout vec4 diffuse, inout vec4 specular) {
  vec3 l = normalize(gl_LightSource[i].position.xyz);
  
  float ndotl = dot(n, l);
  
  if (ndotl > 0.0) {
    vec3 h = gl_LightSource[i].halfVector.xyz;
    
    float pf = pow(max(dot(n, h), 0.0), shininess);
    
    diffuse += gl_LightSource[i].diffuse*ndotl;
    specular += gl_LightSource[i].specular*pf;
  }
  
  ambient += gl_LightSource[i].ambient;
}

void pointLight(in int i, in vec3 n, in vec3 v, in float shininess,
    inout vec4 ambient, inout vec4 diffuse, inout vec4 specular) {
  vec3 d = gl_LightSource[i].position.xyz-v;
  vec3 l = normalize(d);
  
  float dist = length(d);
  float att = attenuation(i, dist);

  float ndotl = dot(n, l);

  if (ndotl > 0.0) {
    vec3 e = normalize(-v);
    vec3 r = reflect(-l, n);

    float pf = pow(max(dot(r, e), 0.0), shininess);

    diffuse += gl_LightSource[i].diffuse*att*ndotl;
    specular += gl_LightSource[i].specular*att*pf;
  }

  ambient += gl_LightSource[i].ambient*att;
}

void spotLight(in int i, in vec3 n, in vec3 v, in float shininess,
    inout vec4 ambient, inout vec4 diffuse, inout vec4 specular) {
  vec3 d = gl_LightSource[i].position.xyz-v;
  vec3 l = normalize(d);

  float dist = length(d);
  float att = attenuation(i, dist);

  float ndotl = dot(n, l);

  if (ndotl > 0.0) {
    float spotEffect = dot(normalize(gl_LightSource[i].spotDirection), -l);

    if (spotEffect > gl_LightSource[i].spotCosCutoff) {
      att *= pow(spotEffect, gl_LightSource[i].spotExponent);

      vec3 e = normalize(-v);
      vec3 r = reflect(-l, n);

      float pf = pow(max(dot(r, e), 0.0), shininess);

      diffuse += gl_LightSource[i].diffuse*att*ndotl;
      specular += gl_LightSource[i].specular*att*pf;
    }
  }

  ambient += gl_LightSource[i].ambient*att;
}

void light(in vec3 n, in vec3 v, in float shininess, inout vec4 ambient,
    inout vec4 diffuse, inout vec4 specular) {
  for (int i = 0; i < gl_MaxLights; ++i) {
    if (gl_LightSource[i].position.w == 0.0)
      directionalLight(i, n, shininess, ambient, diffuse, specular);
    else if (gl_LightSource[i].spotCutoff == 180.0)
      pointLight(i, n, v, shininess, ambient, diffuse, specular);
    else
      spotLight(i, n, v, shininess, ambient, diffuse, specular);
  }
}

void main() {
  vec4 ambient = ambientBlack;
  vec4 diffuse = diffuseBlack;
  vec4 specular = specularBlack;

  light(normal, vertex, gl_FrontMaterial.shininess, ambient, diffuse,
    specular);

  gl_FragColor = gl_LightModel.ambient*gl_FrontMaterial.ambient+
    ambient*gl_FrontMaterial.ambient+
    diffuse*gl_FrontMaterial.diffuse+
    specular*gl_FrontMaterial.specular;
}
#endif
