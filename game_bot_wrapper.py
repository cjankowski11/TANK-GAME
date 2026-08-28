from gameEngine import GameEngine
import numpy as np
NUM_OF_CLOSEST_WALLS = 5
NUM_OF_CLOSEST_BULLETS = 5


class Wrapper():
    def __init__(self, game_engine: GameEngine):
        self.game = game_engine

    def get_tank(self, player):
        return self.game.get_tank(player)

    def sorted_walls(self, player):
        tank = self.get_tank(player)
        walls = self.game.get_walls()
        sorted_walls = sorted(
            walls,
            key=lambda w: self.calculate_distance_from_wall(tank, w)
        )
        return sorted_walls
    
    def sorted_bullets(self, player):
        tank = self.get_tank(player)
        bullets = self.game.get_bullets()
        sorted_bullets = sorted(
            bullets,
            key=lambda b: self.calculate_distance_from_bullet(tank, b)
        )
        return sorted_bullets
    
    def calculate_distance_from_bullet(self, tank, bullet):
        tank_position, bullet_position = tank.get_position(), bullet.get_position()
        return ((tank_position.x - bullet_position.x)**2 +
                (tank_position.y - bullet_position.y)**2)**0.5

    def calculate_distance_from_wall(self, tank, wall):
        tank_position = tank.get_position()
        return min((tank_position.x - wall.x), (wall.x - tank_position.x),
                   (tank_position.y - wall.y), (wall.y - tank_position.y))

    def calculate_distance_from_enemy(self, tank, enemy):
        tank_position = tank.get_position()
        enemy_position = enemy.get_position()
        return ((tank_position.x - enemy_position.x)**2 +
                (tank_position.y - enemy_position.y)**2)**0.5

    def get_tank_position(self, player):
        tank = self.get_tank(player)
        return tank.get_position()

    def get_tank_angle(self, player):
        tank = self.get_tank(player)
        return tank.angle

    def get_enemies(self, player):
        player_name = player.name
        all_tanks = self.game.get_tanks()
        return [tank for tank in all_tanks if tank.player.name != player_name]

    def sorted_enemies(self, player):
        player_tank = self.get_tank(player)
        enemies = self.get_enemies(player)
        sorted_enemies = sorted(
            enemies,
            key=lambda e: self.calculate_distance_from_enemy(player_tank, e)
        )
        return sorted_enemies

    def get_obs(self, player):
        tank = self.get_tank(player)
        position = tank.position
        angle = tank.angle
        bullets_left = tank.bullets_left
        is_able_to_shoot = tank.is_able_to_shoot()
        sorted_enemies = self.sorted_enemies(player)
        enemy_positions = [(enemy.position.x-position.x,
                           enemy.position.y-position.y,
                           enemy.angle, enemy.alive)
                           for enemy in sorted_enemies]
        
        if len(enemy_positions) < 3:
            for _ in range(3 - len(enemy_positions)):
                enemy_positions.append((999, 999, 0, 0))

        sorted_bullets = self.sorted_bullets(player)
        bullets_positions = [(bullet.position.x-position.x,
                             bullet.position.y-position.y, bullet.angle)
                             for bullet in sorted_bullets]
        
        if len(bullets_positions) < 5:
            for _ in range(5 - len(bullets_positions)):
                bullets_positions.append((999, 999, 0))

        sorted_walls = self.sorted_walls(player)
        sorted_walls = [(wall.x, wall.y, wall.w, wall.h) for wall in sorted_walls]
        if len(sorted_walls) < 5:
            for _ in range(5 - len(sorted_walls)):
                sorted_walls.append((0, 0, 0, 0))

        return np.array([position.x, position.y, angle, bullets_left,
                        is_able_to_shoot] +
                        [i for enemy in enemy_positions for i in enemy] +
                        [i for bullet in bullets_positions[:5] for i in bullet] +
                        [i for wall in sorted_walls[:5] for i in wall])

    def execute_bot_action(self, player, action):
        self.game.update_player(player, w, a, s, d, shoot)
        

    def get_reward(self, player):
        pass