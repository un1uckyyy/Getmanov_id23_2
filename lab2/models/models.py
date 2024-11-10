import json
import os.path
import random
import sys
from typing import List, Dict

from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from config import (
    COLUMN_REPAIR_TIME,
    BIRD_FLYING_AWAY_TIME,
    BIRDS_NUM,
    COLUMNS_NUM,
    WINDOW_WIDTH,
    BIRD_SITTING_TIME,
    COLUMN_DURABILITY,
)
from .constants import ColumnState, BirdState


class Board:
    def __init__(self, file_path=None, create_path="random_initial_state.json"):
        self.birds: Dict[int: Bird] = {}
        self.columns: Dict[int: Column] = {}

        if file_path is not None:
            self.try_load_initial_state(file_path)
        else:
            self.create_random_initial_state(create_path)

    def spawn_bird(self):
        x = random.randint(50, WINDOW_WIDTH - 50)
        y = random.randint(50, 150)
        bird = Bird(x, y)
        self.birds[id(bird)] = bird

    def spawn_column(self, x=None):
        if x is None:
            x = random.randint(50, WINDOW_WIDTH - 50)
        y = 380
        column = Column(x, y)
        self.columns[id(column)] = column

    def try_load_initial_state(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                state = json.load(f)
                birds_props = state.get("birds", [])
                for bird_prop in birds_props:
                    bird = Bird(**bird_prop)
                    self.birds[id(bird)] = bird

                columns_props = state.get("columns", [])
                for column_prop in columns_props:
                    column = Column(**column_prop)
                    self.columns[id(column)] = column
        else:
            print(f"Не удалось найти указанный файл: {file_path}")
            sys.exit(1)

    def create_random_initial_state(self, create_path):
        for _ in range(BIRDS_NUM):
            self.spawn_bird()

        for _ in range(COLUMNS_NUM):
            self.spawn_column()

        with open(create_path, 'w') as f:
            state = {
                "birds": [bird.toJSON() for bird in self.birds.values()],
                "columns": [column.toJSON() for column in self.columns.values()],
            }
            json.dump(state, f, indent=1)

    def update(self, time_delta):
        for bird in list(self.birds.values()):
            bird.update(time_delta, self)
            if bird.state == BirdState.FLEW_AWAY:
                del self.birds[id(bird)]
        for column in list(self.columns.values()):
            column.update(time_delta, self)
            if column.state == ColumnState.DESTROYED:
                del self.columns[id(column)]

    def draw(self, painter: QPainter):
        for bird in self.birds.values():
            bird.draw(painter)

        for column in self.columns.values():
            column.draw(painter)

    @property
    def available_columns(self):
        return [column for column in self.columns.values() if column.state == ColumnState.STANDING]


class Column:
    def __init__(self, x, y, durability=COLUMN_DURABILITY):
        self.color = QColor(189, 189, 189)
        self.x = x
        self.y = y

        self.sitting_birds: Dict[int: Bird] = {}
        self.state = ColumnState.STANDING

        self.width = 10
        self.height = 150
        self.durability = durability

    def toJSON(self):
        return {
            "x": self.x,
            "y": self.y,
            "durability": self.durability,
        }

    def update(self, time_delta, board: Board):
        if self.state == ColumnState.STANDING and len(self.sitting_birds) > self.durability:
            self.state = ColumnState.DESTROYED
            for bird in board.birds.values():
                if id(bird.target_column) == id(self):
                    bird.state = BirdState.LOOKING_FOR_COLUMN
                    bird.target_column = None

    def draw(self, painter: QPainter):
        if self.state == ColumnState.STANDING:
            painter.setBrush(QBrush(self.color))
            painter.setPen(QPen(Qt.black))
            rect = QRectF(self.x, self.y, self.width, self.height)
            rect2 = QRectF(self.x - 10, self.y, 30, 10)
            painter.drawRect(rect)
            painter.drawRect(rect2)


class Bird:
    def __init__(self, x, y, sitting_time=BIRD_SITTING_TIME):
        self.color = QColor(0, 0, 255)
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 2

        self.state = BirdState.LOOKING_FOR_COLUMN

        self.target_column: Column | None = None

        self.sitting_time: int = sitting_time


    def toJSON(self):
        return {
            "x": self.x,
            "y": self.y,
            "sitting_time": self.sitting_time,
        }

    def update(self, time_delta: int, board: Board):
        if self.state == BirdState.FLYING_AWAY:
            if self.y < 0:
                self.state = BirdState.FLEW_AWAY
                return

            self.y -= self.speed
            return

        if self.state == BirdState.SITTING:
            if self.sitting_time < 0:
                self.sitting_time = BIRD_SITTING_TIME
                self.state = BirdState.FLYING_AWAY
                self.target_column.sitting_birds.pop(id(self))
                self.target_column = None
                return

            self.sitting_time -= time_delta
            return

        if self.state == BirdState.LOOKING_FOR_COLUMN:
            available_columns = board.available_columns
            if not available_columns:
                self.y += self.speed * random.randint(-1, 1)
                self.x += self.speed * random.randint(-1, 1)
                return
            target_column = self.pick_column(
                available_columns)

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
