import pygame 
import pygame_gui 

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class MapCell(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__()
        if type == "wall":
            wall = pygame.image.load("assets/wall.png")
            self.image = pygame.transform.scale(wall, (CELL_SIZE, CELL_SIZE))
        else:
            tile = pygame.image.load("assets/tile.png")
            self.image = pygame.transform.scale(tile, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

class MapGrid(pygame.sprite.Sprite):
    def __init__(self, map_grid):
        super().__init__()
        self.map_grid = map_grid
        self.image = pygame.Surface((SCREEN_HEIGHT, SCREEN_HEIGHT))
        self.image.fill((10, 20, 30))
        self.rect = self.image.get_rect(center = (SCREEN_HEIGHT // 2, (SCREEN_HEIGHT) // 2))

    def create_map(self):
        """Creates the map grid by creating MapCell sprites for each cell."""

        self.cells = pygame.sprite.Group()

        for row_index, row in enumerate(self.map_grid):
            for col_index, cell_type in enumerate(row):
                cell_x = col_index * CELL_SIZE
                cell_y = row_index * CELL_SIZE
                map_cell = MapCell(cell_type, cell_x, cell_y)
                self.cells.add(map_cell)

        # Render the cells onto the MapGrid's image
        self.cells.draw(self.image)

class TankSprite(pygame.sprite.Sprite):
    def __init__(self, surface, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(surface, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))