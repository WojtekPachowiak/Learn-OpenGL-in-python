import os
import typer

#####################################

frag_template= """#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D texture_diffuse1;

void main()
{
    FragColor = texture(texture_diffuse1, TexCoords);
}"""

#####################################

vert_template = """#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoords;

out VS_OUT {
    vec2 texCoords;
} vs_out;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main()
{
    vs_out.texCoords = aTexCoords;
    gl_Position = projection * view * model * vec4(aPos, 1.0); 
}"""

#####################################

geom_template = """#version 330 core
layout (points) in;
layout (points, max_vertices = 1) out;

void main() {    
    gl_Position = gl_in[0].gl_Position; 
    EmitVertex();
    EndPrimitive();
}  """

#####################################

def main(shader_name:str, add_geometry:bool=False):
    paths = []
    for ext, src in zip([".frag",".geom", ".vert"], [frag_template, geom_template, vert_template]):
        if ext ==".geom" and add_geometry == False:
            continue
        p =  os.path.join("shaders", shader_name + ext) 
        assert not os.path.exists(p)
        with open(p, "w") as f:
            f.write(src)

    
if __name__ == "__main__":
    typer.run(main)