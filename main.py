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
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 16) #antialiasing

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

    # rock = Model("meshes/rock/rock.obj")
    planet = Model("meshes/planet/planet.obj")
    cube = Model("meshes\cube.obj")
    monkey = Model("meshes/monkey.obj")





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
        solid_color_shader.use()
        solid_color_shader.set_mat4fv("view", glm.value_ptr(view))
        solid_color_shader.set_mat4fv("projection", glm.value_ptr(projection))
        gl.glUseProgram(0)
        
        imgui_logic()

        
        


        gl.glClearColor(0.0, 0.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)



        #draw cube
        model = glm.mat4(1.0);
        model = glm.translate(model, glm.vec3(0.0, -3.0, 0.0));
        model = glm.scale(model, glm.vec3(4.0, 4.0, 4.0));
        solid_color_shader.use()
        solid_color_shader.set_mat4fv("model", glm.value_ptr(model));
        monkey.Draw(solid_color_shader);
        gl.glUseProgram(0)

    



        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()