import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: float):
        super().__init__()
        self.image = pygame.Surface((32, 54), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 80, 80), (0, 0, 32, 54), border_radius=6)
        pygame.draw.rect(self.image, (15, 15, 15), (6, 8, 20, 18), border_radius=4)

        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = speed

    def update(self, dt: float):
        self.rect.y += int(self.speed * dt)