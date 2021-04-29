import numpy as np

class Body:
    def __init__(self, position):
        self.position = np.array(position)

class Color:
    def __init__(self, ambient, diffuse, specular):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

class Material:
    def __init__(self, luster, reflectivity):
        self.luster = luster
        self.reflectivity = reflectivity

class Light(Body):
    def __init__(self, position, color):
        super(position)
        self.ambient = color.ambient
        self.diffuse = color.diffuse
        self.specular = color.specular

class Sphere(Body):
    def __init__(self, position, radius, color, material):
        super(position)
        self.radius = radius

        self.ambient = color.ambient
        self.diffuse = color.diffuse
        self.specular = color.specular

        self.luster = material.luster
        self.reflectivity = material.reflectivity
    
    def intersect(self, origin, direction):
        b = 2 * np.dot(direction, origin - self.radius)
        c = np.linalg.norm(origin - self.radius) ** 2 - radius ** 2
        discriminant = b ** 2 - 4 * c

        if discriminant > 0:
            t1 = (-b - np.sqrt(discriminant)) / 2
            t2 = (-b + np.sqrt(discriminant)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)