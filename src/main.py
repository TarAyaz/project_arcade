import arcade
import os
import time
from Tetramino import *

# === Константы ===
TITLE = "Tetris"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# === Координаты поля ===
PLAYFIELD_WIDTH = GRID_WIDTH * GRID_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * GRID_SIZE
PLAYFIELD_X = (SCREEN_WIDTH - SIDEBAR_WIDTH - PLAYFIELD_WIDTH) // 2 + 125
PLAYFIELD_Y = (SCREEN_HEIGHT - PLAYFIELD_HEIGHT) // 2 - 46


# === Класс игры ===
class TetrisGame(arcade.Window):
    # === конструктор игры ===
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.game_over_sound = arcade.load_sound("../sounds/sfx/game_over.mp3")
        self.clear_sound = arcade.load_sound("../sounds/sfx/line_clear.mp3")
        self.move_sound = arcade.load_sound("../sounds/sfx/move_piece.mp3")
        self.drop_sound = arcade.load_sound("../sounds/sfx/piece_landed.mp3")
        self.rotate_sound = arcade.load_sound("../sounds/sfx/rotate_piece.mp3")
        self.tetris_music = arcade.load_sound("../sounds/music/Tetris_Theme.mp3")
        self.is_game_not_over = True
        self.background_sprites = arcade.SpriteList()
        self.bg_path = "../images/tetris/game_fon/0.png"
        self.bg_sprite = arcade.Sprite(self.bg_path)
        self.bg_sprite.center_x = SCREEN_WIDTH // 2
        self.bg_sprite.center_y = SCREEN_HEIGHT // 2
        self.bg_sprite.width = SCREEN_WIDTH
        self.bg_sprite.height = SCREEN_HEIGHT
        self.background_sprites.append(self.bg_sprite)
        self.block_textures = []
        for i in range(7):
            path = f"../images/tetris/blocks/{i}.png"
            if os.path.exists(path):
                self.block_textures.append(arcade.load_texture(path))
            else:
                color_img = arcade.Texture.create_filled(
                    name=f"color_block_{i}", size=(1, 1), color=COLORS[i]
                )
                self.block_textures.append(color_img)

        self.next_piece_sprites = arcade.SpriteList()

        font_path = "../images/tetris/fonts/PressStart2P-Regular.ttf"
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.font_name = "Press Start 2P"
        else:
            self.font_name = "Arial"
        self.preset_key = set()
        self.max_score = 0
        self.reset()

    # === функция отрисовки игры ===
    def on_draw(self):
        self.clear()
        self.background_sprites.draw()
        self.block_sprites.draw()
        self.next_piece_sprites.draw()

        arcade.draw_text(
            "NEXT",
            PLAYFIELD_X + PLAYFIELD_WIDTH + 71,
            PLAYFIELD_Y + PLAYFIELD_HEIGHT // 2 + 60,
            arcade.color.WHITE,
            16,
            font_name=self.font_name,
            anchor_x="left",
        )
        arcade.draw_text(
            "Score:",
            SCREEN_WIDTH - 190,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            f"{self.score:06d}",
            SCREEN_WIDTH - 190,
            SCREEN_HEIGHT - 90,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            "Record:",
            SCREEN_WIDTH - 190,
            SCREEN_HEIGHT - 130,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            f"{self.max_score:06d}",
            SCREEN_WIDTH - 190,
            SCREEN_HEIGHT - 170,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            "Level:",
            SCREEN_WIDTH - 190,
            160,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            f"{self.level:06d}",
            SCREEN_WIDTH - 190,
            125,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            "Lines:",
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )
        arcade.draw_text(
            f"{self.lines_cleared:07d}",
            SCREEN_WIDTH // 2 + 20,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            14,
            font_name=self.font_name,
        )

        if self.game_over:
            arcade.stop_sound(self.music)
            if self.is_game_not_over:
                arcade.play_sound(self.game_over_sound)
                self.is_game_not_over = False
            self.max_score = max(self.score, self.max_score)
            arcade.draw_lbwh_rectangle_filled(
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (0, 0, 0, 200),
            )
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 60,
                arcade.color.WHITE,
                24,
                font_name=self.font_name,
                anchor_x="center",
            )
            arcade.draw_text(
                "Press R to Restart",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.WHITE,
                16,
                font_name=self.font_name,
                anchor_x="center",
            )

            stats_x = 70
            stats_y = SCREEN_HEIGHT - 205
            arcade.draw_text(
                "Piece Stats",
                stats_x,
                stats_y,
                arcade.color.WHITE,
                12,
                font_name=self.font_name,
            )

            stats_sprites = arcade.SpriteList()
            mini_size = 16
            for i in range(7):
                shape = SHAPES[i]
                h, w = len(shape), len(shape[0])
                off_x = (4 - w) * mini_size // 2
                off_y = (4 - h) * mini_size // 2
                base_y = stats_y - 75 - i * 55

                for r, row in enumerate(shape):
                    for c, cell in enumerate(row):
                        if cell:
                            px = stats_x + 20 + off_x + c * mini_size
                            py = base_y + off_y + r * mini_size
                            sprite = arcade.Sprite()
                            sprite.texture = self.block_textures[i]
                            sprite.center_x = px + mini_size // 2
                            sprite.center_y = py + mini_size // 2
                            sprite.width = mini_size
                            sprite.height = mini_size
                            stats_sprites.append(sprite)

                arcade.draw_text(
                    f"x{self.piece_count[i]}",
                    stats_x + 30 + 4 * mini_size,
                    base_y + 27,
                    arcade.color.WHITE,
                    10,
                    font_name=self.font_name,
                )

            stats_sprites.draw()

    # === функция отрисовки следующей фигуры ===
    def _update_next_piece_display(self):
        self.next_piece_sprites.clear()
        shape = self.next_piece.shape
        shape_idx = self.next_piece.shape_idx

        offset_x = (4 - len(shape[0])) // 2
        offset_y = (4 - len(shape)) // 2

        base_x = PLAYFIELD_X + PLAYFIELD_WIDTH + 75
        base_y = PLAYFIELD_Y + PLAYFIELD_HEIGHT - 220
        if shape_idx == 0:
            base_y -= 10
            base_x -= 12
        elif shape_idx == 1:
            base_y += 6
            base_x -= 10
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    x = base_x + (offset_x + c) * GRID_SIZE
                    y = base_y - (offset_y + r) * GRID_SIZE
                    center_x = x + GRID_SIZE // 2
                    center_y = y + GRID_SIZE // 2
                    sprite = arcade.Sprite()
                    sprite.texture = self.block_textures[self.next_piece.shape_idx]
                    sprite.center_x = center_x
                    sprite.center_y = center_y
                    sprite.width = GRID_SIZE
                    sprite.height = GRID_SIZE
                    self.next_piece_sprites.append(sprite)

    # === функция сброса игры ===
    def reset(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.is_game_not_over = True
        self.fall_speed = 0.5
        self.fall_timer = 0.0
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.piece_count = [0] * 7
        self.block_sprites = arcade.SpriteList()
        self.horizontal_delay = 0.1
        self.last_horizontal_time = 0.0
        self._update_next_piece_display()
        self.music = arcade.play_sound(self.tetris_music, loop=True)

    # === функция проверки допустимости позиции фигуры ===
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

    # === функция перемещения фигуры ===
    def move(self, dx, dy):
        if self.game_over or self.paused:
            return False
        nx, ny = self.current_piece.x + dx, self.current_piece.y + dy
        if self.valid_position(self.current_piece.shape, nx, ny):
            self.current_piece.x, self.current_piece.y = nx, ny
            return True
        return False

    # === функция поворота фигуры ===
    def rotate_piece(self):
        if self.game_over or self.paused:
            return False
        rotated = self.current_piece.rotate()
        if self.valid_position(rotated, self.current_piece.x, self.current_piece.y):
            self.current_piece.shape = rotated
            arcade.play_sound(self.rotate_sound)
            return True
        return False

    # === функция обновления игрового мира ===
    def on_update(self, delta_time):
        if self.paused or self.game_over:
            self._rebuild_block_sprites()
            return

        current_time = time.time()
        keys = self.preset_key

        if arcade.key.A in keys:
            if current_time - self.last_horizontal_time >= self.horizontal_delay:
                self.move(-1, 0)
                self.last_horizontal_time = current_time
                arcade.play_sound(self.move_sound)
        elif arcade.key.D in keys:
            if current_time - self.last_horizontal_time >= self.horizontal_delay:
                self.move(1, 0)
                self.last_horizontal_time = current_time
                arcade.play_sound(self.move_sound)
        else:
            self.last_horizontal_time = current_time

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

    # === функция обработки нажатия клавиш ===
    def on_key_press(self, key, modifiers):
        self.preset_key.add(key)
        if key == arcade.key.R and self.game_over:
            self.reset()
        elif key == arcade.key.P:
            self.paused = not self.paused
        elif not self.paused and not self.game_over:
            if key == arcade.key.W:
                self.rotate_piece()
            elif key == arcade.key.SPACE:
                is_moving = False
                while self.move(0, 1):
                    is_moving = True
                if is_moving:
                    arcade.play_sound(self.drop_sound)

    # === функция обработки отпускания клавиш ===
    def on_key_release(self, key, modifiers):
        if key in self.preset_key:
            self.preset_key.remove(key)

    # === функция слияния фигуры ===
    def merge_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    gy = self.current_piece.y + r
                    if gy >= 0:
                        self.grid[gy][self.current_piece.x + c] = (
                                self.current_piece.shape_idx + 1
                        )

    # === функция создания новой фигуры ===
    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        self.piece_count[self.current_piece.shape_idx] += 1
        if not self.valid_position(
                self.current_piece.shape, self.current_piece.x, self.current_piece.y
        ):
            self.game_over = True
        else:
            self._update_next_piece_display()

    # === функция перестройки блоков ===
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
                        x = self.current_piece.x + c
                        y = self.current_piece.y + r
                        if y >= 0:
                            self._add_block_to_sprite_list(
                                x, y, self.current_piece.shape_idx
                            )

    # === функция добавления блока в список спрайтов ===
    def _add_block_to_sprite_list(self, x, y, shape_idx):
        if not 0 <= x < GRID_WIDTH:
            return
        center_x = PLAYFIELD_X + x * GRID_SIZE + GRID_SIZE // 2
        center_y = PLAYFIELD_Y + (GRID_HEIGHT - y - 1) * GRID_SIZE + GRID_SIZE // 2
        sprite = arcade.Sprite()
        sprite.texture = self.block_textures[shape_idx]
        sprite.center_x = center_x
        sprite.center_y = center_y
        sprite.width = GRID_SIZE
        sprite.height = GRID_SIZE
        self.block_sprites.append(sprite)

    # === функция очистки строк ===
    def clear_lines(self):
        lines_to_clear = [y for y in range(GRID_HEIGHT) if all(self.grid[y])]
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0] * GRID_WIDTH)

        if lines_to_clear:
            clear = len(lines_to_clear)
            self.lines_cleared += clear
            self.score += [100, 300, 500, 800][min(clear - 1, 3)] * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)
            arcade.play_sound(self.clear_sound)


def main():
    game = TetrisGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
