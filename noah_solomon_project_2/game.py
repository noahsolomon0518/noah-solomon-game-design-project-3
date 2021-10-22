from math import e
from arcade.csscolor import CORNFLOWER_BLUE
from arcade.sprite_list import spatial_hash
from arcade.sprite_list.sprite_list import SpriteList
from sprites.towers import *
from levels import *

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
        arcade.set_background_color(CORNFLOWER_BLUE)
        self.level = TestLevel(self)


    def setup(self):
        self.mouse_motion_sprites = SpriteList()
        self.mouse_press_sprites = SpriteList()
        self.show_view(self.level)


     
    def on_draw(self):
        arcade.start_render()
        self.level.on_draw()

    

    def on_update(self, delta_time: float):
        self.level.on_update(delta_time)
    











def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
