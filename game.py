import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("House Visiting Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the square
square_size = 50
square_x = (screen_width - square_size) // 2
square_y = (screen_height - square_size) // 2
square_speed = 5

# Set up houses
houses = [
    {"x": 50, "y": 50, "color": RED, "visited": False},
    {"x": 300, "y": 200, "color": GREEN, "visited": False},
    {"x": 600, "y": 400, "color": BLUE, "visited": False}
]

# Environmental messages
messages = [
    {"text": "Visit all houses to win!", "x": 50, "y": 20}
]

# Scoring
score = 0

# Function to check collision between square and houses
def check_collision():
    global score
    for house in houses:
        if (square_x + square_size >= house["x"] and
            square_x <= house["x"] + 50 and
            square_y + square_size >= house["y"] and
            square_y <= house["y"] + 50):
            if not house["visited"]:
                house["visited"] = True
                score += 1

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

    # Check for collision with houses
    check_collision()

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the square
    pygame.draw.rect(screen, BLACK, (square_x, square_y, square_size, square_size))

    # Draw the houses
    for house in houses:
        if not house["visited"]:
            pygame.draw.rect(screen, house["color"], (house["x"], house["y"], 50, 50))

    # Draw environmental messages
    font = pygame.font.SysFont(None, 24)
    for message in messages:
        text = font.render(message["text"], True, BLACK)
        screen.blit(text, (message["x"], message["y"]))

    # Display the score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (50, 50))

    # Check win condition
    if score == len(houses):
        win_text = font.render("You visited all houses! You win!", True, BLACK)
        screen.blit(win_text, (250, 100))

    # Update the display
    pygame.display.flip()

    # Add a short delay to control the frame rate
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
sys.exit()
