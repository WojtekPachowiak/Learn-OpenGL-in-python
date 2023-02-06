#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D depthMap;
uniform float near_plane;
uniform float far_plane;


float linearize_depth(float depth){
    float z = depth * 2.0 - 1.0;
    return (2.0 * far_plane * near_plane) / (far_plane + near_plane - z * (far_plane - near_plane));
}

void main()
{
    float depthValue = texture(depthMap, TexCoords).r;
    FragColor = vec4(vec3(linearize_depth(depthValue) / far_plane), 1.0); 
    // FragColor = vec4(vec3(depthValue), 1.0);
}