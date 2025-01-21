import yaml
from bodies import Color, Material

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
    
materials_config = load_yaml('materials.yaml')
COLORS = materials_config['colors']
MATERIALS = materials_config['materials']

def resolve_color(color_definition):
    """Resolve color definition, either alias or explicit."""
    if isinstance(color_definition, str):
        return Color(**COLORS[color_definition])
    elif isinstance(color_definition, dict):
        return Color(**color_definition)
    else:
        raise ValueError("Invalid color definition.")

def resolve_material(material_definition):
    """Resolve material definition, either alias or explicit."""
    if isinstance(material_definition, str):
        return Material(**MATERIALS[material_definition])
    elif isinstance(material_definition, dict):
        return Material(**material_definition)
    else:
        raise ValueError("Invalid material definition.")