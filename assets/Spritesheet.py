import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.spriteSheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, width, height) -> pygame.Surface:
        sprite = pygame.Surface((width, height))
        sprite.blit(self.spriteSheet, (0,0), (x, y, width, height))

        return sprite