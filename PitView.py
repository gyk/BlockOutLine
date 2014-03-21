
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from OrthoProjection import *

class PitView(QWidget):
    SINK_WIDTH = 10
    LINE_WIDTH = 3

    def __init__(self, parent, n_rows, n_cols, block_size, ortho_prj, direct):
        super(PitView, self).__init__(parent)

        self.ortho_prj = ortho_prj
        self.direct = direct

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.block_size = block_size

        self.width = block_size * n_cols + PitView.SINK_WIDTH * 2
        self.height = block_size * n_rows + PitView.SINK_WIDTH * 2
        self.setMinimumSize(QSize(self.width, self.height))

        self.solid_pen = QPen(QBrush(QColor("#222")), PitView.LINE_WIDTH)

        self.dashed_pen = QPen(QBrush(QColor("#666")), PitView.LINE_WIDTH)
        self.dashed_pen.setStyle(Qt.CustomDashLine)
        self.dashed_pen.setDashPattern([0.6, 3, 0.6, 0])

        self.dotted_pen = QPen(QBrush(QColor('#ddd')), PitView.LINE_WIDTH)
        self.dotted_pen.setStyle(Qt.CustomDashLine)
        self.dotted_pen.setDashPattern([0.25, 4])

        # self.color_map = [
        #     None,  # 1-based
        #     QColor(122, 197, 205),
        #     QColor(0, 205, 0),
        #     QColor(238, 238, 0),
        #     QColor(238, 118, 33),
        #     QColor(238, 44, 44),
        #     QColor(0, 0, 225),
        #     QColor(148, 0, 211),
        #     QColor(100, 149, 237),
        # ]

        self.color_map = [
            None,  # 1-based
            QColor(79, 129, 189),
            QColor(192, 80, 77),
            QColor(155, 187, 89),
            QColor(128, 100, 162),
            QColor(75, 172, 198),
            QColor(247, 150, 70),
            QColor(146, 208, 80),
            QColor(255, 192, 0),
            QColor(175, 33, 121),
        ]

        self.bgcolor = QColor(234, 234, 244)

        self.pen_map = {
            NONE : self.dotted_pen,
            SOLID : self.solid_pen,
            DASHED : self.dashed_pen,
        }

    def draw(self, painter, beams, columns, faces):
        
        painter.fillRect(0, 0, self.width, self.height, 
            QBrush(self.bgcolor, Qt.SolidPattern))
        
        self.draw_grids(painter)
        self.draw_all_blocks(painter, faces)
        self.draw_edges(painter, beams, columns)
        

    def draw_grids(self, painter):
        painter.setPen(self.dotted_pen)
        for r in range(self.n_rows + 1):
            from_x = PitView.SINK_WIDTH
            to_x = from_x + self.block_size * self.n_cols
            y = PitView.SINK_WIDTH + self.block_size * r
            painter.drawLine(from_x, y, to_x, y)

        for c in range(self.n_cols + 1):
            x = PitView.SINK_WIDTH + self.block_size * c
            from_y = PitView.SINK_WIDTH
            to_y = from_y + self.block_size * self.n_rows
            painter.drawLine(x, from_y, x, to_y)

    def draw_edges(self, painter, beams, columns):
        for edge_type in [DASHED, SOLID]:
            # draws horizontal lines
            for r in range(self.n_rows + 1):
                for c in range(self.n_cols):
                    if beams[r][c] != edge_type:
                        continue

                    painter.setPen(self.pen_map[beams[r][c]])

                    from_x = PitView.SINK_WIDTH + self.block_size * c
                    to_x = from_x + self.block_size
                    y = self.height - (PitView.SINK_WIDTH + self.block_size * r)

                    painter.drawLine(from_x, y, to_x, y)

            # draws vertical lines
            for r in range(self.n_rows):
                for c in range(self.n_cols + 1):
                    if columns[r][c] != edge_type:
                        continue

                    painter.setPen(self.pen_map[columns[r][c]])

                    x = PitView.SINK_WIDTH + self.block_size * c
                    from_y = PitView.SINK_WIDTH + self.block_size * r
                    to_y = from_y + self.block_size
                    from_y =  self.height - from_y
                    to_y =  self.height - to_y

                    painter.drawLine(x, from_y, x, to_y)

    def draw_all_blocks(self, painter, faces):        
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                color = faces[row][col]
                
                if color != 0:
                    self.draw_block(painter, row, col, self.color_map[color])

    def draw_block(self, painter, row, col, color):
        left_upper_x = PitView.SINK_WIDTH + col * self.block_size
        left_upper_y = PitView.SINK_WIDTH + row * self.block_size
        left_upper_y = self.height - left_upper_y - self.block_size

        block_rect = QRect(left_upper_x, left_upper_y,
            self.block_size, self.block_size)
        
        painter.fillRect(block_rect, QBrush(color, Qt.SolidPattern))

    def paintEvent(self, event=None):
        painter = QPainter(self)
        beams = self.ortho_prj.beam_dict[self.direct]
        columns = self.ortho_prj.column_dict[self.direct]
        faces = self.ortho_prj.face_dict[self.direct]
        self.draw(painter, beams, columns, faces)


