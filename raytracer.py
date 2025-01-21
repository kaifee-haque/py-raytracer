import numpy as np

ALPHA_AIR = 0.00001
ATTENUATION_DISTANCE_SCALING = 25

# computes a vector with length 1 in the direction of v
def unit(v):
    return v / np.linalg.norm(v)

# computes the reflection of v across the surface perpendicular to n
def reflected(v, n):
    return v - 2 * np.dot(v, n) * n

# returns the nearest object hit by the ray and its distance from the camera
def nearest_intersection(objects, origin, direction):
    distances = [o.intersection(origin, direction) for o in objects]
    minimum_distance = 1_000_000
    nearest_object = None
    for i, distance in enumerate(distances):
        if distance and distance < minimum_distance:
            minimum_distance = distance
            nearest_object = objects[i]
    return nearest_object, minimum_distance

def raytrace(x, y, camera, screen, reflection_depth, objects, light):
    pixel = np.array([x, y, screen])
    origin = camera.position
    direction = unit(pixel - origin)
    color = np.zeros((3))

    reflection_weight = 1

    for k in range(reflection_depth):
        nearest_object, minimum_distance = nearest_intersection(objects, origin, direction)
        if nearest_object is None:
            break

        intersection = origin + minimum_distance * direction
        surface_normal = nearest_object.normal(intersection)
        corrected_point = intersection + 0.00001 * surface_normal

        point_to_light = unit(light.position - corrected_point)

        _, minimum_distance = nearest_intersection(objects, corrected_point, point_to_light)
        point_to_light_distance = np.linalg.norm(light.position - intersection)
        light_blocked = minimum_distance < point_to_light_distance

        if light_blocked:
            break

        scaled_light_distance = point_to_light_distance / ATTENUATION_DISTANCE_SCALING

        attenuation = np.exp(-ALPHA_AIR * scaled_light_distance) / (4 * np.pi * scaled_light_distance**2)

        partial_color = np.zeros((3))

        nearest_obj_ambient, nearest_obj_diffuse, nearest_obj_specular = nearest_object.get_color_at(intersection)

        partial_color += nearest_obj_ambient * light.ambient

        partial_color += nearest_obj_diffuse * light.diffuse * np.dot(point_to_light, surface_normal)

        intersection_to_camera = unit(camera.position - intersection)
        half_angle_vector = unit(point_to_light + intersection_to_camera)
        partial_color += nearest_obj_specular * light.specular * np.dot(surface_normal, half_angle_vector) ** (nearest_object.luster)

        color += reflection_weight * partial_color * attenuation
        reflection_weight *= nearest_object.reflectivity

        origin = corrected_point
        direction = reflected(direction, surface_normal)
    return color