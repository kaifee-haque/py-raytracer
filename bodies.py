import numpy as np

# computes a vector with length 1 in the direction of v
def unit(v):
    return v / np.linalg.norm(v)

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
    def __init__(self, position, color, intensity=1.0):
        super().__init__(position)
        self.intensity = intensity
        self.ambient = np.array(color.ambient) * intensity
        self.diffuse = np.array(color.diffuse) * intensity
        self.specular = np.array(color.specular) * intensity

class Plane(Body):
    def __init__(self, position, distance, color, material):
        super().__init__(position)
        self.distance = distance

        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

        self.luster = material.luster
        self.reflectivity = material.reflectivity

    def normal(self, point):
        return unit(self.position)
    
    def intersection(self, origin, direction):
        p = self.position
        num = self.distance - p[0] * origin[0] - p[1] * origin[1] - p[2] * origin[2]
        denom = p[0] * direction[0] + p[1] * direction[1] + p[2] * direction[2]
        t = num / denom
        if t > 0:
            return t

class Sphere(Body):
    def __init__(self, position, radius, color, material):
        super().__init__(position)
        self.radius = radius

        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

        self.luster = material.luster
        self.reflectivity = material.reflectivity

    def normal(self, point):
        return unit(point - self.position)
    
    def intersection(self, origin, direction):
        b = 2 * np.dot(direction, origin - self.position)
        c = np.linalg.norm(origin - self.position) ** 2 - self.radius ** 2
        discriminant = b ** 2 - 4 * c

        if discriminant > 0:
            t1 = (-b - np.sqrt(discriminant)) / 2
            t2 = (-b + np.sqrt(discriminant)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)