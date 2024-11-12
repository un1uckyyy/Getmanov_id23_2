from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QSpinBox

from config import FRAME_RATE, WINDOW_WIDTH, WINDOW_HEIGHT, COLUMNS_NUM

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
        self.birds_spawn_frequency_slider.setMinimum(50)
        self.birds_spawn_frequency_slider.setMaximum(10000)
        self.birds_spawn_frequency_slider.setValue(1000)
        self.birds_spawn_frequency_slider.valueChanged.connect(self.set_birds_spawn_frequency)
        self.birds_spawn_frequency_timer = QTimer()
        self.birds_spawn_frequency_timer.timeout.connect(self.spawn_bird)
        self.birds_spawn_frequency_timer.start(self.birds_spawn_frequency_slider.value())
        layout.addWidget(self.birds_spawn_frequency_slider)
        self.birds_spawn_frequency_label = QLabel(
            f"Птица прилетает раз в {self.birds_spawn_frequency_slider.value() / 1000} секунд")
        layout.addWidget(self.birds_spawn_frequency_label)
        self.when_next_bird_will_spawn = QLabel(
            f"Птица прилетит через {self.birds_spawn_frequency_timer.remainingTime() / 1000} секунд")
        layout.addWidget(self.when_next_bird_will_spawn)

        self.columns_spawn_frequency_slider = QSlider(Qt.Horizontal)
        self.columns_spawn_frequency_slider.setMinimum(200)
        self.columns_spawn_frequency_slider.setMaximum(10000)
        self.columns_spawn_frequency_slider.setValue(5000)
        self.columns_spawn_frequency_slider.valueChanged.connect(self.set_columns_spawn_frequency)
        self.columns_spawn_frequency_timer = QTimer()
        self.columns_spawn_frequency_timer.timeout.connect(self.spawn_column)
        self.columns_spawn_frequency_timer.start(self.columns_spawn_frequency_slider.value())
        layout.addWidget(self.columns_spawn_frequency_slider)
        self.columns_spawn_frequency_label = QLabel(
            f"Столб появляется раз в {self.columns_spawn_frequency_slider.value() / 1000} секунд")
        layout.addWidget(self.columns_spawn_frequency_label)
        self.when_next_column_will_spawn = QLabel(
            f"Столб появится через {self.columns_spawn_frequency_timer.remainingTime() / 1000} секунд")
        layout.addWidget(self.when_next_column_will_spawn)

        self.column_durability_spin_box = QSpinBox(self)
        self.column_durability_spin_box.setMinimum(1)
        self.column_durability_spin_box.setMaximum(1000)
        self.column_durability_spin_box.hide()
        self.column_durability_spin_box.valueChanged.connect(self.set_columns_durability)
        self.selected_column_id: int = 0

    def update(self):
        self.when_next_bird_will_spawn.setText(
            f"Птица прилетит через {self.birds_spawn_frequency_timer.remainingTime() / 1000} секунд")
        self.when_next_column_will_spawn.setText(
            f"Столб появится через {self.columns_spawn_frequency_timer.remainingTime() / 1000} секунд")
        time_delta = 1000 / FRAME_RATE
        self.board.update(time_delta)
        self.repaint()

    def set_birds_spawn_frequency(self, value):
        self.birds_spawn_frequency_label.setText(
            f"Птица прилетает раз в {self.birds_spawn_frequency_slider.value() / 1000} секунд")
        self.birds_spawn_frequency_timer.setInterval(value)

    def spawn_bird(self):
        self.board.spawn_bird()
        self.repaint()

    def set_columns_spawn_frequency(self, value):
        self.columns_spawn_frequency_label.setText(
            f"Столб появляется раз в {self.columns_spawn_frequency_slider.value() / 1000} секунд")
        self.columns_spawn_frequency_timer.setInterval(value)

    def spawn_column(self, x=None, force=False):
        if len(self.board.columns) < COLUMNS_NUM or force:
            self.board.spawn_column(x)
            self.repaint()

    def set_columns_durability(self, value):
        if self.selected_column_id:
            self.board.columns[self.selected_column_id].durability = value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.board.draw(painter)

    def mousePressEvent(self, event):
        columns = self.board.columns
        columns_positions = [(column_id, column) for column_id, column in columns.items() if
                             column.x <= event.x() <= column.x + column.width]
        if 380 <= event.y() <= 530 and columns_positions:
            column_id, column = columns_positions[0][0], columns_positions[0][1]
            if self.column_durability_spin_box.isHidden():
                self.column_durability_spin_box.setGeometry(column.x, column.y + column.height, 100, 30)
                self.column_durability_spin_box.setValue(columns[column_id].durability)

                self.column_durability_spin_box.show()

                self.selected_column_id = column_id
            elif self.selected_column_id != column_id:
                self.selected_column_id = column_id
                self.column_durability_spin_box.setValue(columns[column_id].durability)
                self.column_durability_spin_box.setGeometry(column.x, column.y + column.height, 100, 30)
            else:
                self.column_durability_spin_box.hide()
                self.selected_column_id = 0
        elif 380 <= event.y() <= 530:
            self.spawn_column(event.x(), force=True)

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
