from typing import List, Union
import arcade
from arcade import sprite
from arcade import color
from arcade.application import Window
from arcade.gui import *
from enum import Enum
from arcade.scene import Scene
from arcade.csscolor import BLACK,RED, LIGHT_STEEL_BLUE
from pyglet.libs.win32.constants import SPI_GETACCESSTIMEOUT

from sprites.towers import PierceTurret, SimpleTurret, SniperTurret, SpeedTurret, Tower, Turret

class BuyTowerPanelsStates(Enum):
    IDLE = 0
    BUYING = 1



class Level(Scene):
    pass





#GUI for levels is below
def draw_information(parent, x = 5, y = 625, font_size = 20):
    arcade.draw_text(f"Money: {parent.money}", x, y,  font_size = font_size)
    arcade.draw_text(f"Health: {parent.health}", x, y - 1.5*font_size, font_size=font_size)
    arcade.draw_text(f"Stage: {parent.stage}", x, y - 3*font_size, font_size=font_size)

class BuyTowerPanels(UIAnchorWidget):

    TOWERS = [SniperTurret, SimpleTurret, PierceTurret, SpeedTurret]

    def __init__(self, level: Level, **kwargs):
        self.buy_tower_panels = None
        self.level = level
        child = self.get_h_box()
        self.selected = None
        super().__init__(child = child, anchor_x="center", anchor_y="bottom", **kwargs)
    
    def get_h_box(self):
        self.buy_tower_panels = self.get_buy_tower_panels()
        return UIBoxLayout(vertical=False, children=self.buy_tower_panels)
    
    def get_buy_tower_panels(self):
        return [BuyTowerPanel(self.level, self, tower).with_space_around(bg_color=LIGHT_STEEL_BLUE).with_border().with_space_around(10,10,20,20) for tower in self.__class__.TOWERS]

class BuyTowerPanel(UIBoxLayout):
    def __init__(self, level:Level, net_parent: BuyTowerPanels, tower: Tower):
        self.net_parent = net_parent
        self.level = level
        self.tower = tower
        self.label = UILabel(text=str(tower.__name__), height = 20, width = 100, font_size=10)
        self.label.fit_content()
        self.sprite_preview = UISpriteWidget(sprite = sprite.Sprite(tower.FILENAME), height=32, width=32).with_space_around(top=10)
        self.cost = UILabel(text=str(tower.COST))
        self.buy = self.get_button(text = "BUY", height = 20, width = 50)
        super().__init__(children=[self.label, self.sprite_preview, self.cost, self.buy])

    def on_buy(self):
        """Controls how button looks after click buy"""
        self.net_parent.selected = self
        self.buy = self.get_button(text = "CANCEL", height = 20, width = 50, style = {
            "bg_color":RED,
            "font_size":7,
            "font_color":BLACK
        })
        self.children = [self.label, self.sprite_preview, self.cost, self.buy]
        self.preview_tower  = PreviewTower(self.level, self.tower)
        self.level.mouse_motion_sprites.append(self.preview_tower)
        self.level.mouse_press_sprites.append(self.preview_tower)
    
    def on_idle(self):
        """Controls how button looks when idle"""
        self.net_parent.selected = None
        self.buy = self.get_button(text = "BUY", height = 20, width = 50)
        self.preview_tower.kill()
        self.preview_tower = None

        self.children = [self.label, self.sprite_preview, self.cost, self.buy]
    

    
    def get_button(self, **kwargs):
        button = UIFlatButton(**kwargs)
        @button.event("on_click")
        def buy_on_click(click):
            if(self.net_parent.selected not in [self, None]):
                self.net_parent.selected.on_idle()
                self.on_buy()
            elif(self.net_parent.selected == None):
                self.on_buy()
            elif(self.net_parent.selected == self):
                self.on_idle()
        return button

class PreviewTower(sprite.Sprite):
    """Mouse click and motion stuff handled by net_parent"""
    def __init__(self, level: Level, tower: Tower):
        self.level = level
        self.tower = tower
        self.cost = tower.COST
        super().__init__(filename=tower.FILENAME)

    def on_mouse_press(self,x,y):
        """When clicked checks if collision with anything and if have enough money"""
        if(self.level.money < self.cost):
            return
        
        
        if(y<100):
            return

        self.level.tower_list.append(self.tower(self.level, center_x = x, center_y=y))
        self.level.money -= self.cost
    

    def on_mouse_motion(self, x,y):
        """Goes to mouse pointer"""
        self.center_y = y
        self.center_x = x

    