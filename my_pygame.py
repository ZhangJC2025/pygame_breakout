import pygame as pg
import sys
import time

# colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
BACKGROUND_COLOR = black

# window size
WIDTH = 800
HEIGTH = 600

# debug mode off
DEBUG_MODE = False

# game status false to stop
GAME_STATUS = True

# game score
SCORE = 0


class Paddle:
    def __init__(self, x, y, width, height):
        self.width = width  # 100
        self.height = height  # 20
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.color = white
        self.hit_box = pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pg.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height),
        )
        if DEBUG_MODE:
            pg.draw.rect(screen, green, self.hit_box, 3)

    def move(self, speed):
        self.x += speed
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

        self.hit_box.x = self.x
        self.hit_box.y = self.y


class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x - self.radius
        self.y = y - self.radius
        self.speed_x = 400
        self.speed_y = 400
        self.color = red
        self.hit_box = pg.Rect(self.x - self.radius, self.y - self.radius, 20, 20)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        if DEBUG_MODE:
            pg.draw.rect(screen, green, self.hit_box, 3)

    def move(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

        if self.x < self.radius:
            self.x = self.radius
            self.speed_x = -self.speed_x
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.speed_x = -self.speed_x

        if self.y < self.radius:
            self.y = self.radius
            self.speed_y = -self.speed_y
        if self.y > HEIGTH - self.radius:
            """self.y = HEIGTH - self.radius
            self.speed_y = -self.speed_y"""
            global GAME_STATUS
            GAME_STATUS = False

        self.hit_box.x = self.x - self.radius
        self.hit_box.y = self.y - self.radius

    def rebound(self):
        """
        TODO : better way to decide the direction
        """
        self.speed_y = -self.speed_y


class Block(Paddle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        return super().draw(screen)

    def move(self, speed):
        return super().move(speed)


class Block_generator:
    def __init__(self, x_range, y_range, line, row):
        self.line = line
        self.row = row
        self.x_range = x_range
        self.y_range = y_range
        self.block_array = []
        for i in range(1, line):
            for j in range(1, row):
                y = (y_range[1] - y_range[0]) / line * i + y_range[0]
                x = (x_range[1] - x_range[0]) / row * j + x_range[0]

                self.block_array.append(Block(x, y, 10, 10))

    def draw(self, surface):
        for block in self.block_array:
            block.draw(surface)

    def destory(self, ball):
        if ball in self.block_array:
            self.block_array.remove(ball)
            global SCORE
            SCORE += 1


def input_handler(eneity, dt):
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        eneity.move(-600 * dt)
    if keys[pg.K_d]:
        eneity.move(600 * dt)
    if keys[pg.K_F3]:
        global DEBUG_MODE
        if DEBUG_MODE:
            DEBUG_MODE = False
        else:
            DEBUG_MODE = True
    if not GAME_STATUS and keys[pg.K_SPACE]:
        main()


def ui_render(surface, dt):
    # fps render
    if dt:
        fps = int(1 / dt)
    else:
        fps = 0
    font_render(surface, 40, f"fps:{fps}", white, (50, 20))

    # score render
    font_render(surface, 40, f"score:{SCORE}", white, (60, surface.get_height() - 20))


def font_render(surface, size, text, color, position):
    font = pg.font.Font(None, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = position
    surface.blit(text, text_rect)


def dead_page(surface):
    surface.fill(red)

    font_render(
        surface,
        30,
        "press esc to escape or space to restart",
        black,
        (surface.get_width() - 200, surface.get_height() - 20),
    )  # esc tips
    font_render(
        surface,
        80,
        "Game Over!",
        black,
        (surface.get_width() / 2, surface.get_height() / 2),
    )  # game over
    font_render(
        surface,
        40,
        f"your score is {SCORE}",
        black,
        (surface.get_width() / 2, surface.get_height() / 2 + 40),
    )  # player's score

    pg.display.update()


def game_init():
    global GAME_STATUS
    GAME_STATUS = True
    global SCORE
    SCORE = 0


def main():
    pg.init()
    game_init()

    screen = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption("Breakout")
    start = time.time()
    # entitys
    paddle = Paddle(screen.get_width() / 2, screen.get_height() - 100, 100, 20)
    ball = Ball(screen.get_width() / 2 - 150, screen.get_height() / 2)
    block_generator = Block_generator((0, WIDTH), (20, 200), 10, 30)

    clock = pg.time.Clock()
    dt = 0

    running = True
    while running:
        if GAME_STATUS:
            playing_time = time.time() - start
            pg.display.set_caption(f"play Breakout {playing_time:.2f}s")

        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                running = False

        screen.fill(BACKGROUND_COLOR)

        input_handler(paddle, dt)

        ui_render(screen, dt)

        ball.move(dt)

        # collider
        if ball.hit_box.colliderect(paddle.hit_box):
            ball.rebound()
        for block in block_generator.block_array:
            if ball.hit_box.colliderect(block.hit_box):
                block_generator.destory(block)
                ball.rebound()

        paddle.draw(screen)
        ball.draw(screen)
        block_generator.draw(screen)

        dt = clock.tick(60) / 1000

        if GAME_STATUS:
            pg.display.update()
        else:
            dead_page(screen)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
