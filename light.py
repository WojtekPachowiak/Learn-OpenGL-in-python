import glm

class DirLight:
    direction :glm.vec3
    color: glm.vec3

class PointLight :
    position :glm.vec3
    radius: float
    color: glm.vec3