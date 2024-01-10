import random

import random

def generate_map(width, height, tile_density=0.7):
    grid = []
    for row in range(height):
        grid.append([])
        for col in range(width):
            # Initialize more tiles based on tile_density
            if random.random() < tile_density:
                grid[row].append("tile")
            else:
                grid[row].append("wall")

    # Apply smoothing rules for less rigid structures
    for _ in range(3):
        new_grid = []
        for row in range(height):
            new_grid.append([])
            for col in range(width):
                neighbors = count_neighbors(grid, row, col)
                if grid[row][col] == "tile":
                    if neighbors >= 5:  # Slightly more crowded, turn into a wall
                        new_grid[row].append("wall")
                    else:
                        new_grid[row].append("tile")
                else:  # It's a wall
                    if neighbors <= 2:  # Slightly less isolated, turn into a tile
                        new_grid[row].append("tile")
                    else:
                        new_grid[row].append("wall")
        grid = new_grid

    # Additional check to prevent inaccessible tiles
    for row in range(height):
        for col in range(width):
            if grid[row][col] == "tile":
                if count_neighbors(grid, row, col) == 8:  # All neighbors are walls
                    grid[row][col] = "wall"

    return grid


def count_neighbors(grid, row, col):
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < len(grid) and 0 <= col + j < len(grid[0]):
                if grid[row + i][col + j] == "wall":
                    neighbors += 1
    return neighbors
