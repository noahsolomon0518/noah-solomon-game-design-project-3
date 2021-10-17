from typing import List, Union
import arcade
from arcade import sprite
from arcade import color
from arcade.application import Window
from arcade.color import AUBURN, BLUE, BLUE_GRAY
from arcade.gui import *
from arcade.scene import Scene
from arcade.csscolor import BLACK
from pyglet.libs.win32.constants import SPI_GETACCESSTIMEOUT

from sprites.towers import PierceTurret, SimpleTurret, SniperTurret, Tower, Turret





class BuyTowerPanel(sprite.Sprite):
    def __init__(self, tower: Tower, **kwargs):
        super().__init__(filename=tower.FILENAME, **kwargs)
    

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        print("HELLO")
        if(self.collides_with_point((x,y))):
            print("MOUSE ON SPRITE")


#GUI for levels is below
def draw_information(parent, x = 5, y = 625, font_size = 20):
    arcade.draw_text(f"Money: {parent.money}", x, y,  font_size = font_size)
    arcade.draw_text(f"Health: {parent.health}", x, y - 1.5*font_size, font_size=font_size)
    arcade.draw_text(f"Stage: {parent.stage}", x, y - 3*font_size, font_size=font_size)

class BuyTowerPanels(UIAnchorWidget):

    TOWERS = [SniperTurret, SimpleTurret, PierceTurret]

    def __init__(self, **kwargs):
        child = self.get_h_box()
        super().__init__(child = child, anchor_x="center", anchor_y="bottom", **kwargs)
    
    def get_h_box(self):
        children = self.get_buy_tower_panels()
        return UIBoxLayout(vertical=False, children=children)
    
    def get_buy_tower_panels(self):
        return [UIBoxLayout(
            children=[
                UITextArea(text=str(tower.__name__), height = 20, width = 100, font_size=10).with_space_around(2,2,2,2, BLUE),
                UISpriteWidget(sprite = sprite.Sprite(tower.FILENAME), height=32, width=32),
                UILabel(text=str(tower.COST))
            ]
        ).with_space_around(bg_color=BLUE_GRAY).with_border().with_space_around(10,10,20,20) for tower in self.__class__.TOWERS]


def draw_buy_tower_panels(buy_tower_panels: List[BuyTowerPanel] = [

], width = 70):
    for i, buy_tower in enumerate(buy_tower_panels):
        buy_tower.center_x = (i+1)*width
        buy_tower.center_y = 30


