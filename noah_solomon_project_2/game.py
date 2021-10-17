from math import e
from arcade.sprite_list import spatial_hash
from arcade.sprite_list.sprite_list import SpriteList
from sprites.enemies import Bear, Enemy, Mushrooms, Toad
from sprites.towers import *
from levels import *
from arcade.gui import UIManager

import arcade





class MyGame(arcade.Window):
    """
    Main application class.
    """
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 650
    SCREEN_TITLE = "Tower Defence"

    def __init__(self):

        super().__init__(self.__class__.SCREEN_WIDTH, self.__class__.SCREEN_HEIGHT, self.__class__.SCREEN_TITLE)
        self.enemy_list = None
        self.projectile_list = None
        self.buy_tower_panels = None
        self.tower_list = None
        self.mouse_motion_sprites = []
        self.mouse_press_sprites = []
        self.health = 59
        self.money = 8000
        self.stage = 5
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        buy_tower_panel_manager = BuyTowerPanels(self)
        self.manager = UIManager()
        self.manager.enable()
        self.manager.add(buy_tower_panel_manager)

        self.buy_tower_panels = []
        self.enemy_list = SpriteList(use_spatial_hash=False)
        self.projectile_list = SpriteList(use_spatial_hash=False)
        self.tower_list = SpriteList()
        self.gun_list = SpriteList(use_spatial_hash=False)
        self.mouse_motion_sprites = SpriteList()
        self.mouse_press_sprites = SpriteList()

        

    

        self.buy_tower_panels.extend(buy_tower_panel_manager.buy_tower_panels)



        turret = PierceTurret(self)
        turret.center_x = 400
        turret.center_y = 300
        self.enemy_list.append(Bear(self, [(0,32), (500,50), (500,500)]))
        self.enemy_list.append(Mushrooms(self, [(0,0), (500,50), (500,500)]))
        self.enemy_list.append(Toad(self, [(60,10), (500,50), (500,500)]))
        self.enemy_list.append(Toad(self, [(60,20), (500,50), (500,500)]))
        self.enemy_list.append(Toad(self, [(60,50), (500,50), (500,500)]))
        self.enemy_list.append(Toad(self, [(60,60), (500,50), (500,500)]))
        arcade.schedule(self.spawn, 0.5)

    def spawn(self, *args):
        self.enemy_list.append(Toad(self, [(60,60), (500,50), (500,500)]))
    def on_draw(self):

        arcade.start_render()
        self.tower_list.draw()
        self.gun_list.draw()
        self.enemy_list.draw()
        self.mouse_motion_sprites.draw()
        self.projectile_list.draw()
        self.manager.draw()
        draw_information(self)


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for sprite in self.mouse_motion_sprites:
            sprite.on_mouse_motion(x,y)
        return super().on_mouse_motion(x, y, dx, dy)
    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for sprite in self.mouse_motion_sprites:
            sprite.on_mouse_press(x,y)
        return super().on_mouse_press(x, y, button, modifiers)


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
