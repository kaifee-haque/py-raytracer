import yaml
import patterns
from config_helpers import *
from bodies import *
from raytracer import *
from matplotlib.pyplot import imsave

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def compute_ray_direction(x, y, camera):
    pixel = np.array([x, y, screen["z"]])
    return unit(pixel - camera.position)

config = load_yaml('scene_config.yaml')
materials = load_yaml('materials.yaml')

# screen setup
width = config['screen']['width']
height = config['screen']['height']

aspect_ratio = width / height
screen = {
    "left": -1,
    "top": 1 / aspect_ratio,
    "right": 1,
    "bottom": -1 / aspect_ratio,
    "z": config['screen']['z']
}

# scene setup
reflection_depth = config['reflection_depth']
camera = Body(config['camera']['position'])
lights = [
    Light(
        position=light['position'],
        color=resolve_color(light['color']),
        intensity=light['intensity']
    )
    for light in config['lights']
]

objects = []
for obj in config['objects']:
    color = resolve_color(obj['color'])
    material = resolve_material(obj['material'])

    pattern = None
    if 'pattern' in obj:
        if obj['pattern']['type'] == 'checkerboard':
            scale = obj['pattern'].get('scale', 5)
            pattern = patterns.Checkerboard(scale=scale)

    if obj['type'] == 'Sphere':
        objects.append(Sphere(obj['position'], obj['radius'], color, material, pattern))

    elif obj['type'] == 'Plane':
        objects.append(
            Plane(
                position=obj['position'],
                distance=obj['distance'],
                color=color,
                material=material,
                pattern=pattern
            )
        )

def reinhard_tone_mapping(color):
    return color / (1 + color)

image = np.zeros((height, width, 3))

for i, y in enumerate(np.linspace(screen["top"], screen["bottom"], height)):
    for j, x in enumerate(np.linspace(screen["left"], screen["right"], width)):
        ray_direction = compute_ray_direction(x, y, camera)
        color = trace_ray(
            origin=camera.position,
            direction=ray_direction,
            reflection_depth=reflection_depth,
            objects=objects,
            lights=lights,
            camera=camera
        )
        image[i, j] = reinhard_tone_mapping(color)

    print(f"Progress: {round((i + 1) * 100 / height)}%")

imsave('output/scene.png', image)
