from gameEngine import GameEngine
NUM_OF_CLOSEST_WALLS = 5
NUM_OF_CLOSEST_BULLETS = 5


class Wrapper():
    def __init__(self, game_engine: GameEngine):
        self.game = game_engine

    def sort_walls(self, name):
        player = self.get_player(name)
        walls = self.game.get_walls()
        sorted_walls = sorted(
            walls,
            key=lambda w: self.calculate_distance_from_wall(player, w)
        )
        return sorted_walls
    
    def sort_bullets(self, name):
        player = self.get_player(name)
        bullets = self.game.get_bullets()
        sorted_bullets = sorted(
            bullets,
            key=lambda b: self.calculate_distance_from_bullet(player, b)
        )
        return sorted_bullets
    
    def get_player(self, player):
        players = self.game.get_players()
        return players.get(player.name)

    def calculate_distance_from_bullet(self, player, bullet):
        tank_position, bullet_position = player.get_position(), bullet.get_position()
        return ((tank_position.x - bullet_position.x)**2 +
                (tank_position.y - bullet_position.y)**2)**0.5

    def calculate_distance_from_wall(self, player, wall):
        tank_position = player.get_position()
        return min((tank_position.x - wall.x), (wall.x - tank_position.x),
                   (tank_position.y - wall.y), (wall.y - tank_position.y))

    def calculate_distance_from_enemy(self, player, enemy):
        tank_position = player.get_position()
        enemy_position = enemy.get_position()
        return ((tank_position.x - enemy_position.x)**2 +
                (tank_position.y - enemy_position.y)**2)**0.5

    def get_player_position(self, player):
        player = self.get_player(player)
        return player.get_position()

    def get_player_angle(self, player):
        player = self.game.get_player(player)
        return player.angle

    def get_enemies(self, player):
        player_name = player.name
        all_players = self.game.get_players()
        return [player for name, player in all_players.items() if name != player_name]

    def sort_enemies(self, player):
        player_tank = self.get_player(player)
        enemies = self.get_enemies(player)
        sorted_enemies = sorted(
            enemies,
            key=lambda e: self.calculate_distance_from_bullet(player_tank, e)
        )
        return sorted_enemies

    def get_obs(self):
        pass

    def step(self):
        pass
    