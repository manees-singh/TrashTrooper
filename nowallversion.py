import pygame
import sys
import random
import math

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
GREY = (128,128,128)

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
class HealthBar():
    def __init__(self, x, y, w,h, max_h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.height = 20
        self.max_h=max_h

    def draw(self,surface):
        ratio= self.h/self.max_h
        pygame.draw.rect(surface, "red",(self.x, self.y, self.w, self.height))
        pygame.draw.rect(surface,"green",(self.x, self.y, self.w * ratio, self.height))

    def increase_health(self):
        if self.h + 10 >= self.max_h:
            self.h = self.max_h
        else:
            self.h = self.h + 10

    def decrease_health(self):
        if self.h - 1 <= 0:
            self.h = 0
            # Game over logic can be added here
        else:
            self.h -= 1

class GreyRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Adjust size as needed
        self.image.fill((128, 128, 128))  # Grey color
        self.rect = self.image.get_rect(topleft=(x, y))

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE + 15, PLAYER_SIZE + 15))  # slightly bigger than player
        self.image.fill(GREY)
        self.rect = self.image.get_rect(center=(x, y))
        self.player = player
        self.health = 100
        self.max_health = 100
        self.speed = 3
        self.is_alive = True

    def draw_health_bar(self,camera_offset_x,camera_offset_y):
        # Calculate health bar dimensions
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        bar_width_current = int(bar_width * health_ratio)

        # Create health bar surface
        if self.is_alive:
            health_bar_surface = pygame.Surface((bar_width, bar_height))
            health_bar_surface.fill(RED)
            health_bar_surface.fill(GREEN, (0, 0, bar_width_current, bar_height))
        else:
            health_bar_surface = pygame.Surface((bar_width, bar_height))
            health_bar_surface.fill(WHITE)
            health_bar_surface.fill(WHITE, (0, 0, bar_width_current, bar_height))

        # Position health bar above the monster
        health_bar_rect = health_bar_surface.get_rect(center=(self.rect.centerx - camera_offset_x, self.rect.top-8 - camera_offset_y))

        # Return the health bar surface and rectangle
        return health_bar_surface, health_bar_rect
    
    def update(self):
        if self.health <= 0:
            self.kill()
            self.is_alive = False
            self.image.fill(WHITE)
            return
        
        # Calculate distance to player
        distance_to_player = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        if distance_to_player.length() < 400:  # Adjust this threshold as needed
            # Move towards player
            if distance_to_player.length() == 0:
                dx = 0
                dy = 0
            else:
                dx = distance_to_player.x / distance_to_player.length() * self.speed
                dy = distance_to_player.y / distance_to_player.length() * self.speed
                self.rect.x += dx
                self.rect.y += dy
        else:
            # Move randomly
            if random.randint(1,9) == 1:
                
                self.rect.x += random.randint(-self.speed*2, self.speed*2)
                self.rect.y += random.randint(-self.speed*2, self.speed*2)
        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = None
        self.enemy_list = []

    def update(self, dx, dy):
        # Move player
        new_rect = self.rect.move(dx, dy)

        # Update player position if no collisions
        self.rect = new_rect

    def attack(self):
        if self.hitbox.rect.colliderect(self.enemy_list[0].rect):
            self.enemy_list[0].health -= 10
        elif self.hitbox.rect.colliderect(self.enemy_list[1].rect):
            self.enemy_list[1].health -= 10
        elif self.hitbox.rect.colliderect(self.enemy_list[2].rect):
            self.enemy_list[2].health -= 10

