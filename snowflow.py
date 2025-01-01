import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 50)

# Font settings
FONT_SIZE = 72
FONT_COLOR = WHITE
font = pygame.font.SysFont('comicsansms', FONT_SIZE)  # Using a default Pygame font

# Load Christmas tree image
tree_image = pygame.image.load("christmas_tree.png")  # Make sure to have a Christmas tree image file
tree_image = pygame.transform.scale(tree_image, (100, 150))  # Resize the tree image

# Load Santa Claus image and sound
santa_image = pygame.image.load("santa_claus.png")  # Make sure to have a Santa Claus image file
santa_image = pygame.transform.scale(santa_image, (150, 100))  # Resize the Santa image
santa_sound = pygame.mixer.Sound("santa_claus_sound.mp3")  # Make sure to have a Santa Claus sound file

class SnowCrystal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(3, 8)  # Larger to show structure
        self.speed = random.uniform(0.5, 2)
        self.drift = random.uniform(-0.3, 0.3)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def draw_snowflake_branch(self, screen, length, rotation):
        # Calculate branch endpoints
        end_x = self.x + length * math.cos(math.radians(rotation))
        end_y = self.y + length * math.sin(math.radians(rotation))

        # Draw main branch
        pygame.draw.line(screen, WHITE, (self.x, self.y), (end_x, end_y), 1)

        # Add smaller side branches
        for angle_offset in [30, -30]:
            side_branch_length = length * 0.5
            side_x = self.x + side_branch_length * math.cos(math.radians(rotation + angle_offset))
            side_y = self.y + side_branch_length * math.sin(math.radians(rotation + angle_offset))
            pygame.draw.line(screen, WHITE, (self.x, self.y), (side_x, side_y), 1)

    def fall(self):
        # Move snowflake down with a slight horizontal drift
        self.y += self.speed
        self.x += self.drift
        self.rotation += self.rotation_speed

        # Reset snowflake if it goes below screen
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            self.rotation = random.uniform(0, 360)

    def draw(self, screen):
        # Draw 6 symmetrical branches to create a snowflake
        for i in range(6):
            rotation = self.rotation + (i * 60)
            self.draw_snowflake_branch(screen, self.size, rotation)

class SantaClaus:
    def __init__(self):
        self.x = WIDTH  # Start off-screen on the right
        self.y = random.randint(100, 250)  # Lower the y position
        self.speed = 2
        self.appeared = False
        self.appear_interval = 5000  # Interval in milliseconds
        self.last_appear_time = pygame.time.get_ticks()

    def move(self):
        self.x -= self.speed
        if self.x < -150:
            self.x = WIDTH
            self.y = random.randint(100, 250)
            self.appeared = False

    def draw(self, screen):
        screen.blit(santa_image, (self.x, self.y))

    def appear(self):
        current_time = pygame.time.get_ticks()
        if not self.appeared and current_time - self.last_appear_time > self.appear_interval:
            santa_sound.play()
            self.appeared = True
            self.last_appear_time = current_time

def setup_audio():
    """
    Setup audio for the snow simulation.
    Note: You'll need to replace these with actual sound file paths.
    """
    try:
        # Background music (soft winter/ambient track)
        pygame.mixer.music.load("winter_ambient.mp3")
        pygame.mixer.music.set_volume(0.3)  # Lower volume for ambient feel
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

        # Optional wind sound effect
        wind_sound = pygame.mixer.Sound("gentle_wind.wav")
        wind_sound.set_volume(0.2)
        wind_sound.play(-1)

        return wind_sound
    except Exception as e:
        print(f"Audio setup error: {e}")
        print("Make sure to have 'winter_ambient.mp3' and 'gentle_wind.wav' in the same directory")
        return None

def main():
    global WIDTH, HEIGHT

    # Create the screen with resizable flag
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Wintery Snowfall Simulation")

    # Setup audio
    wind_sound = setup_audio()

    # Create snowflakes
    num_snowflakes = 100
    snowflakes = [SnowCrystal(random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
                  for _ in range(num_snowflakes)]

    # Create Santa Claus
    santa = SantaClaus()

    # Clock to control frame rate
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Pause/Unpause music with spacebar
                if event.key == pygame.K_SPACE:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        # Fill screen with dark blue background
        screen.fill(DARK_BLUE)

        # Render "Merry Christmas" text
        text_surface = font.render("Merry Christmas", True, FONT_COLOR)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 10))

        # Draw Christmas trees in the background
        for i in range(0, WIDTH, 150):
            screen.blit(tree_image, (i, HEIGHT - tree_image.get_height()))

        # Update and draw snowflakes
        for snowflake in snowflakes:
            snowflake.fall()
            snowflake.draw(screen)

        # Move and draw Santa Claus
        santa.move()
        santa.draw(screen)
        santa.appear()

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    # Clean up
    pygame.mixer.music.stop()
    if wind_sound:
        wind_sound.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()