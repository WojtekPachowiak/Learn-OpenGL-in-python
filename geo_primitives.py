import numpy as np
from OpenGL.GL import *
import ctypes
import glm

class ScreenQuad:
    def __init__(self) -> None:
        vertices = glm.array(glm.float32,
            # positions        # texture Coords
            -1.0,  1.0, 0.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0, 0.0,
             1.0,  1.0, 0.0, 1.0, 1.0,
             1.0, -1.0, 0.0, 1.0, 0.0)

        vao = glGenVertexArrays(1);
        vbo = glGenBuffers(1);
        glBindVertexArray(vao);
        glBindBuffer(GL_ARRAY_BUFFER, vbo);
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW);
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * glm.sizeof(glm.float32), ctypes.c_void_p(0));
        glEnableVertexAttribArray(1);
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * glm.sizeof(glm.float32), ctypes.c_void_p(3 * glm.sizeof(glm.float32)));
        glBindBuffer(GL_ARRAY_BUFFER, 0);
        glBindVertexArray(0)
        self.vao = vao

    def Draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)
