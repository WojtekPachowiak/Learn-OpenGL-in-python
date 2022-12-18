from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

class Shader:
    def __init__(self, name:str):
        #load fragment shader source
        with open(f"./shaders/{name}.frag", "r") as f:
            frag_src = f.read()
        #load vertex shader source
        with open(f"./shaders/{name}.vert", "r") as f:
            vert_src = f.read()
        self.program =  compileProgram(compileShader(vert_src, GL_VERTEX_SHADER), compileShader(frag_src, GL_FRAGMENT_SHADER))
        
    def use(self):
        glUseProgram(self.program)

    def set_mat4fv(self, uniform_name:str, value:glm.mat4):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, value)

    def set_vec3(self, uniform_name:str, value:glm.vec3):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform3fv(loc, 1, value); 