from game.scenes.menu_scene import MenuScene
from game.settings import Settings
import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Top-Down Racer")

    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    clock = pygame.time.Clock()

    scene = MenuScene()

    running = True
    while running:
        dt = clock.tick(Settings.FPS) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene.handle_event(event)

        scene.update(dt)
        scene.draw(screen)
        pygame.display.flip()

        if scene.next_scene is not None:
            scene = scene.next_scene

    pygame.quit()


if __name__ == "__main__":
    main()