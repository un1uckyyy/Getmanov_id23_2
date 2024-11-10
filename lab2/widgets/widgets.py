from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSlider

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

        self.birds_spawn_frequency_slider = QSlider(Qt.Horizontal)
        self.birds_spawn_frequency_slider.setMinimum(200)
        self.birds_spawn_frequency_slider.setMaximum(10000)
        self.birds_spawn_frequency_slider.setValue(5000)
        self.birds_spawn_frequency_slider.valueChanged.connect(self.set_birds_spawn_frequency)
        self.birds_spawn_frequency_timer = QTimer()
        self.birds_spawn_frequency_timer.timeout.connect(self.spawn_bird)
        self.birds_spawn_frequency_timer.start(self.birds_spawn_frequency_slider.value())
        layout.addWidget(self.birds_spawn_frequency_slider)

        self.columns_spawn_frequency_slider = QSlider(Qt.Horizontal)
        self.columns_spawn_frequency_slider.setMinimum(200)
        self.columns_spawn_frequency_slider.setMaximum(10000)
        self.columns_spawn_frequency_slider.setValue(5000)
        self.columns_spawn_frequency_slider.valueChanged.connect(self.set_columns_spawn_frequency)
        self.columns_spawn_frequency_timer = QTimer()
        self.columns_spawn_frequency_timer.timeout.connect(self.spawn_column)
        self.columns_spawn_frequency_timer.start(self.columns_spawn_frequency_slider.value())
        layout.addWidget(self.columns_spawn_frequency_slider)

    def update(self):
        time_delta = 1000 / FRAME_RATE
        self.board.update(time_delta)
        self.repaint()

    def set_birds_spawn_frequency(self, value):
        self.birds_spawn_frequency_timer.setInterval(value)

    def spawn_bird(self):
        self.board.spawn_bird()
        self.repaint()

    def set_columns_spawn_frequency(self, value):
        self.columns_spawn_frequency_timer.setInterval(value)

    def spawn_column(self, x=None):
        self.board.spawn_column(x)
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.board.draw(painter)

    def mousePressEvent(self, event):
        if 380 <= event.y() <= 530:
            self.spawn_column(event.x())

    def handle_pause_btn_clicked(self):
        if self.pause_button.isChecked():
            self.timer.stop()
            self.birds_spawn_frequency_timer.stop()
            self.columns_spawn_frequency_timer.stop()
            self.pause_button.setText('Play')
        else:
            self.timer.start(1000 // FRAME_RATE)
            self.birds_spawn_frequency_timer.start(self.birds_spawn_frequency_slider.value())
            self.columns_spawn_frequency_timer.start(self.columns_spawn_frequency_slider.value())
            self.pause_button.setText('Pause')
