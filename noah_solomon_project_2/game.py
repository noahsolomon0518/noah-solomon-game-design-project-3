from math import e
from arcade.sprite_list.sprite_list import SpriteList
from sprites.enemies import Bear, Enemy, Mushrooms, Toad
from sprites.towers import *


import arcade





class MyGame(arcade.Window):
    """
    Main application class.
    """
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 650
    SCREEN_TITLE = "Platformer"

    def __init__(self):

        super().__init__(self.__class__.SCREEN_WIDTH, self.__class__.SCREEN_HEIGHT, self.__class__.SCREEN_TITLE)
        self.enemy_list = None
        self.projectile_list = None
        self.tower_list = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.enemy_list = SpriteList()
        self.projectile_list = SpriteList()
        self.tower_list = SpriteList()
        self.gun_list = SpriteList()


        turret = PierceTurret(self)
        turret.center_x = 400
        turret.center_y = 300
        self.enemy_list.append(Bear([(0,32), (500,50), (500,500)]))
        self.enemy_list.append(Mushrooms([(0,0), (500,50), (500,500)]))
        self.enemy_list.append(Toad([(60,4), (500,50), (500,500)]))
   
        self.tower_list.append(turret)



    def on_draw(self):

        arcade.start_render()
        self.tower_list.draw()
        self.gun_list.draw()
        self.enemy_list.draw()
        self.projectile_list.draw()




    def on_update(self, delta_time: float):

        self.tower_list.on_update()
        self.enemy_list.on_update()
        self.projectile_list.on_update()
        self.handle_enemy_projectile_collisions()

        return super().on_update(delta_time)


    def handle_enemy_projectile_collisions(self):
        enemy_projectile_collisions = [enemy.collides_with_list(self.projectile_list) for enemy in self.enemy_list]
        for i, enemy in enumerate(self.enemy_list):
            enemy: Enemy
            projectiles_collided = enemy_projectile_collisions[i]
            for projectile in projectiles_collided:
                enemy.on_collision_with_projectile(projectile)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
