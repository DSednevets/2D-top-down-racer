import pygame
from game.settings import Settings


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 54), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (40, 200, 255), (0, 0, 32, 54), border_radius=6)
        pygame.draw.rect(self.image, (15, 15, 15), (6, 8, 20, 18), border_radius=4)

        self.rect = self.image.get_rect(midbottom=(Settings.WIDTH // 2, Settings.HEIGHT - 30))

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        dx = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= Settings.PLAYER_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += Settings.PLAYER_SPEED * dt

        self.rect.x += int(dx)

        # clamp to road
        if self.rect.left < Settings.ROAD_LEFT + 6:
            self.rect.left = Settings.ROAD_LEFT + 6
        if self.rect.right > Settings.ROAD_RIGHT - 6:
            self.rect.right = Settings.ROAD_RIGHT - 6

    def draw(self, screen):
        screen.blit(self.image, self.rect)