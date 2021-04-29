from bodies import *

width, height = 640, 480
aspect_ratio = width / height
screen = [-1, 1 / aspect_ratio, 1, -1 / aspect_ratio]
image = np.zeros((height, width, 3))

camera = Body([0, 0, 1])
light = Body([2, 2, -2])
