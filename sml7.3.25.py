import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game Boy palette
GB_PALETTE = [(255, 255, 255), (170, 170, 170), (85, 85, 85), (0, 0, 0)]

# Sound effects
def generate_jump_sound():
    sample_rate = 44100
    frequency = 523.25
    duration = 0.5
    samples = int(sample_rate * duration)
    sound = np.sin(2 * np.pi * np.arange(samples) * frequency / sample_rate).astype(np.float32)
    return sound

def generate_coin_sound():
    sample_rate = 44100
    frequency = 659.25
    duration = 0.2
    samples = int(sample_rate * duration)
    sound = np.sin(2 * np.pi * np.arange(samples) * frequency / sample_rate).astype(np.float32)
    return sound

def generate_enemy_stomp_sound():
    sample_rate = 44100
    frequency = 392.00
    duration = 0.3
    samples = int(sample_rate * duration)
    sound = np.sin(2 * np.pi * np.arange(samples) * frequency / sample_rate).astype(np.float32)
    return sound

# Levels
levels = [
    {
        "platforms": [(100, 500, 200, 20), (400, 400, 150, 20)],
        "enemies": [(200, 450, 20, 20)],
        "coins": [(250, 350, 10, 10)],
        "pipes": [(500, 450, 50, 50)],
        "powerups": [(600, 300, 20, 20)],
        "end_goal": (700, 400, 20, 20)
    },
    {
        "platforms": [(100, 400, 200, 20), (400, 300, 150, 20)],
        "enemies": [(250, 350, 20, 20)],
        "coins": [(300, 250, 10, 10)],
        "pipes": [(550, 350, 50, 50)],
        "powerups": [(650, 200, 20, 20)],
        "end_goal": (750, 300, 20, 20)
    }
    # Add more levels here...
]

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = 0
        self.mario = {"x": 100, "y": 100, "width": 20, "height": 20, "velocity_x": 0, "velocity_y": 0}
        self.score = 0
        self.lives = 3
        self.powerup = None

    def draw_mario(self):
        pygame.draw.rect(self.screen, RED, (self.mario["x"], self.mario["y"], self.mario["width"], self.mario["height"]))

    def draw_enemies(self, enemies):
        for enemy in enemies:
            pygame.draw.rect(self.screen, GREEN, enemy)

    def draw_coins(self, coins):
        for coin in coins:
            pygame.draw.rect(self.screen, (255, 255, 0), coin)

    def draw_pipes(self, pipes):
        for pipe in pipes:
            pygame.draw.rect(self.screen, (0, 0, 255), pipe)

    def draw_powerups(self, powerups):
        for powerup in powerups:
            pygame.draw.rect(self.screen, (255, 0, 255), powerup)

    def draw_end_goal(self, end_goal):
        pygame.draw.rect(self.screen, (0, 255, 0), end_goal)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mario["velocity_y"] = -10

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.mario["velocity_x"] = -5
        elif keys[pygame.K_RIGHT]:
            self.mario["velocity_x"] = 5
        else:
            self.mario["velocity_x"] = 0

    def update(self):
        self.mario["x"] += self.mario["velocity_x"]
        self.mario["y"] += self.mario["velocity_y"]
        self.mario["velocity_y"] += 1

        if self.mario["y"] > HEIGHT - self.mario["height"]:
            self.mario["y"] = HEIGHT - self.mario["height"]
            self.mario["velocity_y"] = 0

    def play_sound(self, sound):
        pygame.mixer.Sound(buffer=sound).play()

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()

            self.screen.fill(WHITE)

            current_level = levels[self.level]
            self.draw_mario()
            self.draw_enemies(current_level["enemies"])
            self.draw_coins(current_level["coins"])
            self.draw_pipes(current_level["pipes"])
            self.draw_powerups(current_level["powerups"])
            self.draw_end_goal(current_level["end_goal"])

            if self.mario["x"] > current_level["end_goal"][0]:
                self.level += 1
                if self.level >= len(levels):
                    running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

game = Game()
game.play_sound(generate_jump_sound())
game.run()
