import numpy as np
from abc import ABC, abstractmethod
from bodies import unit

class Pattern(ABC):
    """
    Patterns must implement get_color_at() to determine their appearance.
    """
    @abstractmethod
    def get_color_at(self, shape, point):
        pass

class CheckerboardPattern(Pattern):
    def __init__(self, scale=5):
        self.scale = scale

    def get_color_at(self, shape, point):
        """
        Implements checkerboard logic, but defers UV-mapping to shape. 
            - shape.uv_map(point) returns (u, v) in some 2D coordinate system.
        """
        (u, v) = shape.uv_map(point, self.scale)

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
