import random
import pygame
from game.settings import Settings


ENEMY_TYPES = {
    # name: (w, h, body_color, window_color, speed_mult)
    "compact": (30, 50, (255, 220, 50), (20, 20, 20), 1.05),
    "sedan":   (34, 58, (255, 80, 80),  (20, 20, 20), 1.00),
    "truck":   (38, 72, (120, 210, 255),(20, 20, 20), 0.92),
}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, lane_centers: list[int], lane_index: int, y: int, base_speed: float, enemy_type: str = "sedan"):
        super().__init__()
        if enemy_type not in ENEMY_TYPES:
            enemy_type = "sedan"

        self.enemy_type = enemy_type
        w, h, body, window, speed_mult = ENEMY_TYPES[enemy_type]

        self.speed_mult = speed_mult
        self.speed = base_speed * self.speed_mult

        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, body, (0, 0, w, h), border_radius=6)
        pygame.draw.rect(self.image, window, (6, 8, w - 12, 18), border_radius=4)

        self.lane_centers = lane_centers
        self.lane_index = max(0, min(lane_index, len(lane_centers) - 1))

        self.x = float(self.lane_centers[self.lane_index])
        self.rect = self.image.get_rect(center=(int(self.x), y))

        # --- lane change (rare & predictable) ---
        self.changed_once = False
        self.changing = False
        self.target_lane_index = self.lane_index
        self.change_dir = 0  # -1 left, +1 right
        self.turn_signal_time = 0.0  # telegraph timer
        self.turn_signal_total = 1  # seconds to blink before moving
        self.lane_change_speed = 200.0  # px/sec lateral move

    def set_base_speed(self, base_speed: float):
        self.speed = base_speed * self.speed_mult

    def _maybe_start_lane_change(self, dt: float):
        if self.changed_once or self.changing:
            return

        # "Predictable zone": only consider lane change roughly mid-screen
        if not (120 <= self.rect.centery <= 360):
            return

        # Rare: ~3% chance per second (tune this number)
        if random.random() < 0.03 * dt:
            # Choose a valid direction by availability
            options = []
            if self.lane_index > 0:
                options.append(-1)
            if self.lane_index < len(self.lane_centers) - 1:
                options.append(+1)
            if not options:
                return

            self.change_dir = random.choice(options)
            self.target_lane_index = self.lane_index + self.change_dir

            # Start with blinking (telegraph), movement begins after timer ends
            self.turn_signal_time = self.turn_signal_total
            self.changing = True

    def _update_lane_change(self, dt: float):
        if not self.changing:
            return

        # First phase: turn signal (blink), no movement
        if self.turn_signal_time > 0:
            self.turn_signal_time -= dt
            return

        # Second phase: smooth lateral movement
        target_x = float(self.lane_centers[self.target_lane_index])
        if self.x < target_x:
            self.x = min(target_x, self.x + self.lane_change_speed * dt)
        elif self.x > target_x:
            self.x = max(target_x, self.x - self.lane_change_speed * dt)

        # Finish
        if abs(self.x - target_x) < 0.5:
            self.x = target_x
            self.lane_index = self.target_lane_index
            self.changing = False
            self.changed_once = True

        self.rect.centerx = int(self.x)

    def update(self, dt: float):
        # forward movement
        self.rect.y += int(self.speed * dt)

        # lane change logic
        self._maybe_start_lane_change(dt)
        self._update_lane_change(dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # draw turn signal (simple blink) while telegraphing
        if self.changing and self.turn_signal_time > 0:
            blink_on = int(self.turn_signal_time * 10) % 2 == 0
            if blink_on:
                # small indicator on left/right edge
                if self.change_dir < 0:
                    r = pygame.Rect(self.rect.left + 2, self.rect.top + 20, 6, 10)
                else:
                    r = pygame.Rect(self.rect.right - 8, self.rect.top + 20, 6, 10)
                pygame.draw.rect(screen, (255, 240, 120), r, border_radius=2)
