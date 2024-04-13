import pygame
import sys

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

# Define constants
PLAYER_SIZE = 50
ROOM_SIZE = 200
ROOM_MARGIN = 50
PLAYER_SPEED = 5

# Load images
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_image.fill(RED)

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PLAYER_SIZE))

# Define Room class
class Room(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ROOM_SIZE, ROOM_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create rooms
rooms = pygame.sprite.Group()
for i in range(3):
    for j in range(3):
        room = Room((ROOM_SIZE + ROOM_MARGIN) * i, (ROOM_SIZE + ROOM_MARGIN) * j)
        rooms.add(room)

# Create player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Define camera
camera = pygame.Rect(0, 0, WIDTH, HEIGHT)

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED
    if keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED

    # Update player position
    player.update(dx, dy)

    # Adjust camera position to follow the player
    camera.center = player.rect.center

    # Draw rooms within the camera's view
    for room in rooms:
        if camera.colliderect(room.rect):
            screen.blit(room.image, (room.rect.x - camera.x, room.rect.y - camera.y))

    # Draw player
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
