import pygame
import random

# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (159, 226, 191)
RED = (255, 0, 0)
PINK = (255, 105, 180)

# Game settings
gravity = 0.25
initial_bird_movement = -6  # Initial movement when you press space
bird_movement = 0
bird_x = 50
bird_y = HEIGHT // 2
bird_width = 40
bird_height = 40

# Fonts
font = pygame.font.SysFont("Arial", 36)
game_over_font = pygame.font.SysFont('Impact', 48)
title_font = pygame.font.SysFont('Comic Sans MS', 72)

# Pipes
pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks()

# Create the bird
bird = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

# Load sounds
jump_sound = pygame.mixer.Sound("jump.wav")  # Load jump sound
hit_sound = pygame.mixer.Sound("hit_sound.wav")  # Load hit sound
game_over_sound = pygame.mixer.Sound("game_over.wav")  # Load game over sound
pygame.mixer.music.set_volume(0.5)  # Set background music volume

# Set volume for each sound effect
jump_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
game_over_sound.set_volume(0.5)

# Declare global variables for game state
game_over_played = False  # Initialize the global variable

# Function to draw the bird
def draw_bird():
    pygame.draw.rect(screen, PINK, bird)

# Function to create pipes
def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= pipe_velocity
    return [pipe for pipe in pipes if pipe.x > -pipe_width]

# Function to check for collisions
def check_collisions(bird, pipes):
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    return False

# Function to display game over screen
def display_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

    restart_text = font.render("Press Space to Play Again", True, RED)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

# Function to display the title screen with Start button
def display_title_screen():
    screen.fill(WHITE)

    # Title text
    title_text = title_font.render("Flappy Bird", True, PINK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # Start button text
    start_button_text = font.render("Press Space or Click to Start", True, PINK)
    screen.blit(start_button_text, (WIDTH // 2 - start_button_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()

# Function to reset the game state
def reset_game():
    global bird_y, bird_movement, last_pipe, pipes, game_over_played
    bird_y = HEIGHT // 2
    bird_movement = 0
    pipes = []  # Clear any existing pipes
    last_pipe = pygame.time.get_ticks()
    game_over_played = False  # Reset the flag so the sound can be played again

# Main game loop
def game_loop():
    global bird_y, bird_movement, last_pipe, pipes, game_over_played
    
    pipes = []  # Initialize pipes here
    clock = pygame.time.Clock()
    running = True
    game_over = False
    game_started = False  # Track if the game has started

    while running:
        if not game_started:
            # Display title screen
            display_title_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_started = True  # Start the game when space is pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_started = True  # Start the game when clicked

        if game_started:
            # Game logic
            screen.fill(WHITE)

            # Check for events during the game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not game_over:
                        bird_movement = initial_bird_movement  # Make the bird jump
                        jump_sound.play()  # Play jump sound
                    if event.key == pygame.K_SPACE and game_over:
                        # Restart the game
                        reset_game()
                        game_over = False  # Reset game over state
                        bird_movement = 0  # Reset bird movement
                        game_started = True  # Start the game again

            # Update bird position
            bird_movement += gravity
            bird_y += bird_movement
            bird.top = bird_y

            # Check for new pipes
            if not game_over and pygame.time.get_ticks() - last_pipe > pipe_frequency:
                pipes.extend(create_pipe())
                last_pipe = pygame.time.get_ticks()

            # Move and draw pipes
            pipes = move_pipes(pipes)
            for pipe in pipes:
                pygame.draw.rect(screen, BLUE, pipe)

            # Draw bird
            draw_bird()

            # Check for collisions
            if not game_over and check_collisions(bird, pipes):
                game_over = True
                hit_sound.play()  # Play hit sound

            if game_over and not game_over_played:
                game_over_sound.play()  # Play the sound only once
                game_over_played = True  # Set the flag to True

            # If game over, display game over screen
            if game_over:
                display_game_over()

            # Update the screen
            pygame.display.update()

        # Control the game speed
        clock.tick(60)

    pygame.quit()

# Start the game
game_loop()
