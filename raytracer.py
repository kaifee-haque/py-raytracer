import numpy as np

ALPHA_AIR = 0.00001
ATTENUATION_DISTANCE_SCALING = 25

def unit(v):
    """
    Computes a vector with length 1 in the direction of v.
    """
    return v / np.linalg.norm(v)

def reflected(v, n):
    """
    Computes the reflection of v across the surface perpendicular to n
    """
    return v - 2 * np.dot(v, n) * n

def nearest_intersection(objects, origin, direction):
    """
    Returns the nearest object hit by the ray, and its distance from the
    ray's origin.
    If there are no intersections, we return (None, +infinity)
    """
    # get the distances from the ray's origin to each object
    distances = [o.intersection(origin, direction) for o in objects]

    minimum_distance = float("inf")
    nearest_object = None

    for i, distance in enumerate(distances):
        if distance and distance < minimum_distance:
            minimum_distance = distance
            nearest_object = objects[i]

    return nearest_object, minimum_distance

def trace_ray(origin, direction, reflection_depth, objects, lights, camera):
    """
    Casts a ray from the camera through a given pixel, bouncing a
    predefined number of times, considering all lights in the scene.
    """
    color = np.zeros((3))
    reflection_weight = 1

    for k in range(reflection_depth):
        nearest_object, minimum_distance = nearest_intersection(objects, origin, direction)
        if nearest_object is None: # TODO: add support for background colors
            break

        intersection = origin + minimum_distance * direction
        surface_normal = nearest_object.normal(intersection)
        # offset just above the surface so we don't end up with shadow acne
        corrected_point = intersection + 0.00001 * surface_normal

        partial_color = np.zeros((3))

        for light in lights:
            intersection_to_light = unit(light.position - corrected_point)
            intersection_to_light_distance = np.linalg.norm(light.position - intersection)

            # shadow check
            _obstruction_obj, obstruction_distance = nearest_intersection(objects, corrected_point, intersection_to_light)
            if obstruction_distance < intersection_to_light_distance:
                # light is blocked - skip its contribution in the current bounce
                continue

            # light decreases in power according to:
            #   - the square inverse law
            #   - scattering due to the medium (usually air)
            scaled_light_distance = intersection_to_light_distance / ATTENUATION_DISTANCE_SCALING
            attenuation = np.exp(-ALPHA_AIR * scaled_light_distance) / (4 * np.pi * scaled_light_distance**2)

            # add color components
            nearest_obj_ambient, nearest_obj_diffuse, nearest_obj_specular = nearest_object.get_color_at(intersection)

            partial_color += nearest_obj_ambient * light.ambient
            # diffuse depends on angle between light source and object
            partial_color += nearest_obj_diffuse * light.diffuse * np.dot(intersection_to_light, surface_normal)

            # ambient depends on half-angle between camera and light source
            intersection_to_camera = unit(camera.position - intersection)
            half_angle_vector = unit(intersection_to_light + intersection_to_camera)
            partial_color += nearest_obj_specular * light.specular * np.dot(surface_normal, half_angle_vector) ** (nearest_object.luster)

            color += reflection_weight * partial_color * attenuation

        reflection_weight *= nearest_object.reflectivity
        origin = corrected_point
        direction = reflected(direction, surface_normal)

    return color
