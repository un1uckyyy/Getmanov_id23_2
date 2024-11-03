from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from config import FRAME_RATE, WINDOW_WIDTH, WINDOW_HEIGHT

from models.models import Board


class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.board = Board()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // FRAME_RATE)

    def update(self):
        time_delta = 1000 / FRAME_RATE
        self.board.update(time_delta)
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.board.draw(painter)
