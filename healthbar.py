#Healthbar
import pygame
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class HealthBar():
    def __init__(self, x, y, w,h, max_h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.max_h=max_h

    def draw(self,surface):
        ratio= self.h/self.max_h
        pygame.draw.rect(surface, "red",(self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface,"green",(self.x, self.y, self.w * ratio, self.h))


health = HealthBar(250, 200, 300, 40, 100) 
run=True
while run:
    screen.fill("indigo")
    health.h=20
    health.draw(screen)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run= False

    pygame.display.flip()




pygame.quit()