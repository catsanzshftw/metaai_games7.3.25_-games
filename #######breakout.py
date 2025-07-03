import pygame
import numpy as np

# Window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class BreakoutGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.paddle_width = 100
        self.paddle_height = 20
        self.paddle_x = WINDOW_WIDTH / 2 - self.paddle_width / 2
        self.paddle_y = WINDOW_HEIGHT - self.paddle_height - 20

        self.ball_radius = 10
        self.ball_x = WINDOW_WIDTH / 2
        self.ball_y = WINDOW_HEIGHT / 2
        self.ball_vx = 0
        self.ball_vy = 0
        self.ball_launched = False

        self.bricks = []
        self.brick_width = 80
        self.brick_height = 30
        self.brick_rows = 5
        self.brick_cols = 10
        self.brick_gap = 10
        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                x = col * (self.brick_width + self.brick_gap)
                y = row * (self.brick_height + self.brick_gap) + 50
                self.bricks.append((x, y))

        self.score = 0
        self.lives = 3

    def generate_sound(self, freq, duration):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        note = np.sin(freq * t * 2 * np.pi)
        audio = note * (32767 / np.max(np.abs(note)))
        audio = audio.astype(np.int16)
        pygame.mixer.Sound(buffer=audio).play()

    def draw_paddle(self):
        pygame.draw.rect(self.window, WHITE, (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))

    def draw_ball(self):
        pygame.draw.circle(self.window, WHITE, (int(self.ball_x), int(self.ball_y)), self.ball_radius)

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.window, RED, (brick[0], brick[1], self.brick_width, self.brick_height))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                self.paddle_x = pygame.mouse.get_pos()[0] - self.paddle_width / 2
                if self.paddle_x < 0:
                    self.paddle_x = 0
                elif self.paddle_x > WINDOW_WIDTH - self.paddle_width:
                    self.paddle_x = WINDOW_WIDTH - self.paddle_width
                if not self.ball_launched:
                    self.ball_x = self.paddle_x + self.paddle_width / 2
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.ball_launched:
                self.ball_launched = True
                self.ball_vx = 5
                self.ball_vy = -5
                self.generate_sound(523, 0.1)

    def update_ball(self):
        if self.ball_launched:
            self.ball_x += self.ball_vx
            self.ball_y += self.ball_vy

            if self.ball_x < self.ball_radius or self.ball_x > WINDOW_WIDTH - self.ball_radius:
                self.ball_vx *= -1
                self.generate_sound(659, 0.1)
            if self.ball_y < self.ball_radius:
                self.ball_vy *= -1
                self.generate_sound(659, 0.1)

            if (self.ball_y + self.ball_radius > self.paddle_y and
                    self.ball_x > self.paddle_x and
                    self.ball_x < self.paddle_x + self.paddle_width):
                self.ball_vy *= -1
                self.generate_sound(784, 0.1)

            for brick in self.bricks[:]:
                if (self.ball_y - self.ball_radius < brick[1] + self.brick_height and
                        self.ball_y + self.ball_radius > brick[1] and
                        self.ball_x > brick[0] and
                        self.ball_x < brick[0] + self.brick_width):
                    self.bricks.remove(brick)
                    self.ball_vy *= -1
                    self.score += 1
                    self.generate_sound(1047, 0.1)

            if self.ball_y > WINDOW_HEIGHT:
                self.lives -= 1
                self.ball_launched = False
                self.ball_x = self.paddle_x + self.paddle_width / 2
                self.ball_y = WINDOW_HEIGHT / 2
                self.ball_vx = 0
                self.ball_vy = 0
                self.generate_sound(262, 0.1)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, WHITE)
        self.window.blit(text_surface, (x, y))

    def game_over_screen(self):
        self.window.fill((0, 0, 0))
        if self.lives == 0:
            self.draw_text("Game Over", WINDOW_WIDTH / 2 - 75, WINDOW_HEIGHT / 2)
        else:
            self.draw_text("You Win!", WINDOW_WIDTH / 2 - 75, WINDOW_HEIGHT / 2)
        self.draw_text(f"Score: {self.score}", WINDOW_WIDTH / 2 - 75, WINDOW_HEIGHT / 2 + 50)
        pygame.display.update()
        pygame.time.wait(2000)

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update_ball()

            self.window.fill((0, 0, 0))
            self.draw_paddle()
            self.draw_ball()
            self.draw_bricks()
            self.draw_text(f"Score: {self.score}", 10, 10)
            self.draw_text(f"Lives: {self.lives}", 10, 50)

            if self.lives == 0 or len(self.bricks) == 0:
                running = False
                self.game_over_screen()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    pygame.mixer.init()
    game = BreakoutGame()
    game.run()
