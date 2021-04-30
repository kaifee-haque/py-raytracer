from bodies import *
from materials import *
from raytracer import *
from matplotlib.pyplot import imsave

# screen setup
width, height = 150, 100
aspect_ratio = width / height
screen = {
    "left": -1,
    "top": 1 / aspect_ratio,
    "right": 1,
    "bottom": -1 / aspect_ratio,
    "z": 3
}

# scene setup
camera = Body([0, 0, screen["z"] + 1])
light = Light((-4, 10, 3), soft_white)
objects = [
    Sphere((-0.5, 0.1, 0.5), 0.17, purple, shiny),
    Sphere((0, 0.01, -1), 0.75, cyan, shiny),
    Sphere((0.3, 0.01, 0.35), 0.2, green, shiny),
    Sphere((-0.1, 0.03, 0.45), 0.07, white, matte),
    Plane((0.3, -1, -0.2), orange, shiny)
]
reflection_depth = 3

image = np.zeros((height, width, 3))

for i, y in enumerate(np.linspace(screen["top"], screen["bottom"], height)):
    for j, x in enumerate(np.linspace(screen["left"], screen["right"], width)):
        color = raytrace(x, y, camera, screen["z"], reflection_depth, objects, light)
        image[i, j] = np.clip(color, 0, 1)

    print(f"Progress: {round(i * 100 / height)}%")

imsave('scene.png', image)