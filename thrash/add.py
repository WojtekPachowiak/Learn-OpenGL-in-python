    # def add_cube():
    #     # vertices = np.array([
    #     #     # positions          # normals
    #     #     -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
    #     #      0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
    #     #      0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
    #     #      0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
    #     #     -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
    #     #     -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,

    #     #     -0.5, -0.5,  0.5,  0.0,  0.0, 1.0,
    #     #      0.5, -0.5,  0.5,  0.0,  0.0, 1.0,
    #     #      0.5,  0.5,  0.5,  0.0,  0.0, 1.0,
    #     #      0.5,  0.5,  0.5,  0.0,  0.0, 1.0,
    #     #     -0.5,  0.5,  0.5,  0.0,  0.0, 1.0,
    #     #     -0.5, -0.5,  0.5,  0.0,  0.0, 1.0,

    #     #     -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
    #     #     -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
    #     #     -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
    #     #     -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
    #     #     -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,
    #     #     -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,

    #     #      0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
    #     #      0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
    #     #      0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
    #     #      0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
    #     #      0.5, -0.5,  0.5,  1.0,  0.0,  0.0,
    #     #      0.5,  0.5,  0.5,  1.0,  0.0,  0.0,

    #     #     -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
    #     #      0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
    #     #      0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
    #     #      0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
    #     #     -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
    #     #     -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,

    #     #     -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
    #     #      0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
    #     #      0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
    #     #      0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
    #     #     -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
    #     #     -0.5,  0.5, -0.5,  0.0,  1.0,  0.0
    #     # ], dtype=np.float32)
    #     # vao = glGenVertexArrays(1);
    #     # vbo = glGenBuffers(1);
    #     # glBindVertexArray(vao);
    #     # glBindBuffer(GL_ARRAY_BUFFER, vbo);
    #     # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW);
    #     # glEnableVertexAttribArray(0);
    #     # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0));
    #     # glEnableVertexAttribArray(1);
    #     # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12));
    #     # return vao
    #     cube_indices, cube_buffer = ObjLoader.load_model("meshes/cube.obj", False)
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     ebo = glGenBuffers(1)
    #     glBindVertexArray(vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)
    #     glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    #     glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)
    #     # vertices
    #     glEnableVertexAttribArray(0)
    #     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))
    #     # textures
    #     glEnableVertexAttribArray(1)
    #     glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))
    #     # normals
    #     glEnableVertexAttribArray(2)
    #     glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
    #     glBindVertexArray(0)
    #     return vao, cube_indices

    # def add_plane():
    #     plane_indices, plane_buffer = ObjLoader.load_model("meshes/floor.obj")
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     ebo = glGenBuffers(1)
    #     glBindVertexArray(vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     glBufferData(GL_ARRAY_BUFFER, plane_buffer.nbytes, plane_buffer, GL_STATIC_DRAW)
    #     glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    #     glBufferData(GL_ELEMENT_ARRAY_BUFFER, plane_indices.nbytes, plane_indices, GL_STATIC_DRAW)
    #     # vertices
    #     glEnableVertexAttribArray(0)
    #     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, plane_buffer.itemsize * 8, ctypes.c_void_p(0))
    #     # textures
    #     glEnableVertexAttribArray(1)
    #     glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, plane_buffer.itemsize * 8, ctypes.c_void_p(12))
    #     # normals
    #     glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, plane_buffer.itemsize * 8, ctypes.c_void_p(20))
    #     glEnableVertexAttribArray(2)
    #     glBindVertexArray(0)
    #     return vao, plane_indices


    # def add_screenquad():
    #     '''add a quad that fills the entire screen'''
    #     #buffer in Normalized Device Coordinates
    #     vertices = np.array([ 
    #         #positions   #texCoords
    #         -1.0,  1.0,  0.0, 1.0,
    #         -1.0, -1.0,  0.0, 0.0,
    #         1.0, -1.0,  1.0, 0.0,

    #         -1.0,  1.0,  0.0, 1.0,
    #         1.0, -1.0,  1.0, 0.0,
    #         1.0,  1.0,  1.0, 1.0
    #     ],dtype=np.float32)
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     glBindVertexArray(vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    #     glEnableVertexAttribArray(0);
    #     glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0));
    #     glEnableVertexAttribArray(1);
    #     glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(8));
    #     glBindVertexArray(0)
    #     return vao

    # def add_skybox():
    #     vertices = np.array([
    #             # positions          
    #             -1.0,  1.0, -1.0,
    #             -1.0, -1.0, -   1.0,
    #             1.0, -1.0, -1.0,
    #             1.0, -1.0, -1.0,
    #             1.0,  1.0, -1.0,
    #             -1.0,  1.0, -1.0,

    #             -1.0, -1.0,  1.0,
    #             -1.0, -1.0, -1.0,
    #             -1.0,  1.0, -1.0,
    #             -1.0,  1.0, -1.0,
    #             -1.0,  1.0,  1.0,
    #             -1.0, -1.0,  1.0,

    #             1.0, -1.0, -1.0,
    #             1.0, -1.0,  1.0,
    #             1.0,  1.0,  1.0,
    #             1.0,  1.0,  1.0,
    #             1.0,  1.0, -1.0,
    #             1.0, -1.0, -1.0,

    #             -1.0, -1.0,  1.0,
    #             -1.0,  1.0,  1.0,
    #             1.0,  1.0,  1.0,
    #             1.0,  1.0,  1.0,
    #             1.0, -1.0,  1.0,
    #             -1.0, -1.0,  1.0,

    #             -1.0,  1.0, -1.0,
    #             1.0,  1.0, -1.0,
    #             1.0,  1.0,  1.0,
    #             1.0,  1.0,  1.0,
    #             -1.0,  1.0,  1.0,
    #             -1.0,  1.0, -1.0,

    #             -1.0, -1.0, -1.0,
    #             -1.0, -1.0,  1.0,
    #             1.0, -1.0, -1.0,
    #             1.0, -1.0, -1.0,
    #             -1.0, -1.0,  1.0,
    #             1.0, -1.0,  1.0
    #     ],dtype=np.float32)
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     glBindVertexArray(vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    #     glEnableVertexAttribArray(0);
    #     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0));
    #     glBindVertexArray(0)
    #     return vao

    # def add_four_points():
    #     vertices = np.array([
    #     -0.5,  0.5, 1.0, 0.0, 0.0, # top-left
    #     0.5,  0.5, 0.0, 1.0, 0.0, # top-right
    #     0.5, -0.5, 0.0, 0.0, 1.0, # bottom-right
    #     -0.5, -0.5, 1.0, 1.0, 0.0  # bottom-left
    #     ], dtype=np.float32)
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     glBindVertexArray(vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    #     glEnableVertexAttribArray(0);
    #     glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0));
    #     glEnableVertexAttribArray(1);
    #     glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(8));
    #     glBindVertexArray(0)
    #     return vao


    # def add_monkey():
    #     monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/monkey.obj")
    #     # monkey VAO
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     glBindVertexArray(vao) 
    #     # monkey Vertex Buffer Object
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
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
    #     return vao, monkey_indices

    # def add_instanced_quad():
    #     vertices = np.array([
    #     # positions     # colors
    #     -0.05,  0.05,  1.0, 0.0, 0.0,
    #     0.05, -0.05,  0.0, 1.0, 0.0,
    #     -0.05, -0.05,  0.0, 0.0, 1.0,

    #     -0.05,  0.05,  1.0, 0.0, 0.0,
    #     0.05, -0.05,  0.0, 1.0, 0.0,   
    #     0.05,  0.05,  0.0, 1.0, 1.0		    		
    #     ],dtype=np.float32)
    #     vao = glGenVertexArrays(1)
    #     vbo = glGenBuffers(1)
    #     glBindVertexArray(vao)
    #     glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #     glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    #     glEnableVertexAttribArray(0);
    #     glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0));
    #     glEnableVertexAttribArray(1);
    #     glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(8));


    #     #preparing instanced_shader
    #     x = np.linspace(-0.9, 0.9, 10)
    #     translations = np.dstack(np.meshgrid(x,x)).reshape(-1,2).astype(np.float32)

    #     instanceVBO = glGenBuffers(1);
    #     glBindBuffer(GL_ARRAY_BUFFER, instanceVBO);
    #     glBufferData(GL_ARRAY_BUFFER, translations.nbytes, translations, GL_STATIC_DRAW);
    #     glBindBuffer(GL_ARRAY_BUFFER, 0);

    #     glEnableVertexAttribArray(2);
    #     glBindBuffer(GL_ARRAY_BUFFER, instanceVBO);
    #     glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 2 * translations.itemsize, ctypes.c_void_p(0));
    #     glBindBuffer(GL_ARRAY_BUFFER, 0);	
    #     glVertexAttribDivisor(2, 1);  
    #     glBindVertexArray(0)

    #     return vao