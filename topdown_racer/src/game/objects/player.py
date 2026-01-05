import pygame
from game.settings import Settings


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        w, h = 34, 60
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)

        # colors
        body = (12, 24, 70)       # dark blue
        stripe = (245, 245, 245)  # white
        glass = (15, 15, 15)      # dark glass
        light = (255, 245, 190)   # headlight
        tail = (255, 60, 60)      # taillight
        outline = (8, 12, 30)     # subtle outline

        # --- body silhouette (rounded, with a more "nose" front) ---
        # base rounded body
        pygame.draw.rect(self.image, body, (2, 2, w - 4, h - 4), border_radius=10)

        # nose (front) - slightly more rounded / protruding
        # front is the TOP side (smaller y)
        pygame.draw.ellipse(self.image, body, (4, 0, w - 8, 14))
        # rear (bottom) - slightly flatter
        pygame.draw.ellipse(self.image, body, (5, h - 14, w - 10, 14))

        # subtle outline to pop from the road
        pygame.draw.rect(self.image, outline, (2, 2, w - 4, h - 4), width=1, border_radius=10)

        # --- twin racing stripes ---
        stripe_w = 4
        gap = 1
        center = w // 2
        x1 = center - gap - stripe_w
        x2 = center + gap
        pygame.draw.rect(self.image, stripe, (x1, 4, stripe_w, h - 8), border_radius=2)
        pygame.draw.rect(self.image, stripe, (x2, 4, stripe_w, h - 8), border_radius=2)

        # --- windows ---
        pygame.draw.rect(self.image, glass, (7, 14, w - 14, 18), border_radius=6)
        pygame.draw.rect(self.image, glass, (8, 36, w - 16, 10), border_radius=5)

        # --- headlights (front/top) ---
        # small rounded rectangles
        pygame.draw.rect(self.image, light, (6, 3, 6, 5), border_radius=2)
        pygame.draw.rect(self.image, light, (w - 12, 3, 6, 5), border_radius=2)

        # --- taillights (rear/bottom) ---
        pygame.draw.rect(self.image, tail, (6, h - 6, 6, 2), border_radius=1)
        pygame.draw.rect(self.image, tail, (w - 12, h - 6, 6, 2), border_radius=1)

        # small bumper line
        pygame.draw.line(self.image, outline, (7, h - 3), (w - 7, h - 3), 1)

        self.rect = self.image.get_rect(midbottom=(Settings.WIDTH // 2, Settings.HEIGHT - 28))

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