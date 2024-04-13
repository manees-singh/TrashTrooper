import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pygame")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the square
square_size = 50
square_x = (screen_width - square_size) // 2
square_y = (screen_height - square_size) // 2
square_speed = 5

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Move the square based on the pressed keys
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
    if keys[pygame.K_UP]:
        square_y -= square_speed
    if keys[pygame.K_DOWN]:
        square_y += square_speed

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the square
    pygame.draw.rect(screen, BLACK, (square_x, square_y, square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Add a short delay to control the frame rate
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
sys.exit()
