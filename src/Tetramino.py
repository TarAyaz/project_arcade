import random
from main import GRID_WIDTH

# === Цвета тетрамин(при ошибке загрузки избражений) ===
COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 165, 0),
]
# === Шаблоны тетрамин ===
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]


# === Класс тетрамины ===
class Tetromino:
    # === конструктор тетрамины ===
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    # === функция поворота тетрамины ===
    def rotate(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        return [[self.shape[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]
