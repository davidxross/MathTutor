import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 40
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (50, 50, 50)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game speed (FPS) and Starting Speed
FPS = 10

class Worm:
    def __init__(self):
        """Initialize the worm at the center of the screen."""
        self.body = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
        ]
        self.direction = RIGHT
        self.grow_pending = False

    def move(self):
        """Move the worm in the current direction."""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Check for wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False

        # Check for self collision
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)

        if not self.grow_pending:
            self.body.pop()
        
        self.grow_pending = False
        return True

    def set_direction(self, new_direction):
        """Set the worm's direction, preventing it from reversing."""
        # Prevent reversing into itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, screen):
        """Draw the worm on the screen."""
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(
                screen,
                color,
                (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2),
            )


class Food:
    def __init__(self):
        """Initialize food at a random location."""
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.isbad = False

    def draw(self, screen):
        """Draw the food on the screen."""
        pygame.draw.rect(
            screen,
            RED,
            (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2),
        )

    def get_position(self):
        """Return the food's grid position."""
        return (self.x, self.y)

    def respawn(self):
         """Respawn food at a new random location."""
         self.x = random.randint(0, GRID_WIDTH - 1)
         self.y = random.randint(0, GRID_HEIGHT - 1)
         self.isbad = False

    def bad_apple(self):
        """Apple that kills the worm immediately."""
        self.x = random.randint(GRID_WIDTH / 4, GRID_HEIGHT / 0.75)
        self.y = random.randint(GRID_WIDTH / 4, GRID_HEIGHT / 0.75)
        self.isbad = True


class Game:
    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Worm Game")
        self.clock = pygame.time.Clock()
        self.worm = Worm()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.fps = 0
        

    def handle_events(self):
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.worm.set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.worm.set_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.worm.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.worm.set_direction(RIGHT)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.__init__()  # Restart game

        return True

    def update(self):
        if self.game_over:
            return False

        # Move worm
        if not self.worm.move():
            self.game_over = True
    

        # Check if worm ate food
        if self.worm.body[0] == self.food.get_position():
            if self.food.isbad:
                self.game_over = True
                return
            else:
                self.worm.grow_pending = True
                if random.randint(0,10) > 8:  # 20% chance of bad apple
                    self.food.bad_apple()
                else:
                    self.food.respawn()
                self.score += 1
                self.fps += random.randint(0,1)  # Increase speed

    def draw(self):
        """Draw everything on screen."""
        self.screen.fill(BLACK)

        # Draw grid
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)

        # Draw game objects
        self.worm.draw(self.screen)
        self.food.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press SPACE to restart", True, RED)
            text_rect = game_over_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS + (self.fps/3))

        pygame.quit()
        sys.exit()



game = Game()
game.run()
