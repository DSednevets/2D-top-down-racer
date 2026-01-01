import pygame
from game.settings import Settings


class Road:
    def __init__(self):
        self.scroll = 0.0
        self.speed = 240.0  # visual road scroll speed

        # START banner state
        self.start_banner_y = 120
        self.start_banner_alive = True
        self.font = pygame.font.SysFont(None, 34)

    def update(self, dt: float):
        self.scroll += self.speed * dt
        if self.scroll > 40:
            self.scroll -= 40

        if self.start_banner_alive:
            self.start_banner_y += self.speed * dt
            if self.start_banner_y > Settings.HEIGHT + 80:
                self.start_banner_alive = False

    def draw(self, screen):
        # grass
        screen.fill((50, 160, 60))

        # road
        road_rect = pygame.Rect(
            Settings.ROAD_LEFT, 0,
            Settings.ROAD_RIGHT - Settings.ROAD_LEFT, Settings.HEIGHT
        )
        pygame.draw.rect(screen, (90, 90, 95), road_rect)

        # side lines
        pygame.draw.line(screen, (230, 230, 230), (Settings.ROAD_LEFT, 0), (Settings.ROAD_LEFT, Settings.HEIGHT), 3)
        pygame.draw.line(screen, (230, 230, 230), (Settings.ROAD_RIGHT, 0), (Settings.ROAD_RIGHT, Settings.HEIGHT), 3)

        # dashed center line
        center_x = (Settings.ROAD_LEFT + Settings.ROAD_RIGHT) // 2
        dash_h = 26
        gap = 18
        y = -int(self.scroll)
        while y < Settings.HEIGHT:
            pygame.draw.rect(screen, (240, 240, 240), pygame.Rect(center_x - 3, y, 6, dash_h))
            y += dash_h + gap

        # START banner
        if self.start_banner_alive:
            banner_h = 46
            banner_y = int(self.start_banner_y)
            banner_rect = pygame.Rect(
                Settings.ROAD_LEFT + 10,
                banner_y,
                (Settings.ROAD_RIGHT - Settings.ROAD_LEFT) - 20,
                banner_h
            )
            pygame.draw.rect(screen, (245, 245, 245), banner_rect, border_radius=6)

            text = self.font.render("START", True, (40, 40, 40))
            screen.blit(text, text.get_rect(center=banner_rect.center))
