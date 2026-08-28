from tank.tank import Tank
from bullet.bulletEngine import BulletEngine
import math
import pygame
from player import Player


class TankEngine(Tank):
    def __init__(self, start_pos, angle, bullets, ticks_per_sec, player: Player):
        super().__init__(start_pos, angle, bullets)
        self.ticks_per_sec = ticks_per_sec
        self.max_bullets = bullets
        self.shoot_cooldown_frames = 0
        self.reload_frames_limit = 1 * ticks_per_sec
        self.reload_frames_cooldown = 0
        self.cooldown_shoot_limit = 0.5 * ticks_per_sec
        self.player = player

    def shoot(self):
        rad = math.radians(self.angle)
        barrel_length = 20
    
        bullet_x = self.position.x - math.sin(rad) * barrel_length
        bullet_y = self.position.y - math.cos(rad) * barrel_length

        spawn_pos = pygame.Vector2(bullet_x, bullet_y)
        
        bullet = BulletEngine(spawn_pos, self.angle, self.ticks_per_sec, self.player)
        self.bullets_left -= 1
        self.shoot_cooldown_frames = self.cooldown_shoot_limit
        return bullet
 
    def is_able_to_shoot(self):
        if self.bullets_left > 0 and self.shoot_cooldown_frames == 0:
            return True
        return False
    
    def reload_bullet(self):
        self.bullets_left += 1
        self.reload_frames_cooldown = self.reload_frames_limit
        
    def update_shoot_cooldown(self):
        if self.shoot_cooldown_frames > 0:
            self.shoot_cooldown_frames -= 1
    
    def update_reload_cooldown(self):
        if self.bullets_left < self.max_bullets and self.reload_frames_cooldown > 0:
            self.reload_frames_cooldown -= 1
    
    def is_able_to_reload(self):
        if self.reload_frames_cooldown == 0 and self.bullets_left < self.max_bullets:
            return True
        return False