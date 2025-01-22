import numpy as np

def unit(v):
    """
    Computes a vector with length 1 in the direction of v.
    """
    return v / np.linalg.norm(v)

class Body:
    """
    An entity that occupies space in the 3D hyperplane.
    """
    def __init__(self, position):
        self.position = np.array(position)

class Color:
    """
    Color consists of the following components:
        ambient: represents light scattered from reflecting off other surfaces
            - does not depend on direction
        diffuse: represents light reflected directly from a point source
            - depends on the angle between the surface normal and the light source
        specular: represents glare/highlights
            - depends on the half-angle between the surface normal and the camera
    """
    def __init__(self, ambient, diffuse, specular):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

class Material:
    """
    A material consists of the following components:
        luster: a measure of glossiness/shininess
            - higher value -> sharper glare
            - lower value -> softer glare
        reflectivity: self-explanatory
            - the higher the value, the less light is lost on each bounce
    """
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
    """
    The position and orientation of a plane are defined by two components:
        - a normal vector perpendicular to the plane. Here, this is defined
          by the "position" field
        - distance from the origin on the normal
    Planes can optionally implement a checkerboard pattern.
    """
    def __init__(self, position, distance, color, material,
                 checkerboard=False, checker_scale=5):
        super().__init__(position)
        self.distance = distance

        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

        self.luster = material.luster
        self.reflectivity = material.reflectivity

        # checkerboard setup
        self.checkerboard = checkerboard
        self.checker_scale = checker_scale
        if self.checkerboard:
            self._init_axes()

    
    def _init_axes(self):
        """
        Precomputes two orthogonal axes in the plane for the checkerboard pattern.
        """
        normal = unit(self.position)

        # pick an "up" vector not parallel to the plane normal
        # note: this doesn't necessarily have to be [0, 1, 0] or [1, 0, 0].
        #       we just want any vector that's NOT zero or parallel to the normal.
        #       otherwise the cross product would yield zero, which is useless.
        if abs(normal[1]) < 0.999:
            up = np.array([0, 1, 0])
        else:
            up = np.array([1, 0, 0])

        # generate a vector orthogonal to the normal (parallel to the plane) and
        #   orthogonal to "up"
        self.u_axis = unit(np.cross(normal, up))
        # generate a vector orthogonal to the normal (parallel to the plane) and
        #   orthogonal to u
        self.v_axis = np.cross(normal, self.u_axis)

    def normal(self, point=np.array([0, 0, 0])):
        """
        Computes a unit vector orthogonal to the point of intersection.
        Note: for planes, we don't need a specific point here, since
              the normal vector is intrinsic to its associated plane.
        """
        return unit(self.position)
    
    def intersection(self, origin, direction):
        """
        A plane can be represented as p • x = d, where:
            - p is the plane's normal vector
            - x is a point on the plane
            - d is the offset from the origin.
        A ray is parameterized as x(t) = o + td, where:
            - o is the ray's origin
            - d is its direction vector
            - t is a scalar distance along the ray
        In order to get the point of intersection, we substitute the
        ray equation for x and then solve for t.
            - if t is non-zero, the ray intersects the plane!
            - if t is negative, the intersection point is behind the ray's origin. 
            - if t is zero, the ray's origin intersects the plane.
            - if the denominator is zero, the ray is parallel to the plane.
        """
        p = self.position
        num = self.distance - p[0] * origin[0] - p[1] * origin[1] - p[2] * origin[2]
        denom = p[0] * direction[0] + p[1] * direction[1] + p[2] * direction[2]
        t = num / denom
        if t > 0:
            return t
    
    def get_color_at(self, point):
        """
        Returns (ambient, diffuse, specular) at a given intersection point.
            - if checkerboard is false, returns the plane's default color
            - othewise, returns black or white squares
        TODO: Add support for custom colors
        """
        if not self.checkerboard:
            return (self.ambient, self.diffuse, self.specular)

        normal = self.normal()
        offset = np.dot(point, normal) - self.distance
        # correct for the offset introduced in raytracer.py
        #  to avoid shadow acne
        point_on_plane = point - offset * normal

        # get the coordinates of the point on the u-v basis
        u = np.dot(point_on_plane, self.u_axis) * self.checker_scale
        v = np.dot(point_on_plane, self.v_axis) * self.checker_scale

        # alternate colors based on whether the sum of the
        #  coordinates is even/odd
        if int(np.floor(u) + np.floor(v)) % 2 == 0:
            # white square
            return (np.array([1.0, 1.0, 1.0]),
                    np.array([1.0, 1.0, 1.0]),
                    np.array([1.0, 1.0, 1.0]))
        else:
            # black square
            return (np.array([0.0, 0.0, 0.0]),
                    np.array([0.0, 0.0, 0.0]),
                    np.array([1.0, 1.0, 1.0]))

class Sphere(Body):
    """
    The position and size of a sphere are defined by two components:
        - the coordinates of its center point
        - its radius
    """
    def __init__(self, position, radius, color, material):
        super().__init__(position)
        self.radius = radius

        self.ambient = np.array(color.ambient)
        self.diffuse = np.array(color.diffuse)
        self.specular = np.array(color.specular)

        self.luster = material.luster
        self.reflectivity = material.reflectivity

    def normal(self, point):
        """
        Computes a unit vector orthogonal to the point of intersection.
        Note: for spheres, this is simply the difference between the
              contact point and the center point.
        """
        return unit(point - self.position)
    
    def intersection(self, origin, direction):
        """
        A sphere is defined by the equation ||x - p||^2 = r^2, where:
            - x is a point on the sphere
            - p is its center point
            - r is its radius.
        Recall that the ray equation is x(t) = o + td.
        Like in the plane case, we substitute this for x and solve for t.
            - if the discriminant is positive, we have two intersection points
              (the ray passes through the sphere)
            - if it's zero, there's just one - the ray is tangent to (grazes)
              the sphere
            - if it's negative, there is no intersection.
        In the first case, we simply return the minimum of the intersection distances
        (no need to reflect off the exit point).
        """
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
        Returns (ambient, diffuse, specular) at a given intersection point
        TODO: add support for textures.
        """
        return (self.ambient, self.diffuse, self.specular)
