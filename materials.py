from bodies import *

# colors
green = Color(ambient = (0, 0.1, 0), diffuse = (0, 0.7, 0), specular = (1, 1, 1))
orange = Color(ambient = (0.1, 0.05, 0.03), diffuse = (1, 0.5, 0.3), specular = (1, 1, 1))
purple = Color(ambient = (0.07, 0, 0.1), diffuse = (0.7, 0, 1), specular = (1, 1, 1))
white = Color(ambient = (1, 1, 1), diffuse = (1, 1, 1), specular = (1, 1, 1))
cyan = Color(ambient = (0, 1, 1), diffuse = (0, 0.1, 0.1), specular = (1, 1, 1))

# materials
shiny = Material(luster = 100, reflectivity = 0.75)