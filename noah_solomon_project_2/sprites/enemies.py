from typing import List
from arcade import load_texture, AnimationKeyframe
from math import sqrt
from arcade.sprite import AnimatedTimeBasedSprite, Sprite
from arcade.sprite_list.sprite_list import SpriteList
from sprites.projectiles import Projectile, Bullet


def euclidean_distance(pos_1: List, pos_2:List):
    """Gets distance between 2 sprites."""
    return sqrt((pos_1[0] - pos_2[0])**2+(pos_1[1] - pos_2[1])**2)









ENEMY_PATH_CONFIG = {
     """If cord is (0,32) then destination will be middle so (16, 48). First cord is enemy starting place"""
     "map_1" :[
          (None, None)
     ]
}

def extract_textures(name, col_start, col_end, row, sprite_size = 16, duration = 200):
     """Used to partition out animation key frames"""
     return [
          AnimationKeyframe(i, duration, load_texture("assets/enemies/"+ name+ "_16x16.png", i*sprite_size, row*sprite_size, sprite_size, sprite_size)) for i in range(col_start, col_end+1)
     ]


     
class Enemy(AnimatedTimeBasedSprite):
     """Enemy abstract class"""
     WALK_ANIMATION = None
     START_HEALTH = None
     START_SPEED = None
     START_DAMAGE = None

     def __init__(self, level, destinations: List[List], **kwargs):
         super().__init__(**kwargs)
         self.frames = self.__class__.WALK_ANIMATION
         
         self.center_x = destinations[0][0]
         self.center_y = destinations[0][1]
         self.health = self.__class__.START_HEALTH
         self.speed = self.__class__.START_SPEED
         self.damage = self.__class__.START_DAMAGE
         self.destination_number = 0
         self.destinations = destinations
         self.projectiles_hit_by = SpriteList()
         self.direction_vector = (0,0)
     

     def get_next_direction_vector(self):
          self.destination_number += 1
          if(self.destination_number >= len(self.destinations)):
               self.on_reach_last_destination()
          else:
               destination = self.destinations[self.destination_number]
               distance = euclidean_distance(destination, (self.center_x, self.center_y))
               self.direction_vector = (
                    (destination[0] - self.center_x)/distance,
                    (destination[1] - self.center_y)/distance,
               )

     def move(self, delta_time):
          """Moves in direction of destination at speed of self.speed"""
          if(euclidean_distance((self.center_x, self.center_y), self.destinations[self.destination_number])<=self.speed):
               self.get_next_direction_vector()
          self.center_x += 60 * delta_time * self.speed * self.direction_vector[0]
          self.center_y += 60 * delta_time * self.speed * self.direction_vector[1]

     def on_collision_with_projectile(self, projectile: Projectile):
          """Controls what happens when coliides with specific projectile. Collision handled through game. Can only be hit by projectile once"""
          if(projectile not in self.projectiles_hit_by):

               self.projectiles_hit_by.append(projectile)
               projectile.on_enemy_collision(self)

               


     def on_reach_last_destination(self):
          """When the enemy reaches the last destination reduce castles health by 10 ect..."""
          self.kill()

     def on_death(self):
          """Control what happens when health<0"""
          self.kill()

     def on_update(self, delta_time: float = 1 / 60):
          """What happens after enemy is spawned"""
          self.move(delta_time)
          self.update_animation()
          if(self.health<=0):
               self.on_death()
          





class Mushrooms(Enemy):
     """Fast but dont have a lot of health and damage"""
     WALK_ANIMATION = extract_textures("Mushrooms", 5, 8, 1)
     START_HEALTH = 1
     START_SPEED = 1.25
     START_DAMAGE = 1
     WORTH = 1

class Toad(Enemy):
     """Moderate speed but smallish damage and health"""
     WALK_ANIMATION = extract_textures("Toad", 5, 8, 1)
     START_HEALTH = 2
     START_SPEED = 1
     START_DAMAGE = 2
     WORTH = 3

class Bear(Enemy):
     """Tank enemy lots of health and damage but very slow"""
     WALK_ANIMATION = extract_textures("Bear", 5, 8, 1)
     START_HEALTH = 10
     START_SPEED = 0.5
     START_DAMAGE = 10
     WORTH = 10
