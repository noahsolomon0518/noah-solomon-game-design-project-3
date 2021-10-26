from math import e
from arcade.color import GRAY_BLUE
from arcade.csscolor import CORNFLOWER_BLUE
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
    LEVELS = [TestLevel, TestLevel2, TestLevel3]

    def __init__(self):
        super().__init__(self.__class__.SCREEN_WIDTH, self.__class__.SCREEN_HEIGHT, self.__class__.SCREEN_TITLE)
        arcade.set_background_color(CORNFLOWER_BLUE)
        self.levels = [level(self) for level in self.__class__.LEVELS]
        self.intro_screen = IntroScreen(self, self.levels)

    def setup(self):
        self.mouse_motion_sprites = SpriteList()
        self.mouse_press_sprites = SpriteList()
        self.show_view(self.intro_screen)


     

    



#GUI


class IntroScreen(View):
    def __init__(self, game: Window, levels: List):
        super().__init__(game)
        self.game = game
        self.levels = levels
        self.manager = UIManager(self.game)
        self.create_play_buttons()



    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_show_view(self):
        self.manager.enable()
        return super().on_show_view()

    def on_hide_view(self):
        self.manager.disable()
        return super().on_hide_view()
    
    
    def create_play_buttons(self):
        self.v_box = UIBoxLayout()
        self.play_buttons = UIAnchorWidget(child = self.v_box)
        self.v_box.add(UILabel(font_size=50, text="Tower Defence").with_space_around(bottom=50))
        for level in self.levels:
            self.v_box.add(LevelPlayButton(self.game, level).with_space_around(bottom=20))
        self.manager.add(self.play_buttons)

class LevelPlayButton(UIFlatButton):
    def __init__(self, game: Window, level: Level,  **kwargs):
        self.game = game
        self.level = level
        super().__init__(text=str(level.__class__.__name__), width = 200)
        
    
    def on_click(self, event: UIOnClickEvent):
        self.game.show_view(self.level)
        return super().on_click(event)

    






def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
