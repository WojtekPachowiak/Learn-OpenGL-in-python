from OpenGL.GL import glBindTexture, glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR,\
    glTexImage2D, GL_RGBA, GL_UNSIGNED_BYTE, GL_CLAMP_TO_EDGE
from constants import WIDTH,HEIGHT

from OpenGL.GL import *

from PIL import Image
from enum import Enum

import pygame as pg

# # for use with GLFW
# def load_texture(path, texture):
#     glBindTexture(GL_TEXTURE_2D, texture)
    
#     # Set the texture wrapping parameters
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#     # Set texture filtering parameters
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#     # load image
#     image = Image.open(path)
#     image = image.transpose(Image.FLIP_TOP_BOTTOM)
#     img_data = image.convert("RGBA").tobytes()
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
#     return texture


class TEXTURE_WRAP(Enum):
    GL_CLAMP_TO_EDGE = GL_CLAMP_TO_EDGE
    GL_REPEAT = GL_REPEAT

# for use with pygame
def load_texture_pygame(path, param: TEXTURE_WRAP = TEXTURE_WRAP.GL_REPEAT):
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, param.value)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, param.value)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = pg.image.load(path)
    image = pg.transform.flip(image, False, True)
    image_width, image_height = image.get_rect().size
    img_data = pg.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_SRGB_ALPHA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return tex

def generate_framebuffer(width=WIDTH, height=HEIGHT, attachement= GL_COLOR_ATTACHMENT0,texture_wrap_param=GL_REPEAT, texture_min_mag_filter_param=GL_NEAREST): 
    
    #generate texture
    tex = glGenTextures(1);
    glBindTexture(GL_TEXTURE_2D, tex);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, texture_min_mag_filter_param );
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, texture_min_mag_filter_param);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, texture_wrap_param)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, texture_wrap_param)
    glBindTexture(GL_TEXTURE_2D, 0);

    #attach it to currently bound framebuffer object
    framebuffer = glGenFramebuffers(1);
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);   
    glFramebufferTexture2D(GL_FRAMEBUFFER, attachement, GL_TEXTURE_2D, tex, 0);

    # rbo = glGenRenderbuffers(1);
    # glBindRenderbuffer(GL_RENDERBUFFER, rbo); 
    # glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height);  
    # glBindRenderbuffer(GL_RENDERBUFFER, 0);

    # glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo);

    glDrawBuffer(GL_NONE);
    glReadBuffer(GL_NONE);

    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        print("ERROR::FRAMEBUFFER:: Framebuffer is not complete!") 
    glBindFramebuffer(GL_FRAMEBUFFER, 0);

    return framebuffer, tex



def load_cubemap(faces_paths: list[str]):
    texture_id = glGenTextures(1);
    glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id);

    for i in range(len(faces_paths)):
        image = pg.image.load(faces_paths[i])
        # image = pg.transform.flip(image, False, True)
        width, height = image.get_rect().size
        img_data = pg.image.tostring(image, "RGB")
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);

    return texture_id;

