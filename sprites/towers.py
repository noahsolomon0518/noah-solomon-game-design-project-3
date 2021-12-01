from typing import Union
from arcade import Sprite
import arcade
from arcade import Window
from math import cos, sin, sqrt
from arcade.application import View
from arcade.scene import Scene
from sprites.config import UPGRADES
from sprites.projectiles import Bullet, PiercingBullet, IceBullet
import math



def euclidean_distance(sprite_1: Sprite, sprite_2:Sprite):
    """Gets distance between 2 sprites."""
    return sqrt((sprite_1.center_x - sprite_2.center_x)**2+(sprite_1.center_y - sprite_2.center_y)**2)


class Tower(Sprite):
    """Abstract class that all towers inherit from"""

    COST = None
    START_RANGE = None
    FILENAME = None

    def __init__(self, level: View, filename: str = None, range: int = None, **kwargs):
        self.level = level
        self.attacking = False
        self.upgrade_stage = 0
        self.range = range or self.__class__.START_RANGE
        self.enemies_in_range = None
        super().__init__(filename=filename or self.__class__.FILENAME, **kwargs)
        self.gun = Sprite("assets/towers/turret_gun.png", center_x=self.center_x, center_y=self.center_y)
        self.level.gun_list.append(self.gun)
        


    def detect_enemies(self):
        """Returns all enemies from enemy list that are within range."""
        self.enemies_in_range = [
            sprite for sprite in self.level.enemy_list
            if euclidean_distance(self, sprite) <= self.range
        ]
        if(self.enemies_in_range):
            self.aim_at_enemy(self.enemies_in_range[0])
            
        
    def aim_at_enemy(self, enemy: Sprite):
        """Aims turret gun at enemy"""
        x_y = (
                (enemy.center_x-self.center_x)/euclidean_distance(self, enemy),
                (enemy.center_y-self.center_y)/euclidean_distance(self, enemy)
            )
        self.gun.angle = -math.atan2(x_y[0], x_y[1])*180/math.pi - 90

    def attack_enemy(self, dt):
        """Abstract attacking function that is sceduled when enemies in range. Supposed to use self.enemies_in_range"""
        pass
    
    #Not used
    def upgrade(self):
        """Arbitary method to upgrade tower based on config. 
        Slightly hackish but will make things very convenient..."""
        if(self.upgrade_stage<5):
            self.upgrade_stage += 1
            for key, value in UPGRADES[self.__class__.__name__][self.upgrade_stage]:
                self.__dict__[key] = value


    def on_update(self, delta_time):
        pass


        
            
    




class Turret(Tower):

    COST = None
    FILENAME = None
    START_RANGE = None
    START_SPEED = None
    START_BULLET = None
    START_BULLET_DAMAGE = None
    START_BULLET_SPEED = None
    START_BULLET_ACCURACY = None


    def __init__(self, level: Scene, **kwargs):

        self.speed = self.__class__.START_SPEED
        self.bullet = self.__class__.START_BULLET
        self.bullet_damage = self.__class__.START_BULLET_DAMAGE
        self.bullet_speed = self.__class__.START_BULLET_SPEED
        self.bullet_accuracy = self.__class__.START_BULLET_ACCURACY

        super().__init__(level = level, range = self.__class__.START_RANGE, filename = self.__class__.FILENAME, **kwargs)
        
    
    def attack_enemy(self, dt):
        self.level.projectile_list.append(Bullet(self.level, self.enemies_in_range[0], self.bullet_damage, self.bullet_speed, self.bullet_accuracy, center_x = self.center_x, center_y = self.center_y))
        

    def on_update(self, delta_time):
        self.detect_enemies()
        if(self.enemies_in_range and not self.attacking):
            arcade.schedule(self.attack_enemy, 1/self.speed)
            self.attacking = True
        elif(not self.enemies_in_range and self.attacking):
            arcade.unschedule(self.attack_enemy)
            self.attacking = False
        self.gun.center_y = self.center_y
        self.gun.center_x = self.center_x




class SimpleTurret(Turret):
    COST = 25
    FILENAME = "assets/towers/simple_turret.png"
    START_RANGE = 100
    START_SPEED = 1
    START_BULLET = Bullet
    START_BULLET_DAMAGE = 1
    START_BULLET_SPEED = 15
    START_BULLET_ACCURACY = 0.5


class SniperTurret(Turret):
    COST = 75
    FILENAME = "assets/towers/speed_turret.png"
    START_RANGE = 500
    START_SPEED = 0.2
    START_BULLET = Bullet
    START_BULLET_DAMAGE = 10
    START_BULLET_SPEED = 15
    START_BULLET_ACCURACY = 2



class PierceTurret(Turret):
    COST = 100
    FILENAME = "assets/towers/pierce_turret.png"
    START_RANGE = 200
    START_SPEED = 1
    START_BULLET = Bullet
    START_BULLET_DAMAGE = 3
    START_BULLET_SPEED = 10
    START_BULLET_ACCURACY = 2
    START_BULLET_PIERCE = 3

    def attack_enemy(self, dt):
        """Creates instance of PierceBullet"""
        self.level.projectile_list.append(PiercingBullet(self.level, self.enemies_in_range[0], self.bullet_damage, self.bullet_speed, self.bullet_accuracy, self.__class__.START_BULLET_PIERCE, center_x = self.center_x, center_y = self.center_y))

class SpeedTurret(Turret):
    COST = 150
    FILENAME = "assets/towers/speed_turret.png"
    START_RANGE = 75
    START_SPEED = 5
    START_BULLET = Bullet
    START_BULLET_DAMAGE = 1
    START_BULLET_SPEED = 5
    START_BULLET_ACCURACY = 0.65



class IceTurret(Turret):
    COST = 75
    FILENAME = "assets/towers/ice_turret.png"
    START_RANGE = 150
    START_SPEED = 1
    START_BULLET = Bullet
    START_BULLET_DAMAGE = 0
    START_BULLET_SPEED = 10
    START_BULLET_ACCURACY = 2
    START_BULLET_SLOW_TIME = 3
    START_BULLET_SLOW_AMOUNT = 0.5

    def attack_enemy(self, dt):
        """Creates instance of PierceBullet"""
        self.level.projectile_list.append(IceBullet(self.level, self.enemies_in_range[0],  self.bullet_speed, self.bullet_accuracy, self.__class__.START_BULLET_SLOW_TIME, self.__class__.START_BULLET_SLOW_AMOUNT, center_x = self.center_x, center_y = self.center_y))
