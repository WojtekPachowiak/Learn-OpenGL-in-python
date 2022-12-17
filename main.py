import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from TextureLoader import load_texture_pygame, TEXTURE_WRAP, generate_framebuffer
from ObjLoader import ObjLoader
import glm
from camera import Camera
from constants import WIDTH, HEIGHT
import numpy as np
from shader import Shader

# CAMERA settings
cam = Camera()

lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True


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



outline_shader = Shader("solid_color")
texture_shader = Shader("texture")
framebuffer_base_shader = Shader("framebuffer_base")


def add_cube():
    cube_indices, cube_buffer = ObjLoader.load_model("meshes/cube.obj", False)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)
    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))
    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))
    # normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)
    return vao, cube_indices

def add_plane():
    plane_indices, plane_buffer = ObjLoader.load_model("meshes/floor.obj")
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, plane_buffer.nbytes, plane_buffer, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, plane_indices.nbytes, plane_indices, GL_STATIC_DRAW)
    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, plane_buffer.itemsize * 8, ctypes.c_void_p(0))
    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, plane_buffer.itemsize * 8, ctypes.c_void_p(12))
    # normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, plane_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)
    return vao, plane_indices


def add_screenquad():
    '''add a quad that fills the entire screen'''
    #buffer in Normalized Device Coordinates
    vertices = np.array([ 
        #positions   #texCoords
        -1.0,  1.0,  0.0, 1.0,
        -1.0, -1.0,  0.0, 0.0,
         1.0, -1.0,  1.0, 0.0,

        -1.0,  1.0,  0.0, 1.0,
         1.0, -1.0,  1.0, 0.0,
         1.0,  1.0,  1.0, 1.0
    ],dtype=np.float32)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0));
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(8));
    glBindVertexArray(0)
    return vao

# def add_monkey():
#     monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/monkey.obj")
#     # monkey VAO
#     glBindVertexArray(VAO[1])
#     # monkey Vertex Buffer Object
#     glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
#     glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)

#     # monkey vertices
#     glEnableVertexAttribArray(0)
#     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))
#     # monkey textures
#     glEnableVertexAttribArray(1)
#     glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))
#     # monkey normals
#     glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
#     glEnableVertexAttribArray(2)


floor_vao, floor_indices = add_plane()
screenquad_vao = add_screenquad()


textures = glGenTextures(5)
load_texture_pygame("meshes/cube.jpg", textures[0])
load_texture_pygame("meshes/monkey.jpg", textures[1])
load_texture_pygame("meshes/floor.jpg", textures[2])    
load_texture_pygame("textures/grass.png", textures[3], TEXTURE_WRAP.GL_CLAMP_TO_EDGE)

framebuffer, frametexture = generate_framebuffer()

def global_settings():
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # glEnable(GL_STENCIL_TEST);
    # glStencilFunc(GL_NOTEQUAL, 1, 0xFF);
    # glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

    glEnable(GL_BLEND);  
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  

    glEnable(GL_CULL_FACE)

global_settings()


cube_pos =  glm.translate(glm.mat4(1.0), [6, 4, 0])
monkey_pos =  glm.translate(glm.mat4(1.0), [-4, 4, -4])
floor_pos =  glm.translate(glm.mat4(1.0), [0, 0, 0])
grass_pos = glm.translate(glm.rotate(glm.scale(glm.mat4(1.0), glm.vec3(0.2,0.2,0.2)), glm.radians(90), [1,0,0] ), [0,15,-30]) 

projection = glm.perspective(45, WIDTH / HEIGHT, 0.1, 100)



texture_shader.use()
texture_shader.set_mat4fv("projection", glm.value_ptr(projection))
model_loc = glGetUniformLocation(texture_shader.program, "model")
proj_loc = glGetUniformLocation(texture_shader.program, "projection")
view_loc = glGetUniformLocation(texture_shader.program, "view")

outline_shader.use()
outline_shader.set_mat4fv("projection", glm.value_ptr(projection))
omodel_loc = glGetUniformLocation(outline_shader.program, "model")
oproj_loc = glGetUniformLocation(outline_shader.program, "projection")
oview_loc = glGetUniformLocation(outline_shader.program, "view")

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
        pygame.mouse.set_pos((WIDTH-1, mouse_pos[1]))
    elif mouse_pos[0] >= WIDTH-1:
        pygame.mouse.set_pos((0, mouse_pos[1]))

        
    ct = pygame.time.get_ticks() / 1000

    view = cam.get_view_matrix()

    texture_shader.use()
    texture_shader.set_mat4fv("view", glm.value_ptr(view))
    texture_shader.set_mat4fv("projection", glm.value_ptr(projection))

    outline_shader.use()
    outline_shader.set_mat4fv("view", glm.value_ptr(view))
    outline_shader.set_mat4fv("projection", glm.value_ptr(projection))



    # ############################## first pass
    glEnable(GL_DEPTH_TEST); 
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);
    glClearColor(0.1, 0.1, 0.1, 1.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # # draw the monkey
    # glBindVertexArray(VAO[1])
    # glBindTexture(GL_TEXTURE_2D, textures[1])
    # glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_pos)
    # glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))

    # draw the floor
    texture_shader.use()
    glBindVertexArray(floor_vao)
    glBindTexture(GL_TEXTURE_2D, textures[2])
    texture_shader.set_mat4fv("model",glm.value_ptr(floor_pos))
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))
    glBindVertexArray(0);


    
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
    # glUseProgram(outline_shader.program)
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
    
    # #draw grass
    # glUseProgram(texture_shader)
    # glBindVertexArray(VAO[2])
    # glBindTexture(GL_TEXTURE_2D, textures[3])
    # for t in range(5):
    #     grass_pos2 = glm.translate(grass_pos, [0,t*-15,0])
    #     glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(grass_pos2))
    #     glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))


    #################### second pass
    glBindFramebuffer(GL_FRAMEBUFFER, 0) # back to default
    glDisable(GL_DEPTH_TEST)

    glClearColor(1.0, 0.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    framebuffer_base_shader.use()
    glBindVertexArray(screenquad_vao)
    glBindTexture(GL_TEXTURE_2D, frametexture)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    



    pygame.display.flip()

pygame.quit()
