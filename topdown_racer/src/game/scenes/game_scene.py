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
        # achievement sound (optional)
        self.achievement_sound = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.achievement_sound = pygame.mixer.Sound("topdown_racer/assets/sounds/achievement.wav")
            self.achievement_sound.set_volume(0.6)
        except Exception as e:
            print("Achievement sound disabled:", e)
            self.achievement_sound = None

        # engine sound (loop during race)
        self.engine_sound = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.engine_sound = pygame.mixer.Sound("topdown_racer/assets/sounds/engine.wav")
            self.engine_sound.set_volume(0.35)
            self.engine_sound.play(loops=-1)  # loop forever
        except Exception as e:
            print("Engine sound disabled:", e)
            self.engine_sound = None

        self.score = 0
        self.milestones = [1000, 3000, 5000, 10000]
        self.milestones_shown = set()
        self.alive = True
        self.enemies = self.enemy_manager.enemies

    def stop_sounds(self):
        if self.engine_sound:
            self.engine_sound.stop()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # lazy import to avoid circular imports
            from game.scenes.gameover_scene import GameOverScene
            self.stop_sounds()
            self.next_scene = GameOverScene(self.score)

    def update(self, dt: float):
        if not self.alive:
            from game.scenes.gameover_scene import GameOverScene
            self.stop_sounds()
            self.next_scene = GameOverScene(self.score)
            return

        self.road.update(dt)
        self.player.update(dt)
        self.enemy_manager.update(dt)
        self.road.set_speed(self.enemy_manager.enemy_speed * 1.20)

        self.score += int(60 * dt)

        # === Milestones banners ===
        for m in self.milestones:
            if self.score >= m and m not in self.milestones_shown:
                self.milestones_shown.add(m)

                # default (orange)
                bg = (255, 140, 0)
                fg = (20, 20, 20)
                text = f"{m} POINTS"

                # sound for milestones 2000, 5000 and 10000
                if m in (3000, 5000, 10000):
                    if self.achievement_sound:
                        self.achievement_sound.play()

                # special GOLD + text for 10 000
                if m == 10000:
                    bg = (255, 215, 0)   # gold
                    fg = (60, 40, 0)
                    text = "LEGENDARY 10000 POINTS!"


                self.road.show_banner(
                    text,
                    bg=bg,
                    fg=fg,
                    y=-60,
                )
                break  # only one banner per frame

        self.hud.set_score(self.score)
        self.hud.set_speed(self.enemy_manager.enemy_speed)

        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.alive = False

    def draw(self, screen):
        self.road.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        self.hud.draw(screen)
