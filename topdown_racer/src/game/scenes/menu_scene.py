import pygame
from game.scenes.base_scene import BaseScene
from game.scenes.game_scene import GameScene
from game.settings import Settings


class MenuScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.font_big = pygame.font.SysFont(None, 56)
        self.font = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.next_scene = GameScene()

    def draw(self, screen):
        screen.fill((15, 15, 20))
        title = self.font_big.render("TOP-DOWN RACER", True, (240, 240, 240))
        hint = self.font.render("Press Enter / Space to start", True, (200, 200, 200))

        screen.blit(title, title.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 40)))
        screen.blit(hint, hint.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 30)))