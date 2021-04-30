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
    def __init__(self, position, color):
        super().__init__(position)
        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

class Plane(Body):
    def __init__(self, position, color, material):
        super().__init__(position)
        self.height = self.position[1]

        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

        self.luster = material.luster
        self.reflectivity = material.reflectivity

    def normal(self, point):
        return np.array([0, 1, 0])
    
    def intersection(self, origin, direction):
        dot_product = abs(np.dot( direction, np.array([0, 1, 0]) ))
        if dot_product != 0:
            print(origin + (self.height - origin[1]) / direction[1] * direction)
            return (self.height - origin[1]) / direction[1]

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