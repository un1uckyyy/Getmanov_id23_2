from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

from config import FRAME_RATE, WINDOW_WIDTH, WINDOW_HEIGHT

from models.models import Board


class DrawingArea(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        board_opt = {}
        file = kwargs.get('file')
        if file:
            board_opt['file_path'] = file
        board_opt['create_path'] = kwargs.get('create')
        self.board = Board(**board_opt)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // FRAME_RATE)

        self.pause_button = QPushButton('Pause')
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.handle_pause_btn_clicked)
        layout.addWidget(self.pause_button)

    def update(self):
        time_delta = 1000 / FRAME_RATE
        self.board.update(time_delta)
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.board.draw(painter)

    def handle_pause_btn_clicked(self):
        if self.pause_button.isChecked():
            self.timer.stop()
            self.pause_button.setText('Play')
        else:
            self.timer.start(1000 // FRAME_RATE)
            self.pause_button.setText('Pause')
