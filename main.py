# main.py -- A small game called break out
# coded by ZhangJC2025
import pygame as pg
import sys
import time

# colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0

BACKGROUND_COLOR = black

# window size
WIDTH = 800
HEIGTH = 600

# debug mode off
DEBUG_MODE = False

# game status
GAME_STATUS = "PLAYING"

# game score
SCORE = 0

# to detect wheter cheat code in input
cheat_keys = {pg.K_w: "w", pg.K_i: "i", pg.K_n: "n"}
cheat_code = []

# if first run ?
FIRST_RUN = True


class Paddle:
    def __init__(self, x, y, width=100, height=20, color=white):
        self.width = width
        self.height = height
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.color = color
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
    def __init__(self, x, y, radius=10, speed_x=400, speed_y=400, color=red):
        self.radius = radius
        self.x = x - self.radius
        self.y = y - self.radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.hit_box = pg.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

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
            # dead detect
            global GAME_STATUS
            if GAME_STATUS == "PLAYING":
                GAME_STATUS = "LOSE"

        self.hit_box.x = self.x - self.radius
        self.hit_box.y = self.y - self.radius

    def rebound(self, others, direct):
        if direct == "up":
            self.y = others.y - self.radius
        elif direct == "down":
            self.y = others.y + self.radius
        self.speed_y = -self.speed_y


class Brick(Paddle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        super().draw(screen)

    def move(self, speed):
        super().move(speed)


class Brick_generator:
    def __init__(self, x_range, y_range, line, row):
        self.line = line
        self.row = row
        self.x_range = x_range
        self.y_range = y_range
        self.brick_array = []
        for i in range(line):
            for j in range(row):
                y = (y_range[1] - y_range[0]) / line * i + y_range[0]
                x = (x_range[1] - x_range[0]) / row * j + x_range[0]

                self.brick_array.append(Brick(x, y, 10, 10))

    def draw(self, surface):
        for brick in self.brick_array:
            brick.draw(surface)

    def destory(self, ball):
        if ball in self.brick_array:
            self.brick_array.remove(ball)
            global SCORE
            SCORE += 1
        if self.brick_array == []:
            global GAME_STATUS
            if GAME_STATUS == 1:
                GAME_STATUS = 1


def pause_page(surface):
    font_render(
        surface,
        30,
        "press esc to escape or space to continue",
        white,
        (surface.get_width() - 240, surface.get_height() - 20),
    )  # esc tips

    pg.display.update()


def win_page(surface):
    surface.fill(yellow)

    font_render(
        surface,
        30,
        "press esc to escape or space to restart",
        black,
        (surface.get_width() - 240, surface.get_height() - 20),
    )  # esc tips
    font_render(
        surface,
        80,
        "You win!",
        black,
        (surface.get_width() / 2, surface.get_height() / 2),
    )  # words for winner
    font_render(
        surface,
        40,
        f"your score is {SCORE}",
        black,
        (surface.get_width() / 2, surface.get_height() / 2 + 40),
    )  # player's score

    pg.display.update()


def game_init():
    global cheat_code
    cheat_code = []
    global GAME_STATUS
    GAME_STATUS = "PLAYING"
    global SCORE
    SCORE = 0


def input_handler(paddle, dt, brick_generator):
    keys = pg.key.get_pressed()

    global GAME_STATUS
    if GAME_STATUS == "PLAYING":
        if keys[pg.K_a]:
            paddle.move(-600 * dt)
        if keys[pg.K_d]:
            paddle.move(600 * dt)

        if keys[pg.K_p]:
            GAME_STATUS = "PAUSE"

    elif GAME_STATUS == "PAUSE":
        if keys[pg.K_SPACE]:
            GAME_STATUS = "PLAYING"

    elif GAME_STATUS == "LOSE":
        if keys[pg.K_SPACE]:
            main()
    elif GAME_STATUS == "WIN":
        if keys[pg.K_SPACE]:
            main()

    if keys[pg.K_ESCAPE]:
        GAME_STATUS = "EXIT"

    # cheat code
    global cheat_code
    for cheat_key, key_char in cheat_keys.items():
        if keys[cheat_key] and key_char not in cheat_code:
            cheat_code.append(key_char)
    isCHEATED = True
    for cheat_key, key_char in cheat_keys.items():
        if key_char not in cheat_code:
            isCHEATED = False
    if isCHEATED:
        cheat_mode(brick_generator)


def ui_render(surface, dt, ball):
    # fps render
    if dt:
        fps = int(1 / dt)
    else:
        fps = 0
    font_render(surface, 40, f"fps:{fps}", white, (60, 20))

    # score render
    font_render(surface, 40, f"score:{SCORE}", white, (60, surface.get_height() - 20))
    font_render(
        surface,
        40,
        f"Ball in {int(ball.x)},{int(ball.y)}",
        white,
        (surface.get_width() - 120, 20),
    )


def font_render(surface, size, text, color, position):
    try:
        font = pg.font.Font("fonts/CutePixel.ttf", size)
    except FileNotFoundError:
        print("Fonts file not found!")
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
        (surface.get_width() - 240, surface.get_height() - 20),
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


def cheat_mode(brick_generator):
    global GAME_STATUS
    if GAME_STATUS == "LOSE":
        return
    for brick in brick_generator.brick_array:
        brick_generator.destory(brick)
    GAME_STATUS = "WIN"


def main():
    pg.init()
    game_init()

    global FIRST_RUN
    # right declare
    if FIRST_RUN:
        print("Font: Cute Pixel\nSource: fontmeme.com/ziti/cute-pixel-font")
        FIRST_RUN = False

    screen = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption("Breakout")
    start = time.time()
    # entitys
    paddle = Paddle(screen.get_width() / 2, screen.get_height() - 100, 100, 20)
    ball = Ball(screen.get_width() / 2 - 150, screen.get_height() / 2)
    brick_generator = Brick_generator((10, WIDTH), (40, 200), 10, 30)

    clock = pg.time.Clock()
    dt = 0

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYDOWN and e.key == pg.K_F3:
                global DEBUG_MODE
                if DEBUG_MODE:
                    DEBUG_MODE = False
                else:
                    DEBUG_MODE = True

        input_handler(paddle, dt, brick_generator)

        if GAME_STATUS == "PAUSE":
            pause_page(screen)
            # continue
            pass

        if GAME_STATUS == "EXIT":
            running = False

        if GAME_STATUS == "PLAYING":
            playing_time = time.time() - start
            pg.display.set_caption(f"play Breakout {playing_time:.2f}s")

            screen.fill(BACKGROUND_COLOR)

            ui_render(screen, dt, ball)
            if GAME_STATUS == "PLAYING":
                ball.move(dt)

            # collider
            if ball.hit_box.colliderect(paddle.hit_box):
                ball.rebound(paddle, "up")

            for brick in brick_generator.brick_array:
                if ball.hit_box.colliderect(brick.hit_box):
                    ball.rebound(brick, "no")

                    brick_generator.destory(brick)

            paddle.draw(screen)
            ball.draw(screen)
            brick_generator.draw(screen)

        dt = clock.tick(240) / 1000

        if GAME_STATUS == "PLAYING":
            pg.display.update()
        elif GAME_STATUS == "LOSE":
            dead_page(screen)
        elif GAME_STATUS == "WIN":
            win_page(screen)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
