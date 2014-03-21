from collections import defaultdict
from copy import deepcopy
from PyQt4 import QtCore

from MathHelper import *
from Tetracube import CubeBank
from Pit import Pit

NONE = 0
SOLID = 1
BLOCKED = 2
DASHED = 3

class OrthoProjection(QtCore.QObject):
    """
    Orthographic projection of the pit
    """
    
    def __init__(self, pit):
        super(OrthoProjection, self).__init__()
        self.pit = pit
        self.action_dict = {}
        for dir_index, direct in zip((1, -1), '+-'):
            for axis_index, axis in enumerate('XYZ'):
                self.action_dict[direct + axis] = self.at_axis(axis_index, dir_index)

        self.pit.modified.connect(self.regenerate)

    def at_axis(self, axis_index, dir_index):
        """
        axis_index: 0, 1, 2
        dir_index: -1, 1
        """
        
        largest_indices = [
            self.pit.width - 1, self.pit.height - 1, self.pit.depth - 1
        ]

        def start_init(coord):
            if dir_index == 1:
                coord[axis_index] = 0
            else:
                coord[axis_index] = largest_indices[axis_index]
            return coord

        def step_action(coord):
            coord[axis_index] += dir_index
            return coord

        def stop_crierion(coord):
            if dir_index == 1:
                return coord[axis_index] == largest_indices[axis_index]
            else:
                return coord[axis_index] == 0

        from collections import namedtuple
        CoordFunc = namedtuple('CoordFunc', 'start_init step_action stop_crierion');
        return CoordFunc(start_init, step_action, stop_crierion)
 
    def make_ortho(self, direct):
        "direct: '[+-][XY]'"
        far_to_near = self.action_dict[direct]
        if direct == '+X':
            horizontal = self.pit.height
            vertical = self.pit.depth
            left_to_right = self.action_dict['+Y']
            lower_to_up = self.action_dict['+Z']
        elif direct == '-X':
            horizontal = self.pit.height
            vertical = self.pit.depth
            left_to_right = self.action_dict['-Y']
            lower_to_up = self.action_dict['+Z']
        elif direct == '+Y':
            horizontal = self.pit.width
            vertical = self.pit.depth
            left_to_right = self.action_dict['-X']
            lower_to_up = self.action_dict['+Z']
        elif direct == '-Y':
            horizontal = self.pit.width
            vertical = self.pit.depth
            left_to_right = self.action_dict['+X']
            lower_to_up = self.action_dict['+Z']

        layers = self.pit.layers
        new_array_factory = lambda n_r, n_c: \
            [[0] * n_c for i in range(n_r)]

        from operator import getitem
        def get_block(coord):
            return reduce(getitem, coord[::-1], self.pit.layers)

        def state_transfer(old_state, new_state):
            assert new_state != DASHED
            if new_state == NONE:
                return old_state
            if new_state == SOLID:
                return SOLID
            if new_state == BLOCKED:
                if old_state == SOLID or old_state == DASHED:
                    return DASHED
                else:
                    return NONE

        def overlay(old_section, new_section):
            n_rows = len(old_section)
            n_cols = len(old_section[0])
            for i_r in range(n_rows):
                for i_c in range(n_cols):
                    if state_transfer(
                        old_section[i_r][i_c], new_section[i_r][i_c]) == None:
                        print "Holy shit!", old_section[i_r][i_c], new_section[i_r][i_c]
                    new_section[i_r][i_c] = state_transfer(
                        old_section[i_r][i_c], new_section[i_r][i_c])
            return new_section

        coord = ORIGIN
        coord = far_to_near.start_init(coord)

        self.faces = new_array_factory(vertical, horizontal)
        self.beams = new_array_factory(vertical + 1, horizontal)
        self.columns = new_array_factory(vertical, horizontal + 1)

        # farthest to nearest
        while True:
            i_c = 0
            
            self.old_beams = deepcopy(self.beams)
            self.old_columns = deepcopy(self.columns)
            self.beams = new_array_factory(vertical + 1, horizontal)
            self.columns = new_array_factory(vertical, horizontal + 1)
            coord = left_to_right.start_init(coord)

            # leftmost to rightmost
            while True:
                i_r = 0
                coord = lower_to_up.start_init(coord)

                # lowerest to highest
                while True:
                    block = get_block(coord)

                    if block:
                        # beams
                        self.beams[i_r][i_c] += SOLID
                        self.beams[i_r+1][i_c] += SOLID
                        
                        # columns
                        self.columns[i_r][i_c] += SOLID
                        self.columns[i_r][i_c+1] += SOLID
                        
                        # faces
                        self.faces[i_r][i_c] = block

                    if lower_to_up.stop_crierion(coord):
                        break
                    lower_to_up.step_action(coord)
                    i_r += 1

                if left_to_right.stop_crierion(coord):
                    break
                left_to_right.step_action(coord)
                i_c += 1

            self.beams = overlay(self.old_beams, self.beams)
            self.columns = overlay(self.old_columns, self.columns)

            if far_to_near.stop_crierion(coord):
                break
            far_to_near.step_action(coord)

    @QtCore.pyqtSlot()
    def regenerate(self):
        with self.pit.with_active_cube() as _pit:
            self.beam_dict = {}
            self.column_dict = {}
            self.face_dict = {}
            for ortho_type in ['+X', '-X', '+Y', '-Y']:
                self.make_ortho(ortho_type)
                self.beam_dict[ortho_type] = self.beams
                self.column_dict[ortho_type] = self.columns
                self.face_dict[ortho_type] = self.faces
            

class AsciiPrinter:
    H_GRID = '-'
    H_DASH = '.'
    H_SOLID = '*'
    
    V_GRID = '|'
    V_DASH = '.'
    V_SOLID = '*'
                       
    beam_ascii = defaultdict(lambda: AsciiPrinter.H_GRID)
    colomn_ascii = defaultdict(lambda: AsciiPrinter.V_GRID)
    beam_ascii.update({
        NONE    :  H_GRID,
        DASHED  :  H_DASH,
        SOLID   :  H_SOLID,
    })
    colomn_ascii.update({
        NONE    :  V_GRID,
        DASHED  :  V_DASH,
        SOLID   :  V_SOLID,
    })
    
    @classmethod
    def print_all(cls, ortho_prj):
        CROSS_POINT = '+'
        V_GRID = AsciiPrinter.V_GRID
        beam_, col_ = cls.beam_ascii, cls.colomn_ascii

        for b in ortho_prj.beams[-1]:
            print CROSS_POINT, beam_[b],
        print CROSS_POINT

        for (beams, columns, faces) in zip(
            ortho_prj.beams[-2::-1], 
            ortho_prj.columns[::-1], 
            ortho_prj.faces[::-1]):

            for c, f in zip(columns[:-1], faces):
                print col_[c], f,
            print col_[columns[-1]]

            for b in beams:
                print CROSS_POINT, beam_[b],
            print CROSS_POINT
        print
        

if __name__ == '__main__':
    pit = Pit(5, 5, 8)
    ortho_prj = OrthoProjection(pit)
    assert(pit.spawn_cube())
    pit.move_down()
    ortho_prj.make_ortho('+X')
    AsciiPrinter.print_all(ortho_prj)

    with pit.with_active_cube() as _pit:
        ortho_prj.make_ortho('+X')
        AsciiPrinter.print_all(ortho_prj)
    
    # print pit.cur_cube.coords
    # pit.rotate_cube((0, 1, 0))
    # print pit.cur_cube.coords
    

    
