import pygame
import math

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up display variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up game variables
clock = pygame.time.Clock()
FPS = 60

# Define player properties
PLAYER_SIZE = 50
player_pos = [100, 100]
player_vel = [0, 0]
player_on_ground = False
player_powerup = None
player_lives = 3
player_coins = 0
player_score = 0

# Define level data
levels = [
    # World 1-1
    {
        "platforms": [
            {"x": 0, "y": 550, "w": 800, "h": 50},
            {"x": 200, "y": 450, "w": 200, "h": 50},
            {"x": 500, "y": 350, "w": 200, "h": 50},
        ],
        "enemies": [
            {"x": 250, "y": 500, "type": "goomba"},
            {"x": 550, "y": 400, "type": "goomba"},
        ],
        "coins": [
            {"x": 220, "y": 420},
            {"x": 520, "y": 320},
        ],
        "pipes": [
            {"x": 300, "y": 500, "w": 50, "h": 50},
        ],
    },
    # Add more levels here...
]

# Define sound effects
def generate_sound(frequency, duration):
    sample_rate = 44100
    t = pygame.np.linspace(0, duration, int(sample_rate * duration), False)
    note = pygame.np.sin(frequency * t * 2 * pygame.np.pi)
    audio = note * (32767 / pygame.np.max(pygame.np.abs(note)))
    audio = audio.astype(pygame.np.int16)
    return audio

def play_sound(sound):
    pygame.mixer.Sound(buffer=sound).play()

# Game loop
current_level = 0
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_SPACE or event.key == pygame.K_w:
                if player_on_ground:
                    player_vel[1] = -20
                    player_on_ground = False
                    play_sound(generate_sound(523.25, 0.1))

    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_vel[0] = -5
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_vel[0] = 5
    else:
        player_vel[0] = 0

    # Update player position
    player_pos[0] += player_vel[0]
    player_pos[1] += player_vel[1]
    player_vel[1] += 1

    # Collision detection
    for platform in levels[current_level]["platforms"]:
        if (player_pos[0] + PLAYER_SIZE > platform["x"] and
            player_pos[0] < platform["x"] + platform["w"] and
            player_pos[1] + PLAYER_SIZE > platform["y"] and
            player_pos[1] < platform["y"] + platform["h"]):
            player_pos[1] = platform["y"] - PLAYER_SIZE
            player_on_ground = True
            player_vel[1] = 0

    # Draw everything
    screen.fill((0, 0, 0))
    for platform in levels[current_level]["platforms"]:
        pygame.draw.rect(screen, WHITE, (platform["x"], platform["y"], platform["w"], platform["h"]))
    for enemy in levels[current_level]["enemies"]:
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], 50, 50))
    for coin in levels[current_level]["coins"]:
        pygame.draw.circle(screen, GREEN, (coin["x"], coin["y"]), 10)
    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
