import random
from typing import List, Dict

from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QRectF

from config import COLUMN_REPAIR_TIME, BIRD_FLYING_AWAY_TIME, BIRDS_NUM, COLUMNS_NUM, WINDOW_WIDTH, BIRD_SITTING_TIME
from .constants import ColumnState, BirdState


class Board:
    def __init__(self):
        self.birds: List[Bird] = []
        for _ in range(BIRDS_NUM):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, 150)
            bird = Bird(x, y)
            self.birds.append(bird)

        self.columns: List[Column] = []
        for _ in range(COLUMNS_NUM):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = 380
            max_birds = 2
            column = Column(x, y, max_birds)
            self.columns.append(column)

    def update(self, time_delta):
        for bird in self.birds:
            bird.update(time_delta, self)
        for column in self.columns:
            column.update(time_delta, self)

    def draw(self, painter: QPainter):
        for bird in self.birds:
            bird.draw(painter)

        for column in self.columns:
            column.draw(painter)

    @property
    def available_columns(self):
        return [column for column in self.columns if column.state == ColumnState.STANDING]


class Column:
    def __init__(self, x, y, durability):
        self.color = QColor(189, 189, 189)
        self.x = x
        self.y = y

        self.sitting_birds: Dict[int: Bird] = {}
        self.state = ColumnState.STANDING

        self.repair_time = 0  # время отсутствия
        self.width = 10
        self.height = 150
        self.durability = durability

    def update(self, time_delta, board: Board):
        if self.state == ColumnState.STANDING and len(self.sitting_birds) > self.durability:
            self.state = ColumnState.DESTROYED
            self.repair_time = COLUMN_REPAIR_TIME
            for bird in board.birds:
                if id(bird.target_column) == id(self):
                    bird.state = BirdState.LOOKING_FOR_COLUMN
                    bird.target_column = None
            self.sitting_birds = {}

        if self.state == ColumnState.DESTROYED:
            self.repair_time -= time_delta

        if self.repair_time < 0:
            self.state = ColumnState.STANDING

    def draw(self, painter: QPainter):
        if self.state == ColumnState.STANDING:
            painter.setBrush(QBrush(self.color))
            painter.setPen(QPen(Qt.black))
            rect = QRectF(self.x, self.y, self.width, self.height)
            rect2 = QRectF(self.x - 10, self.y, 30, 10)
            painter.drawRect(rect)
            painter.drawRect(rect2)


class Bird:
    def __init__(self, x, y):
        self.color = QColor(0, 0, 255)
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 2

        self.state = BirdState.LOOKING_FOR_COLUMN

        self.target_column: Column | None = None

        self.sitting_time: int = BIRD_SITTING_TIME

        self.flying_away_time: int = 0

    def update(self, time_delta: int, board: Board):
        if self.state == BirdState.FLYING_AWAY:
            if self.flying_away_time < 0:
                self.state = BirdState.LOOKING_FOR_COLUMN
                self.flying_away_time = 0
                return

            self.y -= self.speed
            self.flying_away_time -= time_delta
            return

        if self.state == BirdState.SITTING:
            if self.sitting_time < 0:
                self.sitting_time = BIRD_SITTING_TIME
                self.state = BirdState.FLYING_AWAY
                self.flying_away_time = BIRD_FLYING_AWAY_TIME
                self.target_column.sitting_birds.pop(id(self))
                self.target_column = None
                return

            self.sitting_time -= time_delta
            return

        if self.state == BirdState.LOOKING_FOR_COLUMN:
            available_columns = board.available_columns
            if not available_columns:
                self.y -= self.speed
                self.x += self.speed * random.randint(-1, 1)
                return
            target_column = self.pick_column(
                available_columns)  # может не быть доступных колонн, тогда target_column == None

            self.state = BirdState.FLYING_TO_COLUMN
            self.target_column = target_column

        if self.state == BirdState.FLYING_TO_COLUMN:
            dx = self.target_column.x - self.x
            dy = self.target_column.y - self.y
            delta_distance = (dx ** 2 + dy ** 2) ** 0.5

            if delta_distance < self.speed:
                self.x, self.y = self.target_column.x, self.target_column.y
                self.state = BirdState.SITTING
                self.target_column.sitting_birds[id(self)] = self
                return

            self.x += dx * self.speed / delta_distance
            self.y += dy * self.speed / delta_distance

    def draw(self, painter: QPainter):
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.black))
        painter.drawEllipse(QPointF(self.x, self.y), self.radius, self.radius)

    def pick_column(self, columns: List[Column], nearest=False) -> Column:
        if nearest:
            return self.pick_nearest_column(columns)

        return self.pick_random_column(columns)

    def pick_nearest_column(self, columns):
        return min(columns, key=lambda column: abs(self.x - column.x))

    @staticmethod
    def pick_random_column(columns):
        return random.choice(columns)
