from bodies import *

# colors
green = Color(ambient = (0, 0.1, 0), diffuse = (0, 0.7, 0), specular = (1, 1, 1))
grey = Color(ambient = (0.1, 0.1, 0.1), diffuse = (0.5, 0.5, 0.5), specular = (1, 1, 1))
purple = Color(ambient = (0.07, 0, 0.1), diffuse = (0.7, 0, 1), specular = (1, 1, 1))
white = Color(ambient = (1, 1, 1), diffuse = (1, 1, 1), specular = (1, 1, 1))
soft_white = Color(ambient = (1, 0.8, 0.8), diffuse = (1, 0.8, 0.8), specular = (1, 1, 1))
cyan = Color(ambient = (0, 1, 1), diffuse = (0, 0.1, 0.1), specular = (1, 1, 1))

# materials
shiny = Material(luster = 100, reflectivity = 0.75)
matte = Material(luster = 50, reflectivity = 0.2)