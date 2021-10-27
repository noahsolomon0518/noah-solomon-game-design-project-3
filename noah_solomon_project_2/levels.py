from typing import List, Union
import arcade
from arcade import sprite
from arcade import color
from arcade.application import View, Window
from arcade.gui import *
from numpy.random import choice
from arcade.csscolor import BLACK, BLUE,RED, LIGHT_STEEL_BLUE, WHITE
from sprites.towers import IceTurret, PierceTurret, SimpleTurret, SniperTurret, SpeedTurret, Tower, Turret
from sprites.enemies import *

def tile_to_cartesian(tile):
    return  (32*tile[0]+16, 32*tile[1]+16)

def tiles_to_cartesian(locations: List[List]):
    """Converts tile locations to cartesian locations"""
    print(locations)
    return [tile_to_cartesian(location) for location in locations]


class Spawner:
    """Controls spawning of enemies based on level_enemy_spawns config that is passed to it. This is held in Level"""
    def __init__(self, level, level_enemy_spawns, level_enemy_path):
        self.level = level
        self.level_enemy_path = level_enemy_path
        self.level_enemy_spawns = level_enemy_spawns
        self.stage = 0
        self.part = 0
        self.amount = 0
        self.in_wave = False

    def spawn_next_wave(self):
        """Spawns wave <stage>. If no more waves signals for winning action"""
        if(self.stage>=len(self.level_enemy_spawns)):
            self.level.on_win()
            return
        self.in_wave = True
        arcade.schedule(self.spawn_next_enemy, interval = self.level_enemy_spawns[self.stage][self.part]["interval"])

    def spawn_next_enemy(self, dt = None):
        """Spawns enemies according to stage and part given"""
        
        enemy_choices = self.level_enemy_spawns[self.stage][self.part]["enemies"]
        probabilities = self.level_enemy_spawns[self.stage][self.part]["probabilities"]
        enemy = choice(enemy_choices, p = probabilities)(self.level, self.level_enemy_path)
        self.level.enemy_list.append(enemy)

        self.amount += 1
        
        if(self.amount>=self.level_enemy_spawns[self.stage][self.part]["amount"]):
            if(self.part >= len(self.level_enemy_spawns[self.stage]) - 1):

                self.amount = 0
                self.stage += 1
                arcade.unschedule(self.spawn_next_enemy)
                self.in_wave = False
            else:
                arcade.unschedule(self.spawn_next_enemy)
                self.amount = 0
                self.part += 1
                arcade.schedule(self.spawn_next_enemy, self.level_enemy_spawns[self.stage][self.part]["interval"])

    def delete(self):
        arcade.unschedule(self.spawn_next_enemy)
        del self
        


