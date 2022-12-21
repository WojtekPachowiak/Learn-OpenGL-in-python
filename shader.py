from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import os
class Shader:
    def __init__(self, name:str):
        shaders=[]
        #load fragment shader source
        with open(f"./shaders/{name}.frag", "r") as f:
            frag_src = f.read()
            shaders.append(compileShader(frag_src, GL_FRAGMENT_SHADER))
        #load vertex shader source
        with open(f"./shaders/{name}.vert", "r") as f:
            vert_src = f.read()
            shaders.append(compileShader(vert_src, GL_VERTEX_SHADER))
        #load geometry shader source
        if os.path.exists(f"./shaders/{name}.geom"):
            with open(f"./shaders/{name}.geom", "r") as f:
                geom_src = f.read()
                shaders.append(compileShader(geom_src, GL_GEOMETRY_SHADER))
        self.program =  compileProgram(*shaders)
        
    def use(self):
        glUseProgram(self.program)

    def set_mat4fv(self, uniform_name:str, value:glm.mat4):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, value)

    def set_vec3(self, uniform_name:str, value:glm.vec3, count=1):   
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform3fv(loc, count, value); 
    
    def set_vec4(self, uniform_name:str, value:glm.vec4, count=1): 
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform4fv(loc, count, value); 
    
    def set_vec2(self, uniform_name:str, value:glm.vec2, count=1):   
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform2fv(loc, count, value); 

    def set_float(self, uniform_name:str, value:float):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform1f(loc, value)

    def set_int(self, uniform_name:str, value:int):
        loc = glGetUniformLocation(self.program, uniform_name)
        glUniform1i(loc, value)
    