"""Snake game implementation."""
import pygame
import random
import sys

# Константы которые требуют тесты
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Глобальные переменные которые требуют тесты
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
snake = None
apple = None


class GameObject:
    """Base game object class."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw object on screen."""
        pass


class Apple(GameObject):
    """Apple food for snake."""

    def __init__(self, position=(0, 0)):
        super().__init__(position, (255, 0, 0))

    def draw(self):
        """Draw apple on screen."""
        rect = (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)

    def randomize_position(self, snake_body):
        """Move apple to random position."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.position = (x, y)
            if self.position not in snake_body:
                break


class Snake(GameObject):
    """Snake player class."""

    def __init__(self, position=(GRID_WIDTH // 2, GRID_HEIGHT // 2)):
        super().__init__(position, (0, 255, 0))
        self.positions = [position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = RIGHT

    def get_head_position(self):
        """Get snake head position."""
        return self.positions[0]

    def move(self):
        """Move snake one step."""
        self.direction = self.next_direction
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        new_position = (new_x, new_y)

        if new_position in self.positions[1:]:
            self.reset()
            return False

        self.positions.insert(0, new_position)
        self.position = new_position
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        """Reset snake to initial state."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.position = self.positions[0]
        self.direction = random.choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = self.direction

    def grow(self):
        """Increase snake length."""
        self.length += 1

    def update_direction(self, direction):
        """Change snake direction."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction

    def draw(self):
        """Draw snake on screen."""
        for position in self.positions:
            rect = (position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)


def handle_keys(event):
    """Handle keyboard input."""
    if event.key == pygame.K_UP:
        snake.update_direction(UP)
    elif event.key == pygame.K_DOWN:
        snake.update_direction(DOWN)
    elif event.key == pygame.K_LEFT:
        snake.update_direction(LEFT)
    elif event.key == pygame.K_RIGHT:
        snake.update_direction(RIGHT)


def main():
    """Main game function."""
    global snake, apple
    pygame.init()
    pygame.display.set_caption("Snake Game")
    snake = Snake()
    apple = Apple((random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1)))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keys(event)
        if not snake.move():
            apple.randomize_position(snake.positions)
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
