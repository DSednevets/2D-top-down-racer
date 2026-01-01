import pygame
from game.settings import Settings


class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.score = 0
        self.speed = 0.0

    def set_score(self, score: int):
        self.score = score

    def set_speed(self, speed: float):
        self.speed = speed

    def draw(self, screen):
        text = self.font.render(f"Score: {self.score}", True, (10, 10, 10))
        text2 = self.font.render(f"Speed: {int(self.speed)}", True, (10, 10, 10))

        # simple shadow panel
        panel = pygame.Surface((Settings.WIDTH, 36), pygame.SRCALPHA)
        panel.fill((255, 255, 255, 140))
        screen.blit(panel, (0, 0))

        screen.blit(text, (10, 8))
        screen.blit(text2, (Settings.WIDTH - 120, 8))