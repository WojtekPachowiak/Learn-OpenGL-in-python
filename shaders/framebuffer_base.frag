#version 330 core
out vec4 FragColor;
  
in vec2 TexCoords;

uniform sampler2D screenTexture;

void main()
{ 
    FragColor = texture(screenTexture, TexCoords);
    vec4 col = vec4(vec3(1.)-FragColor.xyz,1.);
    col.r = 0.;
    FragColor = col;
}