from PyQt4.QtCore import *
from PyQt4.QtGui import *

from OrthoProjection import *
from PitView import PitView

from AboutDialog import AboutDialog

class GameWindow(QMainWindow):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        self.setWindowTitle("BlockOutLine")

        from ImageResource import get_icon_pixmap
        self.setWindowIcon(QIcon(get_icon_pixmap()))
        self.create_menu()

        width, height, depth = 3, 3, 16
        self.pit = Pit(width, height, depth)
        self.ortho_prj = OrthoProjection(self.pit)
        block_size = 38
        
        self.drawable_pit_pos_Y = PitView(self, depth, height, block_size, 
            self.ortho_prj, '+Y')
        self.drawable_pit_neg_X = PitView(self, depth, width, block_size, 
            self.ortho_prj, '-X')
        self.drawable_pit_neg_Y = PitView(self, depth, width, block_size, 
            self.ortho_prj, '-Y')
        self.drawable_pit_pos_X = PitView(self, depth, height, block_size, 
            self.ortho_prj, '+X')

        self.pit.modified.connect(self.drawable_pit_pos_Y.repaint)
        self.pit.modified.connect(self.drawable_pit_neg_X.repaint)
        self.pit.modified.connect(self.drawable_pit_neg_Y.repaint)
        self.pit.modified.connect(self.drawable_pit_pos_X.repaint)

        #
        # Control Panel
        #
        self.control_panel = QFrame(self)
        self.control_panel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.control_panel.setFocusPolicy(Qt.NoFocus)

        self.lcd_score = QLCDNumber(7)
        self.lcd_score.setFixedSize(QSize(180, 55))
        button_size = QSize(180, 45)
        self.restart_button = QPushButton("&New game")
        self.restart_button.setFixedSize(button_size)
        self.restart_button.setFocusPolicy(Qt.NoFocus)
        self.restart_button.clicked.connect(self.on_restart)
        self.quit_button = QPushButton("&Quit")
        self.quit_button.setFixedSize(button_size)
        self.quit_button.setFocusPolicy(Qt.NoFocus)
        self.quit_button.clicked.connect(self.close)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.lcd_score)
        vbox.addSpacing(180)
        vbox.addStretch()
        vbox.addWidget(self.restart_button)
        vbox.addSpacing(30)
        vbox.addWidget(self.quit_button)
        vbox.addStretch()

        self.control_panel.setLayout(vbox)
        self.control_panel.setContentsMargins(18, 18, 18, 18)
        self.control_panel.layout().setContentsMargins(20, 20, 20, 20)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(25, 25, 25, 25)

        spacing = int(block_size * 1.35)
        hbox.addWidget(self.drawable_pit_pos_Y)
        hbox.addSpacing(spacing)
        hbox.addWidget(self.drawable_pit_neg_X)
        hbox.addSpacing(spacing)
        hbox.addWidget(self.drawable_pit_neg_Y)
        hbox.addSpacing(spacing)
        hbox.addWidget(self.drawable_pit_pos_X)

        hbox.addSpacing(35)
        hbox.addWidget(self.control_panel)

        dummy_widget = QWidget()
        dummy_widget.setLayout(hbox)
        dummy_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.setCentralWidget(dummy_widget)

        self.move(15, 15)
        self.restart()
        
    def restart(self):
        self.pit.empty()
        self.set_score(0)
        self.pit.spawn_cube()
        self.active_score = 10

    def set_score(self, score):
        self.score = score
        self.lcd_score.display(score)

    def add_score(self, inc):
        self.set_score(self.score + inc)

    def calc_score(self, complete_indicator):
        # The score is determined by the height of each eliminated layer
        # and the total number of eliminated layers.
        base_score = 100
        n_eliminated = sum(complete_indicator)
        if n_eliminated == 0:
            return 0

        # topmost = 2, bottommost = 1, linear interpolation
        factors = [1.0 * i / (self.pit.depth - 1) + 1.0 
            for (i, flag_complete) in 
                enumerate(complete_indicator) if flag_complete]
        layer_scores = [base_score * f for f in factors]
        return int(sum(layer_scores) * (2.0 ** (n_eliminated - 1)))

    def keyPressEvent(self, event):
        from MathHelper import POSITIVE_X, NEGATIVE_X, \
            POSITIVE_Y, NEGATIVE_Y, POSITIVE_Z, NEGATIVE_Z

        ## Rotation
        ROTATION_KEY_MAP = {
            Qt.Key_Q : POSITIVE_X,
            Qt.Key_A : NEGATIVE_X,
            Qt.Key_W : POSITIVE_Y,
            Qt.Key_S : NEGATIVE_Y,
            Qt.Key_E : POSITIVE_Z,
            Qt.Key_D : NEGATIVE_Z,
        }

        if ROTATION_KEY_MAP.has_key(event.key()):
            success = self.pit.rotate_cube(ROTATION_KEY_MAP[event.key()])
            if success:
                self.active_score = max(self.active_score - 2, 0)
            return

        ## Translation
        if event.key() == Qt.Key_Right:
            self.pit.move_cube(POSITIVE_X)
        elif event.key() == Qt.Key_Left:
            self.pit.move_cube(NEGATIVE_X)
        elif event.key() == Qt.Key_Up:
            self.pit.move_cube(POSITIVE_Y)
        elif event.key() == Qt.Key_Down:
            self.pit.move_cube(NEGATIVE_Y)
        elif event.key() == Qt.Key_PageDown:
            if self.pit.move_down():
                self.active_score = max(self.active_score - 1, 0)

        ## Drop
        elif event.key() == Qt.Key_Space:
            self.pit.drop_cube()
            self.pit.add_active_cube()
            complete_indicator = self.pit.remove_completed_layers()

            self.add_score(self.calc_score(complete_indicator))
            self.add_score(self.active_score)

            live = self.pit.spawn_cube()
            self.active_score = 10
            if not live:
                QMessageBox.information(self, "Game Over", 
                    "Your score is " + str(self.score), QMessageBox.Yes)
                self.restart()

        # if event.key() == Qt.Key_Delete:
        #     text, ok = QInputDialog.getText(self, 'Dump it', 'Layer:')
        #     layer = self.pit.layers[int(text)]
        #     print layer


    #
    # Menu
    #
    def create_menu(self):
        ## Game
        self.game_menu = self.menuBar().addMenu("&Game")
        new_game_action = QAction("&New", self)
        new_game_action.setShortcut('Ctrl+N')
        new_game_action.triggered.connect(self.on_restart)
        quit_action = QAction("&Quit", self)
        quit_action.triggered.connect(self.close)
        self.game_menu.addAction(new_game_action)
        self.game_menu.addAction(quit_action)

        ## Help
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.setShortcut('F1')
        about_action.triggered.connect(self.on_about)
        self.help_menu.addAction(about_action)

    def on_restart(self):
        self.restart()

    def on_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setFont(QFont('Segoe UI', 11))
    
    window = GameWindow()
    window.show()

    sys.exit(app.exec_())
