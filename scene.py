import yaml
from config_helpers import *
from bodies import *
from raytracer import *
from matplotlib.pyplot import imsave

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

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
    if obj['type'] == 'Sphere':
        objects.append(Sphere(obj['position'], obj['radius'], color, material))
    elif obj['type'] == 'Plane':
        objects.append(Plane(obj['position'], obj['distance'], color, material))

def reinhard_tone_mapping(color):
    return color / (1 + color)

image = np.zeros((height, width, 3))

for i, y in enumerate(np.linspace(screen["top"], screen["bottom"], height)):
    for j, x in enumerate(np.linspace(screen["left"], screen["right"], width)):
        color = np.zeros((3))
        for light in lights:
            color += raytrace(x, y, camera, screen["z"], reflection_depth, objects, light)
        image[i, j] = reinhard_tone_mapping(color)

    print(f"Progress: {round(i * 100 / height)}%")

imsave('output/scene.png', image)
