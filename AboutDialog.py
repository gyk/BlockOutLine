from PyQt4.QtCore import *
from PyQt4.QtGui import *

about_text = """\
<big><b>BlockOutLine</b></big><br/>
<em><b>The 3D Tetris game for flatlanders</b></em><br/>
<em>Version 0.0.1</em><br/>
<br/>
BlockOutLine is the side-view version of the classic <br/>
<a href="http://en.wikipedia.org/wiki/Blockout">
Blockout</a> game. Provided with multiple facades as <br/>
hint, the player needs to interpret these 2D <br/>
projections and rebuild the 3D scene in the mind. <br/>
<br/>
The four panels from left to right show the back, left, <br/>
front, right views (orthographic projections) of the <br/>
cubes respectively, where solid lines represent visible <br/>
edges and dashed lines represent hidden ones.<br/>
<br/>
The goal of the game is to form complete layers and <br/>
gain score points as high as possible. <br/>
<br/>
"""

keys_desc = [
    ('Q', "Rotate +X"),
    ('A', "Rotate -X"),
    ('W', "Rotate +Y"),
    ('S', "Rotate -Y"),
    ('E', "Rotate +Z"),
    ('D', "Rotate -Z"),
    ('Left arrow', "Move left"),
    ('Right arrow', "Move right"),
    ('Up arrow', "Move forward"),
    ('Down arrow', "Move backward"),
    ('PageDown', "Move down"),
    ('Space', "Drop"),
]

credits_text = """<br/>
This game was written in Python 2.7 with PyQt 4.9.<br/>
Based on the code from <a href="http://eli.thegreenplace.net">Eli Bendersky</a>'s 
Tetris clone.<br/>
<br/>
The source code is hosted on <a href="https://github.com/gyk/BlockOutLine">
GitHub</a>.<br/>
<hr/>
Developed by Yukun Guo<br/>
License: LGPL (<a href="http://www.gnu.org/copyleft/lgpl.html">
http://www.gnu.org/copyleft/lgpl.html</a>)
"""

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle('About BlockOutLine')

        #
        # About
        #
        about_page = QWidget(self)
        about_label = QLabel(about_text)
        about_label.setOpenExternalLinks(True)

        about_layout = QVBoxLayout()
        about_layout.addWidget(about_label, 0, Qt.AlignCenter)
        about_page.setLayout(about_layout)

        #
        # Keys
        #
        keys_page = QWidget(self)
        keys_layout = QGridLayout()

        i = 0
        for key, desc in keys_desc:
            keys_layout.addWidget(QLabel("  " + key), i, 0)
            keys_layout.addWidget(QLabel(desc), i, 1)
            i += 1
        
        keys_page.setLayout(keys_layout)

        #
        # Credits
        #
        credits_page = QWidget(self)
        credits_label = QLabel(credits_text)
        credits_label.setAlignment(Qt.AlignTop)
        credits_label.setOpenExternalLinks(True)

        credits_layout = QVBoxLayout()
        credits_layout.addWidget(credits_label)
        credits_page.setLayout(credits_layout)

        #
        # Organizes tabs
        #
        tabs = QTabWidget(self)        
        tabs.addTab(about_page, 'About')
        tabs.addTab(keys_page, 'Keys')
        tabs.addTab(credits_page, 'Credits')

        #
        # Dialog layout
        #
        ok_button = QPushButton('&OK')
        ok_button.clicked.connect(self.accept)
        
        bbox = QHBoxLayout()
        bbox.addStretch()
        bbox.addWidget(ok_button)
        bbox.addStretch()
        
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        layout.addLayout(bbox)
        self.setLayout(layout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = AboutDialog()
    dialog.exec_()
