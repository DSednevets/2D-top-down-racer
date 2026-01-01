import pygame
from game.scenes.base_scene import BaseScene
from game.settings import Settings


class GameOverScene(BaseScene):
    def __init__(self, score: int):
        super().__init__()
        self.score = score
        self.font_big = pygame.font.SysFont(None, 56)
        self.font = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # lazy import to avoid circular imports
                from game.scenes.game_scene import GameScene
                self.next_scene = GameScene()
            elif event.key == pygame.K_ESCAPE:
                from game.scenes.menu_scene import MenuScene
                self.next_scene = MenuScene()

    def draw(self, screen):
        screen.fill((10, 10, 12))
        t1 = self.font_big.render("GAME OVER", True, (240, 240, 240))
        t2 = self.font.render(f"Score: {self.score}", True, (220, 220, 220))
        t3 = self.font.render("Enter/Space: restart   Esc: menu", True, (180, 180, 180))

        screen.blit(t1, t1.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 60)))
        screen.blit(t2, t2.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2)))
        screen.blit(t3, t3.get_rect(center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 50)))
