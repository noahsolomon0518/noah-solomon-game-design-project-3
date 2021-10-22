from arcade import Sprite, Window, SpriteList
from math import sqrt
from arcade.scene import Scene
import numpy as np


def euclidean_distance(position_1, position_2):
    """Gets distance between 2 sprites."""
    return sqrt((position_1[0] - position_2[0])**2+(position_1[1] - position_2[1])**2)

ACCURACY_SCALER = 5

class Projectile(Sprite):
    """Abstracted projectile class"""
    def __init__(self, level: Scene, target: Sprite, filename: str, damage: int, speed: int, accuracy:int, **kwargs):
        super().__init__(filename = filename, **kwargs)
        self.level = level
        self.damage = damage
        self.speed = speed
        self.accuracy = accuracy
        self.direction_vector = self.calculate_direction_vector(target)

    def calculate_direction_vector(self, target: Sprite):
        """Calculate projectile direction vector to target"""

        x_noise = self.get_noise_for_direction()
        y_noise = self.get_noise_for_direction()
        position_1 = (self.center_x, self.center_y+60*target.direction_vector[1])
        position_2 = (target.center_x + x_noise, target.center_y + y_noise + 60*target.direction_vector[1])
        distance = euclidean_distance(position_1, position_2)
        return ( 
            (target.center_x + 10*target.direction_vector[0] - self.center_x + x_noise)/distance, 
            (target.center_y + 10*target.direction_vector[1] - self.center_y + y_noise)/distance
            )

    def get_noise_for_direction(self):
        """Adds noise to target path"""
        return np.random.normal(scale = ACCURACY_SCALER/self.accuracy)

    
    def move_to_target(self, dt):
        """Move towards target"""
        self.center_x += self.speed * dt * 60 * self.direction_vector[0]
        self.center_y += self.speed * dt * 60 * self.direction_vector[1]


    def on_update(self, delta_time: float = 1 / 60):
        self.move_to_target(delta_time)
        self.delete_if_off_screen()
   

    def delete_if_off_screen(self):
        """Remove from memory if off screen"""
        pad = 5
        if(self.center_x>self.level.game.width + pad or self.center_x<-pad or self.center_y>self.level.game.height + pad or self.center_y<-pad):
            self.kill()

    def on_enemy_collision(self, enemy: Sprite = None):
        """Handles what happens when collides with specific enemy"""
        pass


class Bullet(Projectile):
    """Regular old bullet that is destroyed on collision"""
    def  __init__(self, game: Window, target: Sprite, damage: int, speed: int, accuracy: int, **kwargs):
        super().__init__(game, target, "assets/projectiles/bullet.png", damage, speed, accuracy, **kwargs)

    def on_enemy_collision(self, enemy: Sprite = None):
        """Handles what happens when collides with specific enemy"""
        enemy.health -= self.damage
        self.kill()
        

class PiercingBullet(Projectile):
    """Bullet can pierce <health> amount of enemies"""
    def  __init__(self, game: Window, target: Sprite, damage: int, speed: int, accuracy: int, health:int, **kwargs):
        self.health = health
        super().__init__(game, target, "assets/projectiles/bullet.png", damage, speed, accuracy, **kwargs)

    def on_enemy_collision(self, enemy: Sprite = None):
        """Handles what happens when collides with specific enemy"""
        enemy.health -= self.damage
        self.health -= 1
        if(not self.health):
            self.kill()


    

