import arcade
import os
import random

TITLE = "Tetris"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 165, 0),
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

PLAYFIELD_WIDTH = GRID_WIDTH * GRID_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * GRID_SIZE
PLAYFIELD_X = (SCREEN_WIDTH - SIDEBAR_WIDTH - PLAYFIELD_WIDTH) // 2 + 126
PLAYFIELD_Y = (SCREEN_HEIGHT - PLAYFIELD_HEIGHT) // 2 + 45


class Tetromino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        return [[self.shape[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]


class TetrisGame(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.background_sprites = arcade.SpriteList()
        self.bg_path = "images/tetris/game_fon/0.png"
        self.bg_sprite = arcade.Sprite(self.bg_path)
        self.bg_sprite.center_x = SCREEN_WIDTH // 2
        self.bg_sprite.center_y = SCREEN_HEIGHT // 2
        self.bg_sprite.width = SCREEN_WIDTH
        self.bg_sprite.height = SCREEN_HEIGHT
        self.background_sprites.append(self.bg_sprite)
        self.block_textures = []
        for i in range(7):
            path = f"images/tetris/blocks/{i}.png"
            if os.path.exists(path):
                self.block_textures.append(arcade.load_texture(path))
            else:
                color_img = arcade.Texture.create_filled(
                    name=f"color_block_{i}", size=(1, 1), color=COLORS[i]
                )
                self.block_textures.append(color_img)

        self.next_piece_sprites = arcade.SpriteList()
        self.reset()

        # self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def on_draw(self):
        self.clear()
        self.background_sprites.draw()

        self.block_sprites.draw()
        self._update_next_piece_display()

        arcade.draw_text(
            "NEXT",
            PLAYFIELD_X + PLAYFIELD_WIDTH + 40,
            PLAYFIELD_Y + PLAYFIELD_HEIGHT - 60,
            arcade.color.WHITE,
            16,
            anchor_x="left",
        )
        # for y in range(GRID_HEIGHT):
        #     for x in range(GRID_WIDTH):
        #         pass

    def _update_next_piece_display(self):
        self.next_sprite_block.clear()
        shape = self.next_piece.shape

        offset_x = (4 - len(shape[0])) // 2
        offset_y = (4 - len(shape)) // 2

        base_x = PLAYFIELD_X + PLAYFIELD_WIDTH + 30
        base_y = PLAYFIELD_Y + PLAYFIELD_HEIGHT - 100
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    x = base_x + (offset_x + c) * GRID_SIZE
                    y = base_y + (offset_y + r) * GRID_SIZE
                    center_x = x + GRID_SIZE // 2
                    center_y = y + GRID_SIZE // 2
                    sprite = arcade.Sprite()
                    sprite.texture = self.block_textures[self.next_piece.shape_idx]
                    sprite.center_x = center_x
                    sprite.center_y = center_y
                    sprite.width = GRID_SIZE
                    sprite.height = GRID_SIZE
                    self.next_sprite_block.append(sprite)

    def reset(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.fall_speed = 0.5
        self.fall_timer = 0.0
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.block_sprites = arcade.SpriteList()

    def valid_position(self, shape, x, y):
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    px, py = x + c, y + r
                    if px < 0 or px >= GRID_WIDTH or py >= GRID_HEIGHT:
                        return False
                    if py >= 0 and self.grid[py][px] != 0:
                        return False
        return True

    def move(self, dx, dy):
        if self.game_over or self.paused:
            return False
        nx, ny = self.current_piece.x + dx, self.current_piece.y + dy
        if self.valid_position(self.current_piece.shape, nx, ny):
            self.current_piece.x, self.current_piece.y = nx, ny
            return True
        return False

    def rotate_piece(self):
        if self.game_over or self.paused:
            return False
        rotated = self.current_piece.rotate()
        if self.valid_position(rotated, self.current_piece.x, self.current_piece.y):
            self.current_piece.shape = rotated
            return True
        return False

    def on_update(self, delta_time):
        if self.paused or self.game_over:
            self._rebuild_block_sprites()
            return
        self.fall_timer += delta_time
        if self.fall_timer >= self.fall_speed:
            self.fall_timer = 0
            if not self.move(0, 1):
                self.merge_piece()
                self.clear_lines()
                self.new_piece()
        self._rebuild_block_sprites()
        if self.paused or self.game_over:
            self._update_next_piece_display()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R and self.game_over:
            self.reset()
        elif key == arcade.key.P:
            self.paused = not self.paused
        elif not self.paused and not self.game_over:
            if key == arcade.key.W:
                self.rotate_piece()
            elif key == arcade.key.A:
                self.move(-1, 0)
            elif key == arcade.key.D:
                self.move(1, 0)
            elif key == arcade.key.SPACE:
                while self.move(0, 1):
                    pass

    def merge_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    gy = self.current_piece.y + r
                    if gy >= 0:
                        self.grid[gy][self.current_piece.x + c] = (
                            self.current_piece.shape_idx + 1
                        )

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if not self.valid_position(
            self.current_piece.shape, self.current_piece.x, self.current_piece.y
        ):
            self.game_over = True
        else:
            self._update_next_piece_display()

    def _rebuild_block_sprites(self):
        self.block_sprites.clear()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_value = self.grid[y][x]
                if cell_value:
                    shape_idx = cell_value - 1
                    self._add_block_to_sprite_list(x, y, shape_idx)

        if not self.game_over:
            for r, row in enumerate(self.current_piece.shape):
                for c, cell in enumerate(row):
                    if cell:
                        x = (self.current_piece.x + c,)
                        y = (self.current_piece.y + r,)
                        if y >= 0:
                            self._add_block_to_sprite_list(
                                x, y, self.current_piece.shape_idx
                            )

    def _add_block_to_sprite_list(self, x, y, shape_idx):
        if not 0 <= x < GRID_WIDTH:
            return
        center_x = PLAYFIELD_X + x * GRID_SIZE + GRID_SIZE / 2
        center_y = PLAYFIELD_Y + y * GRID_SIZE + GRID_SIZE / 2
        sprite = arcade.Sprite()
        sprite.texture = self.block_textures[shape_idx]
        sprite.center_x = center_x
        sprite.center_y = center_y
        sprite.width = GRID_SIZE
        sprite.height = GRID_SIZE
        self.block_sprites.append(sprite)


def main():
    game = TetrisGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
