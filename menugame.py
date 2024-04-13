import pygame
import sys
import random

#Initialize Pygame
pygame.init()

# Set up the screen
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
window = (WIDTH, HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Character Movement")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

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

class GreyRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Adjust size as needed
        self.image.fill((128, 128, 128))  # Grey color
        self.rect = self.image.get_rect(topleft=(x, y))

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE + 10, PLAYER_SIZE + 10))  # slightly bigger than player
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.player = player

    def update(self):
        # Calculate direction towards player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = max(abs(dx), abs(dy))  # get the maximum absolute distance
        if distance != 0:
            dx = dx / distance
            dy = dy / distance

        # Move monster towards player
        self.rect.x += dx
        self.rect.y += dy
        
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
    def __init__(self, x, y, w, h, color, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.start_color = color
        self.color = color
        self.button_text = text
        self.font = pygame.font.Font('freesansbold.ttf', 60)
        self.text = self.font.render(text, True, WHITE, self.color)
        self.text_rect = self.text.get_rect()

    #Draw the button
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.text_rect.center = (self.x + (self.width/2), self.y + (self.height/2))
        screen.blit(self.text, self.text_rect)

    #Change button color when mouse hovers over button
    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = MAGENTA
            self.text = self.font.render(self.button_text, True, WHITE, MAGENTA)
            self.draw(screen)
        else:
            self.color = self.start_color
            self.text = self.font.render(self.button_text, True, WHITE, self.start_color)
            self.draw(screen)

    #Determine if the button is clicked
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        return self.rect.collidepoint(mouse_pos) and click[0] == 1

#Define StartButton subclass
class StartButton(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, BLUE, 'START')

    #Start the game
    def action(self):
        play_game()

#Define QuitButton subclass
class QuitButton(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, RED, 'QUIT')

    #Quit the game
    def action(self):
        quit_game()

#Define ResumeButton subclass
class ResumeButton(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, BLUE, 'RESUME')

#Define OptionButton subclass
class OptionsButton(Button):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, GREEN, 'OPTIONS')

    def action(self):
        pass

#Play the game
def play_game():
    # Create tunnels and walls
    tunnels = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    grey_rectangles = pygame.sprite.Group()
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
            # Create grey rectangle
            grey_rect = GreyRectangle(random.randint(x, x + ROOM_SIZE), random.randint(y, y + ROOM_SIZE))
            grey_rectangles.add(grey_rect)
    # Create player
    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create monster
    monster = Monster(WIDTH // 3, HEIGHT // 3, player)
    all_sprites.add(monster)
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Check for collisions with grey rectangles
        collided_grey_rectangles = pygame.sprite.spritecollide(player, grey_rectangles, True)
        for grey_rect in collided_grey_rectangles:
            # Remove grey rectangle from the group
            grey_rectangles.remove(grey_rect)
        # Get key presses
        keys = pygame.key.get_pressed()
        dx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])) * PLAYER_SPEED
        dy = ((keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])) * PLAYER_SPEED
        if keys[pygame.K_ESCAPE]:
            pause_menu()

        # Check for collisions before updating player position
        player.update(dx, dy, walls)

        # Update monster position
        monster.update()

        # Calculate camera offset based on player's position
        camera_offset_x = player.rect.x - WIDTH // 2
        camera_offset_y = player.rect.y - HEIGHT // 2


        # Draw monster
        monster_rect = monster.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect):
            screen.blit(monster.image, monster_rect)

        # Draw everything with camera offset
        screen.fill(WHITE)

        #tunnels
        for tunnel in tunnels:
            tunnel_rect = tunnel.rect.move(-camera_offset_x, -camera_offset_y)
            if screen.get_rect().colliderect(tunnel_rect):
                pygame.draw.rect(screen, WHITE, tunnel_rect)

        #walls
        for wall in walls:
            wall_rect = wall.rect.move(-camera_offset_x, -camera_offset_y)
            if screen.get_rect().colliderect(wall_rect):
                screen.blit(wall.image, wall_rect)

        #trash
        for grey_rect in grey_rectangles:  # Draw grey rectangles after walls and tunnels
            grey_rect_rect = grey_rect.rect.move(-camera_offset_x, -camera_offset_y)
            if screen.get_rect().colliderect(grey_rect_rect):
                screen.blit(grey_rect.image, grey_rect_rect)      

        player_rect = player.rect.move(-camera_offset_x, -camera_offset_y)

        #player
        if screen.get_rect().colliderect(player_rect):
            screen.blit(player.image, player_rect)

        #monster
        monster_rect = monster.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect):
            screen.blit(monster.image, monster_rect)
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
        text_rect.center = (WIDTH // 2, 50)
        screen.blit(text, text_rect)

        #Create buttons
        start_button = StartButton(WIDTH // 2 - 150, HEIGHT // 4 - 60, 300, 120)
        options_button = OptionsButton(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 120)
        quit_button = QuitButton(WIDTH // 2 - 150, HEIGHT // 4 * 3 - 60, 300, 120)

        #Draw buttons
        start_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        #Hover over buttons
        start_button.hover()
        options_button.hover()
        quit_button.hover()

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

#Create the pause menu
def pause_menu():
    #Set the background surface
    background = pygame.Surface(window)

    running = True
    while True:
        #Set background
        screen.blit(background, (0, 0))

        #Create header text
        font = pygame.font.Font('freesansbold.ttf', 100)
        text = font.render('GAME PAUSED', True, WHITE, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 50)
        screen.blit(text, text_rect)

        #Create buttons
        resume_button = ResumeButton(WIDTH // 2 - 150, HEIGHT // 4 - 60, 300, 120)
        options_button = OptionsButton(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 120)
        quit_button = QuitButton(WIDTH // 2 - 150, HEIGHT // 4 * 3 - 60, 300, 120)

        #Draw buttons
        resume_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        #Hover over buttons
        resume_button.hover()
        options_button.hover()
        quit_button.hover()

        #Perform button actions if clicked
        if resume_button.is_clicked():
            running = False
            return
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
