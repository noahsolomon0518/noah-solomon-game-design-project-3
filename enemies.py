from typing import List
from arcade import load_texture, AnimationKeyframe
from math import sqrt
import arcade
from arcade.sprite import AnimatedTimeBasedSprite, Sprite
from arcade.sprite_list.sprite_list import SpriteList
from projectiles import Projectile


def euclidean_distance(pos_1: List, pos_2:List):
    """Gets distance between 2 sprites."""
    return sqrt((pos_1[0] - pos_2[0])**2+(pos_1[1] - pos_2[1])**2)











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
     WORTH = None

     def __init__(self, level, **kwargs):
         super().__init__(**kwargs)
         self.level = level
         self.frames = self.__class__.WALK_ANIMATION
         self.slowing = False
         self.destinations = self.level.find_shortest_path(level.ENEMY_START_POS, level.ENEMY_END_POS)
         self.center_x = self.destinations[0][0]
         self.center_y = self.destinations[0][1]
         self.last_distance_from_destination = float("inf")
         self.health = self.__class__.START_HEALTH
         self.speed = self.__class__.START_SPEED
         self.damage = self.__class__.START_DAMAGE
         self.destination_number = 0
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
          current_distance_from_destination = self.get_distance_from_destination()
          if(self.last_distance_from_destination <= current_distance_from_destination):
               #then moving away
               self.get_next_direction_vector()
               self.last_distance_from_destination = float("inf")
          else:
               self.last_distance_from_destination = current_distance_from_destination
          self.center_x += 60 * delta_time * self.speed * self.direction_vector[0]
          self.center_y += 60 * delta_time * self.speed * self.direction_vector[1]

     def get_distance_from_destination(self):
          return euclidean_distance((self.center_x, self.center_y), self.destinations[self.destination_number])

     def on_collision_with_projectile(self, projectile: Projectile):
          """Controls what happens when coliides with specific projectile. Collision handled through game. Can only be hit by projectile once"""
          if(projectile not in self.projectiles_hit_by):

               self.projectiles_hit_by.append(projectile)
               projectile.on_enemy_collision(self)

     def slow_down(self, time, amount):
          """Enemy slows down for <time> seconds by going <amount> of usual speed"""
          if(self.slowing):
               arcade.unschedule(self.reset_speed)
          
          self.slowing = True
          self.speed = self.__class__.START_SPEED * amount
          arcade.schedule(self.reset_speed, time)



     def reset_speed(self, dt):
          """Bullet can call this when speed should be"""
          self.speed = self.__class__.START_SPEED
          self.slowing = False
          arcade.unschedule(self.reset_speed)


     def re_path(self):
          self.destination_number = 0
          x_tile = round((self.center_x-16)/32)
          y_tile = round((self.center_y-16)/32)
          print((x_tile, y_tile))
          self.destinations = self.level.find_shortest_path((x_tile, y_tile), self.level.ENEMY_END_POS) or []
          self.get_next_direction_vector()


     def on_reach_last_destination(self):
          """When the enemy reaches the last destination reduce castles health by 10 ect..."""
          self.level.health -= self.__class__.WORTH
          if(self.level.health<=0):
               self.level.on_lose()
          self.kill()

     def on_death(self):
          """Control what happens when health<0"""
          self.level.money += self.__class__.WORTH
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
     WORTH = 2

class Toad(Enemy):
     """Moderate speed but smallish damage and health"""
     WALK_ANIMATION = extract_textures("Toad", 5, 8, 1)
     START_HEALTH = 2
     START_SPEED = 1
     START_DAMAGE = 2
     WORTH = 5

class Bear(Enemy):
     """Tank enemy lots of health and damage but very slow"""
     WALK_ANIMATION = extract_textures("Bear", 5, 8, 1)
     START_HEALTH = 13
     START_SPEED = 0.6
     START_DAMAGE = 10
     WORTH = 15


class Beholder(Enemy):
     """Another tank enemy lots of health and damage and faster than bear"""
     WALK_ANIMATION = extract_textures("Beholder", 5, 8, 1)
     START_HEALTH = 18
     START_SPEED = 0.65
     START_DAMAGE = 10
     WORTH = 20


class Necromancer(Enemy):
     """Moderate speed damage, health, and speed"""
     WALK_ANIMATION = extract_textures("Necromancer", 5, 8, 1)
     START_HEALTH = 15
     START_SPEED = 1
     START_DAMAGE = 7
     WORTH = 25

class Creature(Enemy):
     """Boss enemy"""
     WALK_ANIMATION = extract_textures("Creature", 5, 8, 1)
     START_HEALTH = 35
     START_SPEED = 0.9
     START_DAMAGE = 10
     WORTH = 50