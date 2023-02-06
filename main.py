from __future__ import absolute_import
import numpy as np
import glm
from camera import Camera
from constants import WIDTH, HEIGHT, NEAR_CLIP, FAR_CLIP
from shader import Shader   
from model import Model
import ctypes
import sys
import pygame
import OpenGL.GL as gl
from OpenGL.GL import * 
from imgui.integrations.pygame import PygameRenderer
import imgui
from TextureLoader import load_texture_pygame, generate_framebuffer
from geo_primitives import ScreenQuad

timer = 0
fps=0 

planeVAO, planeVBO = 0,0
def main():
    # CAMERA settings
    cam = Camera()


    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)
    # pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 16) # MSAA antialiasing

    pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE) # |pygame.FULLSCREEN

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    #imgui setup
    imgui.create_context()
    impl = PygameRenderer()
    io = imgui.get_io()
    io.display_size = (WIDTH, HEIGHT)


  
    asteroids_shader = Shader("asteroids")
    planet_shader = Shader("planet")
    solid_color_shader = Shader("solid_color")
    framebuffer_base_shader = Shader("framebuffer_base")
    blinn_phong_shader = Shader("blinn_phong")

    simpleDepthShader  = Shader("simple_depth")
    debugDepthQuad  = Shader("depth_debug_quad")


    # rock = Model("meshes/rock/rock.obj")
    planet = Model("meshes/planet/planet.obj")
    cube = Model("meshes\cube.obj")
    monkey = Model("meshes/monkey.obj")
    floor = Model("meshes/floor.obj")
    screenquad = ScreenQuad()


    woodTexture  = load_texture_pygame("./meshes/floor.jpg")



    def global_settings():
        gl.glEnable(gl.GL_DEPTH_TEST)
        # glDepthFunc(GL_LESS)
        # glEnable(GL_FRAMEBUFFER_SRGB)

        # glEnable(GL_STENCIL_TEST);
        # glStencilFunc(GL_NOTEQUAL, 1, 0xFF);
        # glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  

        # glEnable(GL_CULL_FACE)
    global_settings()


    projection = glm.perspective(45, WIDTH / HEIGHT, NEAR_CLIP, FAR_CLIP)


    clock = pygame.time.Clock()

    planeVertices = glm.array(glm.float32,
        # positions            # normals         # texcoords
         25.0, -0.5,  25.0,  0.0, 1.0, 0.0,  25.0,  0.0,
        -25.0, -0.5,  25.0,  0.0, 1.0, 0.0,   0.0,  0.0,
        -25.0, -0.5, -25.0,  0.0, 1.0, 0.0,   0.0, 25.0,

         25.0, -0.5,  25.0,  0.0, 1.0, 0.0,  25.0,  0.0,
        -25.0, -0.5, -25.0,  0.0, 1.0, 0.0,   0.0, 25.0,
         25.0, -0.5, -25.0,  0.0, 1.0, 0.0,  25.0, 25.0)

    # plane VAO
    planeVAO = glGenVertexArrays(1)
    planeVBO = glGenBuffers(1)
    glBindVertexArray(planeVAO)
    glBindBuffer(GL_ARRAY_BUFFER, planeVBO)
    glBufferData(GL_ARRAY_BUFFER, planeVertices.nbytes, planeVertices.ptr, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(3 * glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(6 * glm.sizeof(glm.float32)))
    glBindVertexArray(0)
    





    SHADOW_WIDTH = 1024
    SHADOW_HEIGHT = 1024
    depthMapFBO = glGenFramebuffers(1)
    # create depth texture
    depthMap = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depthMap)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # attach depth texture as FBO's depth buffer
    glBindFramebuffer(GL_FRAMEBUFFER, depthMapFBO)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depthMap, 0)
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    

    debugDepthQuad.use()
    debugDepthQuad.set_int("depthMap", 0)

    # lighting info
    # -------------
    lightPos = glm.vec3(-2.0, 4.0, -1.0)


    def imgui_logic():
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        
        # imgui.show_test_window()

        clock.tick()
        global timer, fps
        timer += clock.get_time()
        if (timer > 2000):
            timer=0
            fps = int(clock.get_fps())
        flags = (
            imgui.WINDOW_NO_SCROLLBAR | 
            imgui.WINDOW_NO_DECORATION | 
            imgui.WINDOW_ALWAYS_AUTO_RESIZE | 
            imgui.WINDOW_NO_FOCUS_ON_APPEARING |
            imgui.WINDOW_NO_SAVED_SETTINGS |
            imgui.WINDOW_NO_NAV
        )
        imgui.begin("FPS tracker", True,flags)
        imgui.text(f"FPS: {fps}")
        imgui.end()



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.VIDEORESIZE:
                gl.glViewport(0, 0, event.w, event.h)
                projection = glm.perspective(glm.radians(45), event.w / event.h, NEAR_CLIP, FAR_CLIP)
            impl.process_event(event)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            cam.process_keyboard("LEFT", 0.08)
        if keys_pressed[pygame.K_d]:
            cam.process_keyboard("RIGHT", 0.08)
        if keys_pressed[pygame.K_w]:
            cam.process_keyboard("FORWARD", 0.08)
        if keys_pressed[pygame.K_s]:
            cam.process_keyboard("BACKWARD", 0.08)

        imgui.new_frame()

        xoffset, yoffset = pygame.mouse.get_rel()
        cam.process_mouse_movement(xoffset, -yoffset)

        
                

        
        view = cam.get_view_matrix()
        #view and projection setting
        asteroids_shader.use()
        asteroids_shader.set_mat4fv("view", view)
        asteroids_shader.set_mat4fv("projection", projection)
        planet_shader.use()
        planet_shader.set_mat4fv("view", view)
        planet_shader.set_mat4fv("projection", projection)
        solid_color_shader.use()
        solid_color_shader.set_mat4fv("view", view)
        solid_color_shader.set_mat4fv("projection", projection)
        blinn_phong_shader.use()
        blinn_phong_shader.set_mat4fv("view", view)
        blinn_phong_shader.set_mat4fv("projection", projection)

        gl.glUseProgram(0)
        
        imgui_logic()

        
        


        gl.glClearColor(0.0, 0.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


        
        near_plane, far_plane = 1.0,  7.5
        
        lightProjection = glm.ortho(-10.0, 10.0, -10.0, 10.0, near_plane, far_plane);
        lightView = glm.lookAt(lightPos, glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0));
        lightSpaceMatrix = lightProjection * lightView;
        # render scene from light's point of view
        simpleDepthShader.use();
        simpleDepthShader.set_mat4fv("lightSpaceMatrix", lightSpaceMatrix);

        glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, depthMapFBO)
        glClear(GL_DEPTH_BUFFER_BIT)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, woodTexture)
        renderScene(simpleDepthShader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # reset viewport
        glViewport(0, 0, WIDTH, HEIGHT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # render Depth map to quad for visual debugging
        # ---------------------------------------------
        debugDepthQuad.use()
        debugDepthQuad.set_float("near_plane", near_plane)
        debugDepthQuad.set_float("far_plane", far_plane)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, depthMap)
        renderQuad()

    


        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()

    pygame.quit()

# renders the 3D scene
# --------------------
def renderScene(shader : Shader) -> None:
    global planeVAO

    # floor
    model = glm.mat4(1.0)
    shader.set_mat4fv("model", model)
    glBindVertexArray(planeVAO)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    # cubes
    model = glm.mat4(1.0)
    model = glm.translate(model, glm.vec3(0.0, 1.5, 0.0))
    model = glm.scale(model, glm.vec3(0.5))
    shader.set_mat4fv("model", model)
    renderCube()
    model = glm.mat4(1.0)
    model = glm.translate(model, glm.vec3(2.0, 0.0, 1.0))
    model = glm.scale(model, glm.vec3(0.5))
    shader.set_mat4fv("model", model)
    renderCube()
    model = glm.mat4(1.0)
    model = glm.translate(model, glm.vec3(-1.0, 0.0, 2.0))
    model = glm.rotate(model, glm.radians(60.0), glm.normalize(glm.vec3(1.0, 0.0, 1.0)))
    model = glm.scale(model, glm.vec3(0.25))
    shader.set_mat4fv("model", model)
    renderCube()

# renderCube() renders a 1x1 3D cube in NDC.
# -------------------------------------------------
cubeVAO = 0
cubeVBO = 0
def renderCube() -> None:
    global cubeVAO, cubeVBO

    # initialize (if necessary)
    if (cubeVAO == 0):

        vertices = glm.array(glm.float32,
            # back face
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 0.0, # bottom-left
             1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 1.0, # top-right
             1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 0.0, # bottom-right         
             1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 1.0, 1.0, # top-right
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 0.0, # bottom-left
            -1.0,  1.0, -1.0,  0.0,  0.0, -1.0, 0.0, 1.0, # top-left
            # front face
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 0.0, # bottom-left
             1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 0.0, # bottom-right
             1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 1.0, # top-right
             1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 1.0, 1.0, # top-right
            -1.0,  1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 1.0, # top-left
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, 0.0, 0.0, # bottom-left
            # left face
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, 1.0, 0.0, # top-right
            -1.0,  1.0, -1.0, -1.0,  0.0,  0.0, 1.0, 1.0, # top-left
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, 0.0, 1.0, # bottom-left
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, 0.0, 1.0, # bottom-left
            -1.0, -1.0,  1.0, -1.0,  0.0,  0.0, 0.0, 0.0, # bottom-right
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, 1.0, 0.0, # top-right
            # right face
             1.0,  1.0,  1.0,  1.0,  0.0,  0.0, 1.0, 0.0, # top-left
             1.0, -1.0, -1.0,  1.0,  0.0,  0.0, 0.0, 1.0, # bottom-right
             1.0,  1.0, -1.0,  1.0,  0.0,  0.0, 1.0, 1.0, # top-right         
             1.0, -1.0, -1.0,  1.0,  0.0,  0.0, 0.0, 1.0, # bottom-right
             1.0,  1.0,  1.0,  1.0,  0.0,  0.0, 1.0, 0.0, # top-left
             1.0, -1.0,  1.0,  1.0,  0.0,  0.0, 0.0, 0.0, # bottom-left     
            # bottom face
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 0.0, 1.0, # top-right
             1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 1.0, 1.0, # top-left
             1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 1.0, 0.0, # bottom-left
             1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 1.0, 0.0, # bottom-left
            -1.0, -1.0,  1.0,  0.0, -1.0,  0.0, 0.0, 0.0, # bottom-right
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, 0.0, 1.0, # top-right
            # top face
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 0.0, 1.0, # top-left
             1.0,  1.0 , 1.0,  0.0,  1.0,  0.0, 1.0, 0.0, # bottom-right
             1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 1.0, 1.0, # top-right     
             1.0,  1.0,  1.0,  0.0,  1.0,  0.0, 1.0, 0.0, # bottom-right
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, 0.0, 1.0, # top-left
            -1.0,  1.0,  1.0,  0.0,  1.0,  0.0, 0.0, 0.0)  # bottom-left        

        cubeVAO = glGenVertexArrays(1)
        cubeVBO = glGenBuffers(1)
        # fill buffer
        glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)
        # link vertex attributes
        glBindVertexArray(cubeVAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(3 * glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * glm.sizeof(glm.float32), ctypes.c_void_p(6 * glm.sizeof(glm.float32)))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # render Cube
    glBindVertexArray(cubeVAO)
    glDrawArrays(GL_TRIANGLES, 0, 36)
    glBindVertexArray(0)

# renderQuad() renders a 1x1 XY quad in NDC
# -----------------------------------------
quadVAO = 0
def renderQuad() -> None:
    global quadVAO, quadVBO

    if (quadVAO == 0):

        quadVertices = glm.array(glm.float32,
            # positions        # texture Coords
            -1.0,  1.0, 0.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0, 0.0,
             1.0,  1.0, 0.0, 1.0, 1.0,
             1.0, -1.0, 0.0, 1.0, 0.0)

        # setup plane VAO
        quadVAO = glGenVertexArrays(1)
        quadVBO = glGenBuffers(1)
        glBindVertexArray(quadVAO)
        glBindBuffer(GL_ARRAY_BUFFER, quadVBO)
        glBufferData(GL_ARRAY_BUFFER, quadVertices.nbytes, quadVertices.ptr, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * glm.sizeof(glm.float32), ctypes.c_void_p(3 * glm.sizeof(glm.float32)))

    glBindVertexArray(quadVAO)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glBindVertexArray(0)


if __name__ == "__main__":
    main()



