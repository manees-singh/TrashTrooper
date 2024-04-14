#Import modules
import pygame
import sys
import random

#Initialize Pygame
pygame.init()
pygame.mixer.init()

#Get sound files
strike_sound=pygame.mixer.Sound('collect.wav')
game_over_sound=pygame.mixer.Sound("game_over.wav")
background_sound=pygame.mixer.Sound("background.mp3")
start_menu_sound=pygame.mixer.Sound("startmenu.wav")
victory_sound=pygame.mixer.Sound("victory.wav")

#Set volumes for sound files
background_sound.set_volume(0.8)
strike_sound.set_volume(0.8)
game_over_sound.set_volume(0.3)

# Play the first song on channel 1
channel1 = pygame.mixer.Channel(1)


# Play the second song on channel 2
channel2 = pygame.mixer.Channel(2)

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

#Define HealthBar class
class HealthBar():
    def __init__(self, x, y, w,h, max_h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.height = 20
        self.max_h=max_h

    #Draw player's health bar
    def draw(self,surface):
        ratio= self.h/self.max_h
        pygame.draw.rect(surface, "red",(self.x, self.y, self.w, self.height))
        pygame.draw.rect(surface,"green",(self.x, self.y, self.w * ratio, self.height))

    #Increase player's health
    def increase_health(self):
        #Player's health cannot exceed the maximum health
        if self.h + 10 >= self.max_h:
            self.h = self.max_h
        else:
            self.h = self.h + 10

    #Decrease player's health
    def decrease_health(self):
        if self.h - 1 <= 0:
            self.h = 0
        else:
            self.h -= 1

#Define GreyRectangle class (trash bag objects)
class GreyRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('trash_pickup3.png').convert_alpha()  # Adjust size as needed
        self.image = pygame.transform.scale(self.original_image, (70, 70))  # Scale down the image
        self.rect = self.image.get_rect(topleft=(x, y))

#Define Monster class
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.original_image = pygame.image.load('the_trash_monster.jpg').convert_alpha()  # Adjust size as needed
        self.image = pygame.transform.scale(self.original_image, (70, 70))  # Scale down the image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.player = player
        self.health = 150
        self.max_health = 150
        self.speed = 4
        self.is_alive = True

    #Set monster's health bar
    def draw_health_bar(self,camera_offset_x,camera_offset_y):
        #Calculate health bar dimensions
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        bar_width_current = int(bar_width * health_ratio)

        #Create health bar surface
        health_bar_surface = pygame.Surface((bar_width, bar_height))
        health_bar_surface.fill(RED)
        health_bar_surface.fill(GREEN, (0, 0, bar_width_current, bar_height))

        #Position health bar above the monster
        health_bar_rect = health_bar_surface.get_rect(center=(self.rect.centerx - camera_offset_x, self.rect.top-8 - camera_offset_y))

        #Add health bar to screen if monster is alive
        if self.is_alive:
            health_bar_surface = pygame.Surface((bar_width, bar_height))
            health_bar_surface.fill(RED)
            health_bar_surface.fill(GREEN, (0, 0, bar_width_current, bar_height))
        #Add invisible health bar to sceen if monster is killed
        else:
            health_bar_surface = pygame.Surface((bar_width, bar_height))
            health_bar_surface.fill(WHITE)
            health_bar_surface.fill(WHITE, (0, 0, bar_width_current, bar_height))
        # Return the health bar surface and rectangle
        return health_bar_surface, health_bar_rect

    #Update monster's properties
    def update(self):
        #Kill monster if its health is reduced to 0
        if self.health <= 0:
            self.kill()
            self.is_alive = False
            self.image.fill(WHITE)
            return
        #Calculate distance to player
        distance_to_player = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        if distance_to_player.length() < 400:  # Adjust this threshold as needed
            #Move towards player
            if distance_to_player.length() == 0:
                dx = 0
                dy = 0
            else:
                dx = distance_to_player.x / distance_to_player.length() * self.speed
                dy = distance_to_player.y / distance_to_player.length() * self.speed
                self.rect.x += dx
                self.rect.y += dy
        else:
            #Move randomly
            if random.randint(1,9) == 1:
                self.rect.x += random.randint(-self.speed*2, self.speed*2)
                self.rect.y += random.randint(-self.speed*2, self.speed*2)

#Define Player class  
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('player.png').convert_alpha()  # Adjust size as needed
        self.image = pygame.transform.scale(self.original_image, (100, 70))  # Scale down the image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = None
        self.enemy_list = []

    #Update the player's position
    def update(self, dx, dy):
        #Move player
        new_rect = self.rect.move(dx, dy)

        #Update player position if no collisions
        self.rect = new_rect

    #Attack the trash monsters
    def attack(self):
        if self.hitbox.rect.colliderect(self.enemy_list[0].rect):
            self.enemy_list[0].health -= 5
        elif self.hitbox.rect.colliderect(self.enemy_list[1].rect):
            self.enemy_list[1].health -= 5
        elif self.hitbox.rect.colliderect(self.enemy_list[2].rect):
            self.enemy_list[2].health -= 5

#Define AttackHitbox class
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

    #Update the position of the hitbox
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

    #Change button color to magenta when mouse hovers over button
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
    #Create a group for the trash objects
    grey_rectangles = pygame.sprite.Group()

    #Generate trash objects
    for i in range(5):
        for j in range(5):
            x = i * (ROOM_SIZE + ROOM_MARGIN)
            y = j * (ROOM_SIZE + ROOM_MARGIN)
            # Create trash objects and add them to the trash objects group
            grey_rect = GreyRectangle(random.randint(x, x + ROOM_SIZE), random.randint(y, y + ROOM_SIZE))
            grey_rectangles.add(grey_rect)

    #Generate trash objects
    for i in range(1,3):
        for j in range(1,3):
            x = i * (ROOM_SIZE + ROOM_MARGIN)
            y = j * (ROOM_SIZE + ROOM_MARGIN)
            
            #Create trash objects and add them to the trash objects group
            grey_rect = GreyRectangle(random.randint(x, x + ROOM_SIZE), random.randint(y, y + ROOM_SIZE))
            grey_rectangles.add(grey_rect)
            
    #Create the player and add it to the sprites group
    player = Player(WIDTH // 2, HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    #Create an attack hitbox object and add it to the sprites group
    attack_hitbox = AttackHitbox(player)
    all_sprites.add(attack_hitbox)

    #Create monster objects
    monster = Monster(WIDTH // 3, HEIGHT // 3, player)
    monster2 = Monster(0, 0,player)
    monster3 = Monster(WIDTH // 4, HEIGHT, player)

    #Store the three monster objects in the player's enemy list
    player.enemy_list = [monster, monster2, monster3]

    #Add monsters to the sprites group
    all_sprites.add(monster)
    all_sprites.add(monster2)
    all_sprites.add(monster3)

    #added healthbar
    health = HealthBar(50, 50, 300, 10, 300)
    timer = pygame.time.get_ticks() #initial timer
    
    # Main loop
    running = True
    while running:
        #Play the background sound
        background_sound.play()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Check for collisions with trash objects
        collided_grey_rectangles = pygame.sprite.spritecollide(player, grey_rectangles, True)
        for grey_rect in collided_grey_rectangles:
            # Remove trash object from the group
            grey_rectangles.remove(grey_rect)
            health.increase_health()
            channel2.play(strike_sound)

        #Go to victory menu if all trash objects have been removed
        if len(grey_rectangles) == 0:
            victory_menu()
            
        #Get key presses
        keys = pygame.key.get_pressed()

        #WASD and arrow keys move the player
        dx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])) * PLAYER_SPEED
        dy = ((keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])) * PLAYER_SPEED

        #Escape key loads the pause menu
        if keys[pygame.K_ESCAPE]:
            pause_menu()

        #Space key causes the player to attack the trash monsters
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


        #Add trash objects to the screen
        for grey_rect in grey_rectangles:
            grey_rect_rect = grey_rect.rect.move(-camera_offset_x, -camera_offset_y)
            if screen.get_rect().colliderect(grey_rect_rect):
                screen.blit(grey_rect.image, grey_rect_rect)      

        #Get the player object rectangle
        player_rect = player.rect.move(-camera_offset_x, -camera_offset_y)

        #Add player object to the screen
        if screen.get_rect().colliderect(player_rect):
            screen.blit(player.image, player_rect)

        #Add monster objects to the screen
        monster_rect = monster.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect):
            screen.blit(monster.image, monster_rect)
        monster_rect2 = monster2.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect2):
            screen.blit(monster2.image, monster_rect2)
        monster_rect3 = monster3.rect.move(-camera_offset_x, -camera_offset_y)
        if screen.get_rect().colliderect(monster_rect3):
            screen.blit(monster3.image, monster_rect3)


        # Draw the monster health bars
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

        #Get current time
        current_time = pygame.time.get_ticks()
        time_interval = 10000  # Interval in milliseconds (2 seconds)

        #Add a new trash object to the screen every 10 seconds
        i = random.randint(1,2)
        j = random.randint(1,2)
        x = i*(ROOM_SIZE + ROOM_MARGIN)
        y = j * (ROOM_SIZE + ROOM_MARGIN)
        if current_time - timer >= time_interval:
            # Add a new trash object
            new_grey_rect = GreyRectangle(x,y)
            grey_rectangles.add(new_grey_rect)
            timer = current_time  # Update the timer

        # Cap the frame rate
        pygame.time.Clock().tick(60)

def game_over():
    #Play victory music and stop other music
    background_sound.stop()
    game_over_sound.play()

    #Run menu loop until a button is clicked
    running = True
    while running:
        #Set black background
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

#Create the victory menu
def victory_menu():
    #Play victory music and stop other music
    background_sound.stop()
    victory_sound.play(-1)

    #Run menu loop until a button is clicked
    running = True
    while running:
        #Set black background
        screen.fill(BLACK)
        
        #Display game over text
        font = pygame.font.Font('freesansbold.ttf', 100)
        game_over_text = font.render('You Saved the World!', True, GREEN)
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
            victory_sound.stop()
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
    start_menu_sound.play()
    
    #Set the background surface
    background = pygame.Surface(window)

    #Run menu loop until a button is clicked
    running = True
    while True:
        #Set black background
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
            start_menu_sound.stop()
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

    #Run menu loop until a button is clicked
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
