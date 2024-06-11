import pygame
import random




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





#Define trashbag class (trash bag objects)
class GreyRectangle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('trash_pickup3.png')  # Adjust size as needed, .convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (70, 70))  # Scale down the image
        self.rect = self.image.get_rect(topleft=(x, y))


#healthbar to indicate the life for the components of the game
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

    #Change player's health
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

#Define Monster(antagonist)
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
class Player(pygame.sprite.Sprite):  # sprites are objects with different properties like height, width, color, etc., 
                                        #  and methods like moving right, left, up and down, jump, etc.
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('player.png')  # Adjust size as needed  , .convert_alpha()
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

