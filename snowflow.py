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
    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wintery Snowfall Simulation")

    # Setup audio
    wind_sound = setup_audio()

    # Create snowflakes
    num_snowflakes = 100
    snowflakes = [SnowCrystal(random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
                  for _ in range(num_snowflakes)]

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

        # Fill screen with dark blue background
        screen.fill(DARK_BLUE)

        # Update and draw snowflakes
        for snowflake in snowflakes:
            snowflake.fall()
            snowflake.draw(screen)

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