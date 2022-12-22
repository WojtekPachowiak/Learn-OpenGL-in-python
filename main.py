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
from imgui.integrations.pygame import PygameRenderer
import imgui

timer = 0
fps=0 

def main():
    # CAMERA settings
    cam = Camera()


    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)
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

    rock = Model("meshes/rock/rock.obj")
    planet = Model("meshes/planet/planet.obj")





    #cubemap
    # faces_paths = [
    #     "textures/skybox/right.jpg",
    #     "textures/skybox/left.jpg",
    #     "textures/skybox/top.jpg",
    #     "textures/skybox/bottom.jpg",
    #     "textures/skybox/front.jpg",
    #     "textures/skybox/back.jpg"
    # ]
    # cubemap_tex = load_cubemap(faces_paths);  

    # #framebuffer
    # framebuffer, frametexture = generate_framebuffer()

    def global_settings():
        gl.glEnable(gl.GL_DEPTH_TEST)
        # glDepthFunc(GL_LESS)

        # glEnable(GL_STENCIL_TEST);
        # glStencilFunc(GL_NOTEQUAL, 1, 0xFF);
        # glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

        # glEnable(GL_BLEND);  
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  

        # glEnable(GL_CULL_FACE)
    global_settings()


    projection = glm.perspective(45, WIDTH / HEIGHT, NEAR_CLIP, FAR_CLIP)


    amount = 100000
    modelMatrices = glm.array.zeros(amount, glm.mat4)
    import time
    glm.setSeed(int(time.time())) # initialize random seed	
    radius = 150.0
    offset = 25.0
    for i in range(amount):
        model = glm.mat4(1.0)
        # 1. translation: displace along circle with 'radius' in range [-offset, offset]
        angle = float(i) / amount * 360.0
        displacement = glm.linearRand(-offset, offset)
        x = glm.sin(angle) * radius + displacement
        displacement = glm.linearRand(-offset, offset)
        y = displacement * 0.4 # keep height of asteroid field smaller compared to width of x and z
        displacement = glm.linearRand(-offset, offset)
        z = glm.cos(angle) * radius + displacement
        model = glm.translate(model, glm.vec3(x, y, z))

        # 2. scale: Scale between 0.05 and 0.25
        scale = glm.linearRand(0.05, 0.25)
        model = glm.scale(model, glm.vec3(scale))

        # 3. rotation: add random rotation around a (semi)randomly picked rotation axis vector
        rotAngle = glm.linearRand(0, 360)
        model = glm.rotate(model, rotAngle, glm.vec3(0.4, 0.6, 0.8))

        # 4. now add to list of matrices
        modelMatrices[i] = model

    buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, modelMatrices.nbytes, modelMatrices.ptr, gl.GL_STATIC_DRAW)

    for i in range(len(rock.meshes)):
            VAO = rock.meshes[i].VAO
            gl.glBindVertexArray(VAO)
            # set attribute pointers for matrix (4 times vec4)
            gl.glEnableVertexAttribArray(3)
            gl.glVertexAttribPointer(3, 4, gl.GL_FLOAT, gl.GL_FALSE, glm.sizeof(glm.mat4), None)
            gl.glEnableVertexAttribArray(4)
            gl.glVertexAttribPointer(4, 4, gl.GL_FLOAT, gl.GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p(glm.sizeof(glm.vec4)))
            gl.glEnableVertexAttribArray(5)
            gl.glVertexAttribPointer(5, 4, gl.GL_FLOAT, gl.GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p(2 * glm.sizeof(glm.vec4)))
            gl.glEnableVertexAttribArray(6)
            gl.glVertexAttribPointer(6, 4, gl.GL_FLOAT, gl.GL_FALSE, glm.sizeof(glm.mat4), ctypes.c_void_p(3 * glm.sizeof(glm.vec4)))

            gl.glVertexAttribDivisor(3, 1)
            gl.glVertexAttribDivisor(4, 1)
            gl.glVertexAttribDivisor(5, 1)
            gl.glVertexAttribDivisor(6, 1)

            gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER,0)



    clock = pygame.time.Clock()

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
        asteroids_shader.set_mat4fv("view", glm.value_ptr(view))
        asteroids_shader.set_mat4fv("projection", glm.value_ptr(projection))
        planet_shader.use()
        planet_shader.set_mat4fv("view", glm.value_ptr(view))
        planet_shader.set_mat4fv("projection", glm.value_ptr(projection))
        gl.glUseProgram(0)

        imgui_logic()

        
        


        gl.glClearColor(0.0, 0.0, .0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # draw planet
        model = glm.mat4(1.0);
        model = glm.translate(model, glm.vec3(0.0, -3.0, 0.0));
        model = glm.scale(model, glm.vec3(4.0, 4.0, 4.0));
        planet_shader.use()
        planet_shader.set_mat4fv("model", glm.value_ptr(model));
        planet.Draw(planet_shader);

        # draw meteorites
        asteroids_shader.use()
        asteroids_shader.set_int("texture_diffuse1", 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, rock.textures_loaded[0].id) # note: we also made the textures_loaded vector public (instead of private) from the model class.
        for i in range(len(rock.meshes)):
            gl.glBindVertexArray(rock.meshes[i].VAO)
            gl.glDrawElementsInstanced(gl.GL_TRIANGLES, len(rock.meshes[i].indices), gl.GL_UNSIGNED_INT, None, amount)
            gl.glBindVertexArray(0)
        gl.glUseProgram(0)

        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()