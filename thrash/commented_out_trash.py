
# # cube VAO
# glBindVertexArray(VAO[0])
# # cube Vertex Buffer Object
# glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
# glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)

# # cube vertices
# glEnableVertexAttribArray(0)
# glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))
# # cube textures
# glEnableVertexAttribArray(1)
# glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))
# # cube normals
# glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
# glEnableVertexAttribArray(2)

# # monkey VAO
# glBindVertexArray(VAO[1])
# # monkey Vertex Buffer Object
# glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
# glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)

# # monkey vertices
# glEnableVertexAttribArray(0)
# glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))
# # monkey textures
# glEnableVertexAttribArray(1)
# glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))
# # monkey normals
# glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
# glEnableVertexAttribArray(2)

# # floor VAO
# glBindVertexArray(VAO[2])
# # floor Vertex Buffer Object
# glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
# glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)

# # floor vertices
# glEnableVertexAttribArray(0)
# glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))
# # floor textures
# glEnableVertexAttribArray(1)
# glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))
# # floor normals
# glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
# glEnableVertexAttribArray(2)

#=================================================

        # #draw instanced quads
        # instanced_shader.use()
        # glBindVertexArray(instanced_vao);
        # glDrawArraysInstanced(GL_TRIANGLES, 0, 6, 100);  
        

        

        # draw the cube
        # reflective_shader.use()
        # glBindVertexArray(cube_vao)
        # # glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_tex);
        # reflective_shader.set_mat4fv("model", glm.value_ptr(cube_pos))
        # reflective_shader.set_vec3("cameraPos", glm.value_ptr(cam.camera_pos))
        # glDrawArrays(GL_TRIANGLES, 0, 36);

        # #draw four points
        # houses_shader.use()
        # glBindVertexArray(four_points_vao)
        # glDrawArrays(GL_POINTS, 0, 4)
        
        # draw the monkey
        # texture_shader.use()
        # glBindVertexArray(monkey_vao)
        # glBindTexture(GL_TEXTURE_2D, textures[1])
        # texture_shader.set_mat4fv("model", glm.value_ptr(monkey_pos))
        # glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices)) 

        # # draw the monkey normals
        # vis_normal_shader.use()
        # glBindVertexArray(monkey_vao)
        # glBindTexture(GL_TEXTURE_2D, textures[1])
        # vis_normal_shader.set_mat4fv("model", glm.value_ptr(monkey_pos))
        # glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))  

        


        #draw skybox
        # glDepthFunc(GL_LEQUAL);  # change depth function so depth test passes when values are equal to depth buffer's content
        # skybox_shader.use();
        # skybox_view = glm.mat4(glm.mat3(cam.get_view_matrix()));  
        # skybox_shader.set_mat4fv("view", glm.value_ptr(skybox_view))
        # glBindVertexArray(skybox_vao);
        # glBindTexture(GL_TEXTURE_CUBE_MAP, cubemap_tex);
        # glDrawArrays(GL_TRIANGLES, 0, 36);
        # glBindVertexArray(0);
        # glDepthFunc(GL_LESS); # set depth function back to default


        # #draw screenquad
        # framebuffer_base_shader.use()
        # frame_model =  glm.translate(glm.scale(glm.mat4(1.0), glm.vec3(0.4,0.4,0)), [0,2,0])

        # framebuffer_base_shader.set_mat4fv("model",glm.value_ptr(frame_model) )
        # glBindVertexArray(screenquad_vao)
        # glBindTexture(GL_TEXTURE_2D, frametexture)
        # glDrawArrays(GL_TRIANGLES, 0, 6)


#=========================

  # outline_shader = Shader("solid_color")
    # texture_shader = Shader("texture")
    # framebuffer_base_shader = Shader("framebuffer_base")
    # skybox_shader = Shader("skybox_cubemap")
    # reflective_shader = Shader("reflective_refractive")
    # houses_shader = Shader("houses")
    # explode_shader = Shader("explode")
    # vis_normal_shader = Shader("visualize_normals")
    # instanced_shader = Shader("instanced")

#==========================
#  texture_shader.use()
#         texture_shader.set_mat4fv("view", glm.value_ptr(view))
#         texture_shader.set_mat4fv("projection", glm.value_ptr(projection))
#         outline_shader.use()
#         outline_shader.set_mat4fv("view", glm.value_ptr(view))
#         outline_shader.set_mat4fv("projection", glm.value_ptr(projection))
#         # skybox_shader.use()
#         # skybox_shader.set_mat4fv("projection", glm.value_ptr(projection))
#         # reflective_shader.use()
#         # reflective_shader.set_mat4fv("view", glm.value_ptr(view))
#         # reflective_shader.set_mat4fv("projection", glm.value_ptr(projection))
#         # explode_shader.use()
#         # explode_shader.set_mat4fv("view", glm.value_ptr(view))
#         # explode_shader.set_mat4fv("projection", glm.value_ptr(projection))
#         # vis_normal_shader.use()
#         # vis_normal_shader.set_mat4fv("view", glm.value_ptr(view))
#         # vis_normal_shader.set_mat4fv("projection", glm.value_ptr(projection))