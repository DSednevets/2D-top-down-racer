import random
import pygame
from game.settings import Settings
from game.objects.enemy import Enemy


class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()

        self.spawn_timer = 0.0
        self.spawn_interval = Settings.ENEMY_SPAWN_INTERVAL

        self.enemy_speed = Settings.ENEMY_BASE_SPEED
        self.elapsed = 0.0

        road_w = Settings.ROAD_RIGHT - Settings.ROAD_LEFT
        self.lanes = [
            Settings.ROAD_LEFT + road_w * 0.25,
            Settings.ROAD_LEFT + road_w * 0.50,
            Settings.ROAD_LEFT + road_w * 0.75,
        ]

    def update(self, dt: float):
        self.elapsed += dt

        mult = Settings.speed_mult()
        base = (Settings.ENEMY_BASE_SPEED + (self.elapsed * 80 * Settings.DIFFICULTY_RAMP)) * mult
        self.enemy_speed = base

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self._spawn_enemy()

        for e in list(self.enemies):
            e.set_base_speed(self.enemy_speed * 0.70)  # враги чуть быстрее разметки
            e.update(dt)

            if e.rect.top > Settings.HEIGHT + 120:
                e.kill()

    def _spawn_enemy(self):
        enemy_type = random.choices(
            population=["compact", "sedan", "truck"],
            weights=[0.45, 0.40, 0.15],
            k=1
        )[0]

        lane_index = random.randrange(len(self.lanes))
        y = -70
        self.enemies.add(Enemy(self.lanes, lane_index, y, self.enemy_speed, enemy_type))