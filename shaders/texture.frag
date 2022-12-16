# version 330

in vec2 v_texture;

out vec4 FragColor;

uniform sampler2D s_texture;

void main()
{
    vec4 texColor = texture(s_texture, v_texture);

    FragColor = texColor;
    
}



