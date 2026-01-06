import arcade


TITLE = "Tetris"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

PLAYFIELD_WIDTH = GRID_WIDTH * GRID_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * GRID_SIZE
PLAYFIELD_X = (SCREEN_WIDTH - SIDEBAR_WIDTH - PLAYFIELD_WIDTH) // 2 + 126
PLAYFIELD_Y = (SCREEN_HEIGHT - PLAYFIELD_HEIGHT) // 2 + 45


class TetrisGame(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.bg_path = "../images/tetris/game_fon/0.png"
        self.background_color = arcade.load_texture(self.bg_path)

        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background,
        )

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pass


def main():
    game = TetrisGame()
    arcade.run()


if __name__ == "__main__":
    main()
