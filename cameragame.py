import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Character Movement")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define constants
PLAYER_SIZE = 20
ROOM_SIZE = 200
ROOM_MARGIN = 50
PLAYER_SPEED = 5

# Load images
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_image.fill(RED)

teacher_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
teacher_image.fill(BLUE)

wall_image = pygame.Surface((ROOM_SIZE, ROOM_SIZE))
wall_image.fill(BLACK)

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dx, dy, walls):
        # Move player
        new_rect = self.rect.move(dx, dy)

        # Check for collisions with walls
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                if dx > 0:
                    new_rect.right = wall.rect.left
                elif dx < 0:
                    new_rect.left = wall.rect.right
                elif dy > 0:
                    new_rect.bottom = wall.rect.top
                elif dy < 0:
                    new_rect.top = wall.rect.bottom

        # Update player position if no collisions
        self.rect = new_rect

# Define Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_image
        self.rect = self.image.get_rect(topleft=(x, y))

# Define Tunnel class
class Tunnel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, ROOM_SIZE, ROOM_SIZE)

# Create tunnels and walls
tunnels = pygame.sprite.Group()
walls = pygame.sprite.Group()
for i in range(5):
    for j in range(5):
        x = i * (ROOM_SIZE + ROOM_MARGIN)
        y = j * (ROOM_SIZE + ROOM_MARGIN)
        if random.random() < 0.6:  # Create tunnel
            tunnel = Tunnel(x, y)
            tunnels.add(tunnel)
        else:  # Create wall
            wall = Wall(x, y)
            walls.add(wall)

# Create player
player = Player(WIDTH // 2, HEIGHT // 2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
    dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * PLAYER_SPEED

    # Check for collisions before updating player position
    player.update(dx, dy, walls)

    # Calculate camera offset based on player's position
    camera_offset_x = max(min(player.rect.x - WIDTH // 2, ROOM_SIZE * 5 - WIDTH), 0)
    camera_offset_y = max(min(player.rect.y - HEIGHT // 2, ROOM_SIZE * 5 - HEIGHT), 0)

    # Draw everything with camera offset
    screen.fill(WHITE)
    for tunnel in tunnels:
        tunnel_rect = tunnel.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(tunnel_rect):
            pygame.draw.rect(screen, WHITE, tunnel_rect)
    for wall in walls:
        wall_rect = wall.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(wall_rect):
            screen.blit(wall.image, wall_rect)
    player_rect = player.rect.move(-camera_offset_x, -camera_offset_y)
    if screen.get_rect().colliderect(player_rect):
        screen.blit(player.image, player_rect)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
