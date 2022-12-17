
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