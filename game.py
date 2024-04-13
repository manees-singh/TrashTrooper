import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1500,1500
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
    def __init__(self, x, y, teacher_present=False):
        super().__init__()
        self.image = pygame.Surface((ROOM_SIZE, ROOM_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.teacher_present = teacher_present

    def draw_teacher(self):
        if self.teacher_present:
            screen.blit(teacher_image, (self.rect.x - camera.x + ROOM_SIZE // 2 - PLAYER_SIZE // 2, self.rect.y - camera.y + ROOM_SIZE // 2 - PLAYER_SIZE // 2))

# Create rooms
rooms = pygame.sprite.Group()
for i in range(5):
    for j in range(5):
        if (i, j) == (2, 2):  # Room with teacher
            room = Room((ROOM_SIZE + ROOM_MARGIN) * i, (ROOM_SIZE + ROOM_MARGIN) * j, teacher_present=True)
        else:
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
            room.draw_teacher()

    # Check if the player is in the room with the teacher
    player_room = pygame.sprite.spritecollideany(player, rooms)
    if player_room and player_room.teacher_present:
        # Display message
        font = pygame.font.Font(None, 36)
        text = font.render("Hello everyone!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    # Draw player
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
