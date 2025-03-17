import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
WHITE, BLACK, GRAY, RED = (255, 255, 255), (0, 0, 0), (128, 128, 128), (255, 0, 0)

# Tetrimino Shapes (Using 4x4 Grid Representation)
SHAPES = [
    [[1, 1, 1, 1]],  # I Shape
    [[1, 1, 1], [0, 1, 0]],  # T Shape
    [[1, 1, 0], [0, 1, 1]],  # Z Shape
    [[0, 1, 1], [1, 1, 0]],  # S Shape
    [[1, 1], [1, 1]],  # O Shape
    [[1, 1, 1], [1, 0, 0]],  # L Shape
    [[1, 1, 1], [0, 0, 1]],  # J Shape
]

# Colors for each shape
SHAPE_COLORS = [(0, 255, 255), (128, 0, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 165, 0), (0, 0, 255)]

# Game Variables
grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
score = 0

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]
        self.x, self.y = COLUMNS // 2 - len(self.shape[0]) // 2, 0

    def move(self, dx, dy):
        if not self.collision(dx, dy):
            self.x += dx
            self.y += dy

    def rotate(self):
        rotated = list(zip(*self.shape[::-1]))  # Rotate 90 degrees clockwise
        if not self.collision(0, 0, rotated):
            self.shape = rotated

    def collision(self, dx=0, dy=0, shape=None):
        shape = shape or self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.x + x + dx, self.y + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                        return True
        return False

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color
        clear_lines()
        return Tetrimino()

def clear_lines():
    global score
    full_rows = [i for i in range(ROWS) if all(grid[i][x] != BLACK for x in range(COLUMNS))]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * COLUMNS)
    score += len(full_rows) * 100  # Increase score per cleared row

# Game Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
piece = Tetrimino()
running = True
fall_time = 0

# Game Loop
while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick(30)

    if fall_time > 500:  # Move piece down every 500ms
        if piece.collision(0, 1):
            piece = piece.lock()
        else:
            piece.move(0, 1)
        fall_time = 0

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                piece.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                piece.move(1, 0)
            elif event.key == pygame.K_DOWN:
                piece.move(0, 1)
            elif event.key == pygame.K_UP:
                piece.rotate()

    # Draw Grid
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw Piece
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, GRAY, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Display Score
    font = pygame.font.Font(None, 30)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