class AttackHitbox(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.player = player
        self.follow_speed = 1/4
        self.rect.center = self.player.rect.center
        player.hitbox = self
        
    def update(self):
        self.rect.center = self.player.rect.center

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
    def __init__(self, x, y, w, h, text='START'):
        super().__init__(x, y, w, h, BLUE, text)

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


#Play the game
def play_game():
    # Create tunnels and walls
    grey_rectangles = pygame.sprite.Group()
    for i in range(5):
        for j in range(5):
            x = i * (ROOM_SIZE + ROOM_MARGIN)
            y = j * (ROOM_SIZE + ROOM_MARGIN)
            # Create grey rectangle
            grey_rect = GreyRectangle(random.randint(x, x + ROOM_SIZE), random.randint(y, y + ROOM_SIZE))
            grey_rectangles.add(grey_rect)

    for i in range(-50,50):
        for j in range(-50,50):
            x = i * (ROOM_SIZE + ROOM_MARGIN)
            y = j * (ROOM_SIZE + ROOM_MARGIN)
            # Create grey rectangle
            grey_rect = GreyRectangle(random.randint(x, x + ROOM_SIZE), random.randint(y, y + ROOM_SIZE))
            grey_rectangles.add(grey_rect)
    # Create player
    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    attack_hitbox = AttackHitbox(player)
    all_sprites.add(attack_hitbox)

    # Create monster
    monster = Monster(WIDTH // 3, HEIGHT // 3, player)
    monster2 = Monster(0, 0, player)
    monster3 = Monster(WIDTH, HEIGHT, player)

    player.enemy_list = [monster, monster2, monster3]
    
    all_sprites.add(monster)
    all_sprites.add(monster2)
    all_sprites.add(monster3)

    #added healthbar
    health = HealthBar(250, 200, 300, 10, 100)
    timer = pygame.time.get_ticks() #initial timer
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
            health.increase_health()
        # Get key presses
        keys = pygame.key.get_pressed()
        dx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])) * PLAYER_SPEED
        dy = ((keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])) * PLAYER_SPEED
        if keys[pygame.K_ESCAPE]:
            pause_menu()
        if keys[pygame.K_SPACE]:
            player.attack()

        # Check for collisions before updating player position
        player.update(dx, dy)
        attack_hitbox.update()

        # Update monster position
        monster.update()
        monster2.update()
        monster3.update()

        if player.rect.colliderect(monster.rect) and monster.is_alive:
            # Decrease player's health
            health.decrease_health()
            if health.h <= 0:
                game_over()

        if player.rect.colliderect(monster2.rect) and monster2.is_alive:
            # Decrease player's health
            health.decrease_health()
            if health.h <= 0:
                game_over()

        if player.rect.colliderect(monster3.rect) and monster3.is_alive:
            # Decrease player's health
            health.decrease_health()
            if health.h <= 0:
                game_over()
        # Calculate camera offset based on player's position
        camera_offset_x = player.rect.x - WIDTH // 2
        camera_offset_y = player.rect.y - HEIGHT // 2

        
        # Draw everything with camera offset
        screen.fill(WHITE)


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

        monster_rect2 = monster2.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect2):
            screen.blit(monster2.image, monster_rect2)

        monster_rect3 = monster3.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect3):
            screen.blit(monster3.image, monster_rect3)


        # Draw monster health bar
        health_bar_surface, health_bar_rect = monster.draw_health_bar(camera_offset_x,camera_offset_y)
        screen.blit(health_bar_surface, health_bar_rect)

        health_bar_surface2, health_bar_rect2 = monster2.draw_health_bar(camera_offset_x,camera_offset_y)
        screen.blit(health_bar_surface2, health_bar_rect2)

        health_bar_surface3, health_bar_rect3 = monster3.draw_health_bar(camera_offset_x,camera_offset_y)
        screen.blit(health_bar_surface3, health_bar_rect3)
        
        
        #add health bar
        health.draw(screen)
        # Update display
        pygame.display.flip()

        current_time = pygame.time.get_ticks()
        time_interval = 2000  # Interval in milliseconds (2 seconds)
        if current_time - timer >= time_interval:
            # Add a new grey rectangle
            new_grey_rect = GreyRectangle(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            grey_rectangles.add(new_grey_rect)
            timer = current_time  # Update the timer

        # Cap the frame rate
        pygame.time.Clock().tick(60)

def game_over():
    running = True
    while running:
        screen.fill(BLACK)
        
        #Display game over text
        font = pygame.font.Font('freesansbold.ttf', 100)
        game_over_text = font.render('GAME OVER', True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)

        #Create buttons
        retry_button = StartButton(WIDTH // 3 - 150, HEIGHT // 4 * 3 - 60, 300, 120, 'RETRY')
        quit_button = QuitButton(WIDTH // 3 * 2 - 150, HEIGHT // 4 * 3 - 60, 300, 120)

        #Draw buttons
        retry_button.draw(screen)
        quit_button.draw(screen)

        #Hover over buttons
        retry_button.hover()
        quit_button.hover()

        #Perform button actions if clicked
        if retry_button.is_clicked():
            running = False
            retry_button.action()
        if quit_button.is_clicked():
            running = False
            quit_button.action()

        #Update display
        pygame.display.flip()

        #Close the window if required
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
        text = font.render('TRASH TROOPERS', True, WHITE, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 6)
        screen.blit(text, text_rect)

        #Create buttons
        start_button = StartButton(WIDTH // 2 - 150, HEIGHT // 3 - 60, 300, 120)
        quit_button = QuitButton(WIDTH // 2 - 150, HEIGHT // 3 * 2 - 60, 300, 120)

        #Draw buttons
        start_button.draw(screen)
        quit_button.draw(screen)

        #Hover over buttons
        start_button.hover()
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
        text_rect.center = (WIDTH // 2, HEIGHT // 6)
        screen.blit(text, text_rect)

        #Create buttons
        resume_button = ResumeButton(WIDTH // 2 - 150, HEIGHT // 3 - 60, 300, 120)
        quit_button = QuitButton(WIDTH // 2 - 150, HEIGHT // 3 * 2 - 60, 300, 120)

        #Draw buttons
        resume_button.draw(screen)
        quit_button.draw(screen)

        #Hover over buttons
        resume_button.hover()
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
