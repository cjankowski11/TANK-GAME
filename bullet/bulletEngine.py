from bullet.bullet import Bullet

BULLET_LONGEVITY = 5


class BulletEngine(Bullet):
    def __init__(self, position, angle, ticks_per_sec, player):
        super().__init__(position)
        self.ticks_per_sec = ticks_per_sec
        self.player = player
        self.angle = angle
        self.existence_time = 0
        self.logevity = BULLET_LONGEVITY * ticks_per_sec
        self.exists = True

    def update_exist_time(self):
        self.existence_time += 1
        if self.existence_time >= self.logevity:
            self.exists = False

    def is_existing(self):
        return self.exists