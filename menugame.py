import pygame
import sys
import random

#Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
window = (WIDTH, HEIGHT)
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

#Define Button class
class Button:
    def __init__(self, x, y, w, h, color, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.font = pygame.font.Font('freesansbold.ttf', 60)
        self.text = self.font.render(text, True, WHITE, self.color)
        self.text_rect = self.text.get_rect()

    #Draw the button
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.text_rect.center = (self.x + (self.width/2), self.y + (self.height/2))
        screen.blit(self.text, self.text_rect)

    #Determine if the button is clicked
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        return self.rect.collidepoint(mouse_pos) and click[0] == 1

#Define StartButton class
class StartButton(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, BLUE, 'START')

    #Start the game
    def action(self):
        play_game()

#Define QuitButton class
class QuitButton(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, RED, 'QUIT')

    #Quit the game
    def action(self):
        quit_game()

def play_game():
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
        if keys[pygame.K_ESCAPE]:
            quit_game()

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

#Quit the game
def quit_game():
    pygame.quit()
    sys.exit()

#Create the start menu
def start_menu():
    #Set the background surface
    background = pygame.Surface(window)

    running = True
    while True:
        #Set background
        screen.blit(background, (0, 0))

        #Create header text
        font = pygame.font.Font('freesansbold.ttf', 100)
        text = font.render('OUR EPIC GAME', True, WHITE, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH / 2, HEIGHT / 4)
        screen.blit(text, text_rect)

        #Create start and quit buttons
        start_button = StartButton(WIDTH / 2 - 125, HEIGHT / 2 - 50, 250, 100)
        quit_button = QuitButton(WIDTH / 2 - 125, HEIGHT / 4 * 3 - 50, 250, 100)

        #Draw start and quit buttons
        start_button.draw(screen)
        quit_button.draw(screen)

        #Perform button actions if clicked
        if start_button.is_clicked():
            running = False
            start_button.action()
        if quit_button.is_clicked():
            running = False
            quit_button.action()

        #Close the window if required
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Update the display
        pygame.display.update()

#Run the menu
start_menu()
