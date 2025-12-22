import pygame as pg
import sys

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


class Paddle:
    def __init__(self, x, y):
        self.width = 100
        self.height = 20
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.color = white
        self.hit_box = pg.Rect(self.x, self.y, 100, 20)

    def draw(self, screen):
        pg.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=8,
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
            self.y = HEIGTH - self.radius
            self.speed_y = -self.speed_y

        self.hit_box.x = self.x - self.radius
        self.hit_box.y = self.y - self.radius


class Block(Paddle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.height = 10
        self.width = 10
        self.hit_box = pg.Rect(self.x, self.y, 10, 10)


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


def fps_render(surface, dt):
    if dt:
        fps = int(1 / dt)
    else:
        fps = 0
    font = pg.font.Font(None, 40)
    text = font.render(f"fps:{fps}", True, white)
    surface.blit(text, (0, 0))


def main():
    pg.init()

    screen = pg.display.set_mode((WIDTH, HEIGTH))
    pg.display.set_caption("Breakout")

    # entitys
    paddle = Paddle(screen.get_width() / 2, screen.get_height() - 100)
    ball = Ball(screen.get_width() / 2, screen.get_height() / 2)

    clock = pg.time.Clock()
    dt = 0

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                running = False

        screen.fill(BACKGROUND_COLOR)

        input_handler(paddle, dt)

        fps_render(screen, dt)

        ball.move(dt)

        # collider
        if ball.hit_box.colliderect(paddle.hit_box):
            """
            if (
                ball.y < paddle.y - paddle.height // 2
                or ball.y > paddle.y + paddle.height // 2
            ):
                ball.speed_y = -ball.speed_y
            else:
                ball.speed_x = -ball.speed_x
            """
            ball.speed_y = -ball.speed_y

        paddle.draw(screen)
        ball.draw(screen)

        dt = clock.tick(60) / 1000

        pg.display.update()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
