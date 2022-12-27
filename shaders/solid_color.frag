#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D texture_diffuse1;

void main()
{   
    // FragColor = texture(texture_diffuse1, TexCoords);
    FragColor = vec4(vec3(0.9137, 0.0392, 0.0392),1.);
}