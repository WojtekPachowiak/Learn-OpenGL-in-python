# version 330

in vec2 v_texture;

out vec4 FragColor;

uniform sampler2D s_texture;

void main()
{
    FragColor = texture(s_texture, v_texture);
}



