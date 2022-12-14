
# version 330

in vec2 v_texture;

out vec4 FragColor;

float near = 0.1; 
float far  = 100.0; 
  
uniform sampler2D s_texture;

float LinearizeDepth(float depth) 
{
    float z = depth * 2.0 - 1.0; // back to NDC 
    return (2.0 * near * far) / (far + near - z * (far - near));	
}

void main()
{
    FragColor = vec4(vec3(LinearizeDepth(gl_FragCoord.z)/ far), 1.0);  

    // FragColor = vec4(vec3(gl_FragCoord.z), 1.0);  

    // FragColor = texture(s_texture, v_texture);
}



