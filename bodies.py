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
    def __init__(self, position, distance, color, material,
                 checkerboard=False, checker_scale=5):
        super().__init__(position)
        self.distance = distance

        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

        self.luster = material.luster
        self.reflectivity = material.reflectivity

        # checkerboard fields
        self.checkerboard = checkerboard
        self.checker_scale = checker_scale

        # precompute two orthogonal axes in the plane for checkerboard pattern
        if self.checkerboard:
            self._init_axes()

    
    def _init_axes(self):
        normal = unit(self.position)

        # pick an "up" vector not parallel to the plane normal
        if abs(normal[1]) < 0.999:
            up = np.array([0, 1, 0])
        else:
            up = np.array([1, 0, 0])

        self.u_axis = unit(np.cross(normal, up))
        self.v_axis = np.cross(normal, self.u_axis)

    def normal(self, point):
        return unit(self.position)
    
    def intersection(self, origin, direction):
        p = self.position
        num = self.distance - p[0] * origin[0] - p[1] * origin[1] - p[2] * origin[2]
        denom = p[0] * direction[0] + p[1] * direction[1] + p[2] * direction[2]
        t = num / denom
        if t > 0:
            return t
    
    def get_color_at(self, point):
        """
        returns (ambient, diffuse, specular) at a given intersection point
        if checkerboard is false, returns the plane's default color
        othewise, returns black or white squares
        """
        if not self.checkerboard:
            return (self.ambient, self.diffuse, self.specular)

        normal = unit(self.position)
        offset = np.dot(point, normal) - self.distance
        point_on_plane = point - offset * normal

        u = np.dot(point_on_plane, self.u_axis) * self.checker_scale
        v = np.dot(point_on_plane, self.v_axis) * self.checker_scale

        if int(np.floor(u) + np.floor(v)) % 2 == 0:
            # White square
            return (np.array([1.0, 1.0, 1.0]),
                    np.array([1.0, 1.0, 1.0]),
                    np.array([1.0, 1.0, 1.0]))
        else:
            return (np.array([0.0, 0.0, 0.0]),
                    np.array([0.0, 0.0, 0.0]),
                    np.array([1.0, 1.0, 1.0]))

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

    def get_color_at(self, point):
        """
        for spheres, color doesn't vary by position (no texture)
        returns the same color for any intersection point
        """
        return (self.ambient, self.diffuse, self.specular)