class Level(View):
    ENEMY_SPAWNS = None
    ENEMY_PATH = None
    TILESHEET = None
    START_MONEY = None
    START_HEALTH = None


    def __init__(self, game: Window):
        self.game = game
        super().__init__(game)
        self.tilemap = arcade.tilemap.load_tilemap(self.__class__.TILESHEET, use_spatial_hash=True)
        self.front_layer = None
        self.back_layer = None
        self.radius_list = None
        self.enemy_list = None
        self.tower_list = None
        self.projectile_list = None
        self.gun_list = None
        self.preview_tower = None
        self.manager = None
        self.buy_tower_panels = None
        self.health = None
        self.money = None
        self.stage = 1


    def setup(self):
        self.front_layer = SpriteList()
        self.back_layer = SpriteList()
        self.radius_list = SpriteList()
        self.enemy_list = SpriteList(use_spatial_hash=False)
        self.tower_list = SpriteList(use_spatial_hash=False)
        self.projectile_list = SpriteList(use_spatial_hash=False)
        self.gun_list = SpriteList(use_spatial_hash=False)
        self.preview_tower = SpriteList(use_spatial_hash=False)
        self.manager = UIManager()
        self.buy_tower_panels = []
        self.health = self.__class__.START_HEALTH
        self.money = self.__class__.START_MONEY
        self.stage = 1
        buy_tower_panel_manager = BuyTowerPanels(self)
        self.back_layer = self.tilemap.sprite_lists["background"]
        self.front_layer = self.tilemap.sprite_lists["front"]
        self.manager.enable()
        self.manager.add(widget= Quit(self.game))
        self.manager.add(UIAnchorWidget(child = NextWave(self), anchor_x="right", anchor_y="bottom"))
        self.manager.add(buy_tower_panel_manager)
        self.spawner = Spawner(self, self.__class__.ENEMY_SPAWNS, self.__class__.ENEMY_PATH)
        self.buy_tower_panels.extend(buy_tower_panel_manager.buy_tower_panels)

    def on_update(self, delta_time) -> None:
        self.handle_enemy_projectile_collisions()
        self.enemy_list.on_update(delta_time)
        self.projectile_list.on_update(delta_time)
        self.tower_list.on_update(delta_time)
        self.preview_tower.update()


    def on_draw(self):
        arcade.start_render()
        self.back_layer.draw()
        self.front_layer.draw()
        self.enemy_list.draw()
        self.tower_list.draw()
        self.projectile_list.draw()
        self.gun_list.draw()
        self.preview_tower.draw()
        self.radius_list.draw()
        self.manager.draw()
        draw_information(self)

 

    def handle_enemy_projectile_collisions(self):
        """All collisions between bullet and enemy handled here"""
        enemy_projectile_collisions = [enemy.collides_with_list(self.projectile_list) for enemy in self.enemy_list]
        for i, enemy in enumerate(self.enemy_list):
            enemy: Enemy
            projectiles_collided = enemy_projectile_collisions[i]
            for projectile in projectiles_collided:
                enemy.on_collision_with_projectile(projectile)

    def show_preview_tower(self, tower):
        """Shows range of tower"""
        self.preview_tower.append(tower)


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """Move preview tower"""
        if(self.preview_tower):
            self.preview_tower[0].on_mouse_motion(x,y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Buy tower"""
        if(self.preview_tower):
            self.preview_tower[0].on_mouse_press(x,y)
        
    def on_hide_view(self):
        self.manager.disable()
        del self
    
    
    def on_show_view(self):
        self.setup()

    def on_lose(self):
        """Displays lose screen"""
        self.game.show_view(self.game.lose_screen)

    def on_win(self):
        """Display winning screen"""
        self.game.show_view(self.game.win_screen)


class Quit(UIFlatButton):

    def __init__(self, game: Window):
        super().__init__(text="Quit", style=dict(bg_color = RED))
        self.game = game

    def on_click(self, event: UIOnClickEvent):
        """Quits to  main screen"""
        self.game.hide_view()
        print(self.game.current_view)
        self.game.show_view(self.game.intro_screen)
        
    
    
class NextWave(UIFlatButton):

    def __init__(self, level: Level):
        super().__init__(text="Next Wave", style=dict(bg_color = BLUE))
        self.level = level

    def on_click(self, event: UIOnClickEvent):
        """If no current wave go to next wave"""
        if(not self.level.spawner.in_wave):
            self.level.spawner.spawn_next_wave()


    def on_update(self, dt):
        if(self.level.spawner.in_wave):
            self._style["bg_color"] = color.GRAY
        else:
            self._style["bg_color"] = BLUE
        
    

class TestLevel(Level):
    ENEMY_SPAWNS = [[{
        "enemies":[Toad],
        "probabilities":[1],
        "amount": 1,
        "interval": 1
    }]]
    ENEMY_PATH = tiles_to_cartesian([(-1,10),(11,10), (11,6), (22,6), (22,10), (31,10)])
    TILESHEET = "tilemaps/map1.json"
    START_MONEY = 5000
    START_HEALTH = 1

class TestLevel2(Level):
    ENEMY_SPAWNS = [[{
        "enemies":[Toad],
        "probabilities":[1],
        "amount": 100,
        "interval": 1
    }]]
    ENEMY_PATH = tiles_to_cartesian([(-1,10),(11,10), (11,6), (22,6), (22,10), (31,10)])
    TILESHEET = "tilemaps/map1.json"
    START_MONEY = 500
    START_HEALTH = 100

class TestLevel3(Level):
    ENEMY_SPAWNS = [[{
        "enemies":[Toad, Bear],
        "probabilities":[0.5,0.5],
        "amount": 100,
        "interval": 0.5
    }]]
    ENEMY_PATH = tiles_to_cartesian([(-1,10),(11,10), (11,6), (22,6), (22,10), (31,10)])
    TILESHEET = "tilemaps/map1.json"
    START_MONEY = 5000
    START_HEALTH = 100



#GUI for levels is below
def draw_information(level:Level, x = 5, y = 625, font_size = 20):
    """Draws score, money and stage"""
    arcade.draw_text(f"Money: {level.money}", x, y,  font_size = font_size)
    arcade.draw_text(f"Health: {level.health}", x, y - 1.5*font_size, font_size=font_size)
    arcade.draw_text(f"Stage: {level.stage}", x, y - 3*font_size, font_size=font_size)

class BuyTowerPanels(UIAnchorWidget):
    """BuyTowerPanels manager"""

    TOWERS = [SniperTurret, SimpleTurret, PierceTurret, SpeedTurret, IceTurret]

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
        self.level.preview_tower.append(self.preview_tower)

    
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
        self.level.radius_list.append(sprite.SpriteCircle(self.tower.START_RANGE, WHITE))
        self.level.radius_list[0].alpha = 100
        
        self.cost = tower.COST
        super().__init__(filename=tower.FILENAME)

    def on_mouse_press(self,x,y):
        """When clicked checks if collision with anything and if have enough money"""
        if(self.level.money < self.cost):
            return
        
        
        if(y<100):
            return

        if(self.level.radius_list[0].color == RED):
            return

        self.level.tower_list.append(self.tower(self.level, center_x = self.center_x, center_y=self.center_y))
        self.level.money -= self.cost
    


    
    def kill(self):
        self.level.radius_list[0].kill()
        return super().kill()
    
    
    def on_mouse_motion(self, x,y):
        """Goes to mouse pointer"""
        collisions = self.collides_with_list(self.level.front_layer)
        if(collisions):
            self.level.radius_list[0].color = RED
        else:
            self.level.radius_list[0].color = WHITE
        self.center_y = (y//32)*32  + 16
        self.center_x = (x//32)*32  + 16
        self.level.radius_list[0].center_y = self.center_y
        self.level.radius_list[0].center_x = self.center_x

    