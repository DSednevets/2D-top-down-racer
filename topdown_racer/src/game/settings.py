class Settings:
    WIDTH = 480
    HEIGHT = 680
    FPS = 60

    ROAD_MARGIN = 70            # grass area on each side
    ROAD_LEFT = ROAD_MARGIN
    ROAD_RIGHT = WIDTH - ROAD_MARGIN

    PLAYER_SPEED = 260          # px/sec
    ENEMY_BASE_SPEED = 220      # px/sec
    ENEMY_SPAWN_INTERVAL = 0.9  # seconds

    DIFFICULTY_RAMP = 0.033      # speed increase per second

    DIFFICULTY = "normal"  # "normal" | "fast"

    @classmethod
    def speed_mult(cls) -> float:
        return 1.5 if cls.DIFFICULTY == "fast" else 1.0
