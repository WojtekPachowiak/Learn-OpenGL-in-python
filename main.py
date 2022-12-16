import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from TextureLoader import load_texture_pygame, TEXTURE_WRAP
from ObjLoader import ObjLoader
import glm
from camera import Camera

# CAMERA settings
cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True


vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


def mouse_look(xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)


pygame.init()
pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE) # |pygame.FULLSCREEN

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# load here the 3d meshes
cube_indices, cube_buffer = ObjLoader.load_model("meshes/cube.obj", False)
monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/monkey.obj")
floor_indices, floor_buffer = ObjLoader.load_model("meshes/floor.obj")

def load_shader(name:str):
    #load fragment shader source
    with open(f"./shaders/{name}.frag", "r") as f:
        frag_src = f.read()
    #load vertex shader source
    with open(f"./shaders/{name}.vert", "r") as f:
        vert_src = f.read()
    shader = compileProgram(compileShader(vert_src, GL_VERTEX_SHADER), compileShader(frag_src, GL_FRAGMENT_SHADER))
    return shader
        
outline_shader = load_shader("solid_color")
texture_shader = load_shader("texture")


# VAO and VBO
VAO = glGenVertexArrays(3)
VBO = glGenBuffers(3)
EBO = glGenBuffers(1)

# cube VAO
glBindVertexArray(VAO[0])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# monkey VAO
glBindVertexArray(VAO[1])
# monkey Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)

# monkey vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))
# monkey textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))
# monkey normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# floor VAO
glBindVertexArray(VAO[2])
# floor Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)

# floor vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))
# floor textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


textures = glGenTextures(4)
load_texture_pygame("meshes/cube.jpg", textures[0])
load_texture_pygame("meshes/monkey.jpg", textures[1])
load_texture_pygame("meshes/floor.jpg", textures[2])
load_texture_pygame("textures/grass.png", textures[3], TEXTURE_WRAP.GL_CLAMP_TO_EDGE)

#settings
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# glEnable(GL_STENCIL_TEST);
# glStencilFunc(GL_NOTEQUAL, 1, 0xFF);
# glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

glEnable(GL_BLEND);  
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  

glEnable(GL_CULL_FACE)

###


glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

cube_pos =  glm.translate(glm.mat4(1.0), [6, 4, 0])
monkey_pos =  glm.translate(glm.mat4(1.0), [-4, 4, -4])
floor_pos =  glm.translate(glm.mat4(1.0), [0, 0, 0])
grass_pos = glm.translate(glm.rotate(glm.scale(glm.mat4(1.0), glm.vec3(0.2,0.2,0.2)), glm.radians(90), [1,0,0] ), [0,15,-30]) 

projection = glm.perspective(45, 1280 / 720, 0.1, 100)


glUseProgram(texture_shader)
model_loc = glGetUniformLocation(texture_shader, "model")
proj_loc = glGetUniformLocation(texture_shader, "projection")
view_loc = glGetUniformLocation(texture_shader, "view")
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))

glUseProgram(outline_shader)
omodel_loc = glGetUniformLocation(outline_shader, "model")
oproj_loc = glGetUniformLocation(outline_shader, "projection")
oview_loc = glGetUniformLocation(outline_shader, "view")
glUniformMatrix4fv(oproj_loc, 1, GL_FALSE, glm.value_ptr(projection))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
            projection = glm.perspective(45, event.w / event.h, 0.1, 100)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        cam.process_keyboard("LEFT", 0.08)
    if keys_pressed[pygame.K_d]:
        cam.process_keyboard("RIGHT", 0.08)
    if keys_pressed[pygame.K_w]:
        cam.process_keyboard("FORWARD", 0.08)
    if keys_pressed[pygame.K_s]:
        cam.process_keyboard("BACKWARD", 0.08)


    mouse_pos = pygame.mouse.get_pos()
    mouse_look(mouse_pos[0], mouse_pos[1])

    # to been able to look around 360 degrees, still not perfect
    if mouse_pos[0] <= 0:
        pygame.mouse.set_pos((1279, mouse_pos[1]))
    elif mouse_pos[0] >= 1279:
        pygame.mouse.set_pos((0, mouse_pos[1]))

        
    ct = pygame.time.get_ticks() / 1000

    glClearColor(0, 0.1, 0.1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    view = cam.get_view_matrix()

    glUseProgram(texture_shader)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
    glUseProgram(outline_shader)
    glUniformMatrix4fv(oview_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(oproj_loc, 1, GL_FALSE, glm.value_ptr(projection))


    # ############################## first pass
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);
    glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # we're not using the stencil buffer now
    glEnable(GL_DEPTH_TEST);

    # # draw the monkey
    # glBindVertexArray(VAO[1])
    # glBindTexture(GL_TEXTURE_2D, textures[1])
    # glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_pos)
    # glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))

    # draw the floor
    glUseProgram(texture_shader)
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(floor_pos))
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    
    # # draw the cube
    # glStencilFunc(GL_ALWAYS, 1, 0xFF)
    # glStencilMask(0xFF)
    # glUseProgram(texture_shader)
    # glBindVertexArray(VAO[0])
    # glBindTexture(GL_TEXTURE_2D, textures[0])
    # glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(cube_pos))
    # glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)



    # # draw cube's outline
    # glStencilFunc(GL_NOTEQUAL, 1, 0xFF)
    # glStencilMask(0x00)
    # glDisable(GL_DEPTH_TEST)
    # glUseProgram(outline_shader)
    # scale = 1.5
    # glBindVertexArray(VAO[0])
    # glBindTexture(GL_TEXTURE_2D, textures[0])
    # model = cube_pos
    # # model = glm.translate(model, glm.vec3(-1.0, 0.0, -1.0))
    # model = glm.scale(model, glm.vec3(scale, scale, scale))
    # glUniformMatrix4fv(omodel_loc, 1, GL_FALSE, glm.value_ptr(model))
    # glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, None)


    # glStencilMask(0x00)
    # glStencilFunc(GL_ALWAYS, 0, 0xFF)
    # glEnable(GL_DEPTH_TEST) 
    
    #draw grass
    glUseProgram(texture_shader)
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    for t in range(5):
        grass_pos2 = glm.translate(grass_pos, [0,t*-15,0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(grass_pos2))
        glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))


    #################### second pass
    glBindFramebuffer(GL_FRAMEBUFFER, 0) # back to default
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f)
    glClear(GL_COLOR_BUFFER_BIT)
    
    screenShader.use()
    glBindVertexArray(quadVAO)
    glDisable(GL_DEPTH_TEST)
    glBindTexture(GL_TEXTURE_2D, textureColorbuffer)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    



    pygame.display.flip()

pygame.quit()
