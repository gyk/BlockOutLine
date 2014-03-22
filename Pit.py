from contextlib import contextmanager
from PyQt4 import QtCore

from Tetracube import CubeBank
from MathHelper import *

class Pit(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    def __init__(self, width, height, depth):
        "width: X-axis, height: Y-axis, depth: Z-axis"
        super(Pit, self).__init__()
        
        self.width, self.height, self.depth = width, height, depth
        self.empty()
        
        self.cur_cube = None
        self.cur_pos = None

    def empty(self):
        width, height, depth = self.width, self.height, self.depth
        # Is copy.deepcopy() faster?
        self.empty_layer_factory = lambda: [a[:] for a in [[0] * width] * height]
        self.layers = [self.empty_layer_factory() for d in range(depth)]
        self.modified.emit()
        
    def spawn_cube(self):
        """ 
        Creates a new tetracube in the pit.
        
        Returns False if there's no room for the new tetracube
        (this basically means game over), and True if 
        everything is OK and the tetracube has been created.
        """
        tc = CubeBank.get_random()
        half_width, half_height = self.width / 2, self.height / 2
        pos = [half_width, half_height, self.depth - int(tc.three_d) - 1]
        if self.is_conflict(tc, pos):
            return False
        self.cur_cube = tc
        self.cur_pos = pos
        self.modified.emit()
        return True
        
    def is_conflict(self, tetracube, pos):
        for x, y, z in tetracube.coords:
            x_, y_, z_ = x+pos[0], y+pos[1], z+pos[2]
            if 0 <= x_ < self.width and \
                0 <= y_ < self.height and \
                0 <= z_ < self.depth and \
                not self.layers[z_][y_][x_]:
                continue
            else:
                return True
        return False

    def get_offset(self, tetracube, pos):
        """
        After adding `offset` to `cur_pos`, the cube will be moved inside 
        the pit (if possible).
        """
        offset = [0, 0, 0]
        sizes = [self.width, self.height, self.depth]            

        for coord in tetracube.coords:
            coord = add(coord, pos)
            for i in range(3):
                off = 0
                if coord[i] < 0:
                    off = -coord[i]
                elif coord[i] >= sizes[i]:
                    off = -(coord[i] - sizes[i] + 1)

                if abs(off) > abs(offset[i]):
                    offset[i] = off

        return offset
                
    def move_cube(self, offset) :
        """ 
        Moves the current tetracube by the given offset. The
        offset is a tuple (X, Y, Z).

        Returns True if the figure was successfully moved,
        and False if the move introduces a conflict.
        """
        if not self.cur_pos:
            return False
        
        new_pos = add(self.cur_pos, offset)
        if self.is_conflict(self.cur_cube, new_pos):
            return False
        self.cur_pos = new_pos
        self.modified.emit()
        return True
        
    def move_down(self):
        return self.move_cube(NEGATIVE_Z)
    
    def rotate_cube(self, axis):
        tmp_cube = self.cur_cube.copy()
        tmp_cube.rotate(axis)
        if self.is_conflict(tmp_cube, self.cur_pos):
            offset = self.get_offset(tmp_cube, self.cur_pos)
            if offset == [0, 0, 0] or \
                self.is_conflict(tmp_cube, add(self.cur_pos, offset)):
                return False
            else:
                self.cur_pos = add(self.cur_pos, offset)

        self.cur_cube = tmp_cube
        self.modified.emit()
        return True
    
    def can_move_down(self):
        down_pos = add(self.cur_pos, NEGATIVE_Z)
        return not self.is_conflict(self.cur_cube, down_pos)
    
    def drop_cube(self):
        while(self.can_move_down()):
            self.move_down()
    
    @staticmethod
    def _is_layer_incomplete(layer):
        for row in layer:
            for blk in row:
                if not blk:
                    return True
        return False
        
    def remove_completed_layers(self):
        complete = [not Pit._is_layer_incomplete(lay) for lay in self.layers]
        self.layers = [lay for (lay, flag_complete) in 
            zip(self.layers, complete) if not flag_complete]
        self.layers += [self.empty_layer_factory() for i in range(sum(complete))]
        self.modified.emit()
        return complete
    
    @contextmanager
    def with_active_cube(self):
        self.put_active_cube()
        yield self
        self.remove_active_cube()

    def _manipulate_active_cube(self, add_cube):
        "Puts the active cube into the pit, or removes it from the pit."
        cur_cube = self.cur_cube
        if not cur_cube:
            return
        for x, y, z in cur_cube.coords:
            x_, y_, z_ = x+self.cur_pos[0], y+self.cur_pos[1], z+self.cur_pos[2]
            self.layers[z_][y_][x_] = cur_cube.color_index if add_cube else 0

    def put_active_cube(self):
        self._manipulate_active_cube(True)

    def remove_active_cube(self):
        self._manipulate_active_cube(False)

    def add_active_cube(self):
        self.put_active_cube()

        # Sets current cube to None so the added cube will not be taken away
        # when calling `remove_active_cube`
        self.cur_cube = None
