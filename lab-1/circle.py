from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPainter, QBrush, QPen
from PyQt6.QtWidgets import QApplication, QWidget, QSlider, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton

from math import sin, cos, radians


class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0  # угол поворота
        self.direction = 1

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.GlobalColor.red)
        painter.drawEllipse(100, 100, 400, 400)  # окружность с центром (200, 200)

        # точка
        x = 300 + 200 * cos(radians(self.angle))
        y = 300 + 200 * sin(radians(self.angle))
        painter.setBrush(QBrush(Qt.GlobalColor.red))
        painter.drawEllipse(int(x - 5), int(y - 5), 10, 10)

        # обновляем угол
        self.angle += self.direction % 360

    def change_direction(self):
        self.direction *= -1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(600, 600))

        # Слайдер с выбором скорости точки
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(5)
        self.slider.setMaximum(55)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.set_speed)

        # добавление слайдера
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)
        layout.addWidget(self.slider)

        # добавление области для рисования круга
        self.drawing_area = DrawingWidget()
        layout.addWidget(self.drawing_area)

        # добавление переключателя
        self.toggle_button = QPushButton("Изменить направление")
        self.toggle_button.clicked.connect(self.drawing_area.change_direction)
        layout.addWidget(self.toggle_button)

        # Таймер
        self.timer = QTimer()
        self.timer.setInterval(self.slider.value())
        self.timer.timeout.connect(self.drawing_area.update)
        self.timer.start()

    def set_speed(self, value):
        self.timer.setInterval(value)  # обновляем интервал таймера


def main():
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    app.exec()


if __name__ == '__main__':
    main()
