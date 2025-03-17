import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 60
WHITE, BLACK, GRAY, BLUE, RED = (255, 255, 255), (0, 0, 0), (200, 200, 200), (0, 0, 255), (255, 0, 0)

# Sudoku Puzzle (0 represents an empty space)
PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Copy of the puzzle to track user input
grid = [row[:] for row in PUZZLE]
selected = None

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
font = pygame.font.Font(None, 40)

# Helper Functions
def draw_grid():
    """Draws the Sudoku grid and numbers."""
    screen.fill(WHITE)

    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, 540), thickness)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (540, i * GRID_SIZE), thickness)

    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num != 0:
                text = font.render(str(num), True, BLACK)
                screen.blit(text, (col * GRID_SIZE + 20, row * GRID_SIZE + 15))

    if selected:
        pygame.draw.rect(screen, BLUE, (selected[1] * GRID_SIZE, selected[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

def is_valid(row, col, num):
    """Checks if a number can be placed in a specific position."""
    if num in grid[row]: return False  # Check row
    if num in [grid[i][col] for i in range(9)]: return False  # Check column

    box_x, box_y = col // 3 * 3, row // 3 * 3
    for i in range(3):
        for j in range(3):
            if grid[box_y + i][box_x + j] == num:
                return False
    return True

def handle_click(pos):
    """Handles mouse clicks to select a cell."""
    global selected
    x, y = pos[0] // GRID_SIZE, pos[1] // GRID_SIZE
    if PUZZLE[y][x] == 0:
        selected = (y, x)

def handle_key(num):
    """Handles keyboard input for number placement."""
    if selected and is_valid(selected[0], selected[1], num):
        grid[selected[0]][selected[1]] = num

# Game Loop
running = True
while running:
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

        elif event.type == pygame.KEYDOWN:
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                handle_key(event.key - pygame.K_0)
            elif event.key == pygame.K_BACKSPACE and selected:
                grid[selected[0]][selected[1]] = 0

    pygame.display.flip()

pygame.quit()
