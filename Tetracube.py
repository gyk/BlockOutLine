import copy
from MathHelper import *

class Tetracube:
    """
    Represents a tetracube.
    
    Each tetracube has an implicit center at (0, 0, 0) and a list of coordinates (3-tuples) 
    which represent the blocks relative to the center. 
    """
    def __init__(self, coords=[], color_index=1):
        self.coords = coords
        self.color_index = color_index
        z_range = [co[2] for co in coords]
        self.three_d = max(z_range) - min(z_range)
        
    def copy(self):
        return copy.deepcopy(self)
    
    def rotate(self, axis):
        """@axis: a 3-tuple unit vector representing the axis of rotation,
        eg. (0, 0, 1) means rotate counter-clockwise around positive Z-axis."""
        # TODO: need improvement
        self.coords = [(0, 0, 0)] + [rotate(block, axis) for block in self.coords[1:]]
        

import random
        
class CubeBank:
    """
    A collection of all types of tetracubes. 
    """
    Z   = Tetracube([(0, 0, 0), (0, -1, 0), (1, 0, 0), (1, 1, 0)], 1)

    # I   = Tetracube([(0, 0, 0), (0, -1, 0), (0, 1, 0), (0, 2, 0)], 2)
    # In 3X3 pit, we use the following definition instead
    I   = Tetracube([(0, 0, 0), (1, 0, 0), (-1, 0, 0)], 2)

    T   = Tetracube([(0, 0, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0)], 3)
    L   = Tetracube([(0, 0, 0), (-1, 0, 0), (1, 0, 0), (1, 1, 0)], 4)
    O   = Tetracube([(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)], 5)
    L0  = Tetracube([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)], 6)
    LX  = Tetracube([(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 0, 1)], 7)
    LY  = Tetracube([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1)], 8)

    C   = Tetracube([(0, 0, 0), (1, 0, 0), (0, 1, 0)], 9)
    
    bank = [Z, I, T, L, O, L0, LX, LY, C]
    
    @classmethod
    def get_random(cls):
        return random.choice(CubeBank.bank)
        
        
if __name__ == '__main__':
    tc = CubeBank.get_random()
    print tc.coords
    tc.rotate(POSITIVE_Z)
    print tc.coords, tc.color_index
    
    
        
        
