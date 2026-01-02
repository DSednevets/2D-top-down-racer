import pygame
from game.scenes.base_scene import BaseScene
from game.objects.player import Player
from game.objects.road import Road
from game.objects.hud import HUD
from game.systems.enemy_manager import EnemyManager


class GameScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.road = Road()
        self.player = Player()
        self.enemy_manager = EnemyManager()
        self.hud = HUD()

        self.score = 0
        self.milestone_1000_shown = False
        self.alive = True
        self.enemies = self.enemy_manager.enemies

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # lazy import to avoid circular imports
            from game.scenes.gameover_scene import GameOverScene
            self.next_scene = GameOverScene(self.score)

    def update(self, dt: float):
        if not self.alive:
            from game.scenes.gameover_scene import GameOverScene
            self.next_scene = GameOverScene(self.score)
            return

        self.road.update(dt)
        self.player.update(dt)
        self.enemy_manager.update(dt)

        self.score += int(60 * dt)
        if (not self.milestone_1000_shown) and self.score >= 1000:
            self.milestone_1000_shown = True
            # orange banner like START
            self.road.show_banner("1000 POINTS", bg=(255, 140, 0), fg=(20, 20, 20), y=-60)
        self.hud.set_score(self.score)
        self.hud.set_speed(self.enemy_manager.enemy_speed)

        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.alive = False

    def draw(self, screen):
        self.road.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.hud.draw(screen)
