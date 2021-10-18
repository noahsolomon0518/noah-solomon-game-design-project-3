from typing import List, Union
import arcade
from arcade import sprite
from arcade.gui import *
from numpy.random import choice
from arcade.scene import Scene
from arcade.csscolor import BLACK,RED, LIGHT_STEEL_BLUE
from sprites.towers import PierceTurret, SimpleTurret, SniperTurret, SpeedTurret, Tower, Turret
from sprites.enemies import *


class Spawner:
    """Controls spawning of enemies based on level_enemy_spawns config that is passed to it. This is held in Level"""
    def __init__(self, level, level_enemy_spawns, level_enemy_path):
        self.level = level
        self.level_enemy_path = level_enemy_path
        self.level_enemy_spawns = level_enemy_spawns
        self.stage = 0
        self.part = 0
        self.amount = 0

    def spawn_next_wave(self):
        arcade.schedule(self.spawn_next_enemy, interval = self.level_enemy_spawns[self.stage][self.part]["interval"])


    def spawn_next_enemy(self, dt = None):
        """Spawns enemies according to stage and part given"""
        enemy_choices = self.level_enemy_spawns[self.stage][self.part]["enemies"]
        probabilities = self.level_enemy_spawns[self.stage][self.part]["probabilities"]
        self.level.enemy_list.append(choice(enemy_choices, p = probabilities)(self.level, self.level_enemy_path))
        self.amount += 1
        
        if(self.amount>=self.level_enemy_spawns[self.stage][self.part]["amount"]):
            if(self.part >= len(self.level_enemy_spawns[self.stage]) - 1):

                self.amount = 0
                self.stage += 1
                arcade.unschedule(self.spawn_next_enemy)
            else:
                arcade.unschedule(self.spawn_next_enemy)
                self.amount = 0
                self.part += 1
                arcade.schedule(self.spawn_next_enemy, self.level_enemy_spawns[self.stage][self.part]["interval"])


        


class Level(Scene):
    ENEMY_SPAWNS = None
    ENEMY_PATH = None
    TILESHEET = None
    START_MONEY = None
    START_HEALTH = None


    def __init__(self):
        super().__init__()
        self.add_sprite_list("enemy_list")
        self.add_sprite_list("tower_list")
        self.add_sprite_list("projectile_list")
        self.add_sprite_list("gun_list")
        self.add_sprite_list("mouse_motion_sprites")
        self.add_sprite_list("mouse_press_sprites")

        self.manager = UIManager()

        self.buy_tower_panels = []

        self.health = 59
        self.money = 8000
        self.stage = 1

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.setup()

    def setup(self):
        buy_tower_panel_manager = BuyTowerPanels(self)
        self.manager.enable()
        self.manager.add(buy_tower_panel_manager)
        self.spawner = Spawner(self, self.__class__.ENEMY_SPAWNS, self.__class__.ENEMY_SPAWNS)
        self.buy_tower_panels.extend(buy_tower_panel_manager.buy_tower_panels)
        self.spawner.spawn_next_wave()

    def draw(self, names, **kwargs) -> None:
        self.manager.draw()
        draw_information(self)
        return super().draw(names=names, **kwargs)

    def handle_enemy_projectile_collisions(self):
        enemy_projectile_collisions = [enemy.collides_with_list(self.get_sprite_list("projectile_list")) for enemy in self.get_sprite_list("enemy_list")]
        for i, enemy in enumerate(self.get_sprite_list("enemy_list")):
            enemy: Enemy
            projectiles_collided = enemy_projectile_collisions[i]
            for projectile in projectiles_collided:
                enemy.on_collision_with_projectile(projectile)

    
    
    
    





#GUI for levels is below
def draw_information(level:Level, x = 5, y = 625, font_size = 20):
    """Draws score, money and stage"""
    arcade.draw_text(f"Money: {level.money}", x, y,  font_size = font_size)
    arcade.draw_text(f"Health: {level.health}", x, y - 1.5*font_size, font_size=font_size)
    arcade.draw_text(f"Stage: {level.stage}", x, y - 3*font_size, font_size=font_size)

class BuyTowerPanels(UIAnchorWidget):
    """BuyTowerPanels manager"""

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
    """One tower panel"""
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

    