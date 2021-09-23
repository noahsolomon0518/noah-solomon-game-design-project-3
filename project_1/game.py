"""
Goal of game: Survive as long as possible. Don't get hit by red enemies

Controls:
    w or up: Move player upwards
    s or down: Mode player downwards
    space: Shoot bullet

Bugs:
    1. Game slows down a bit after a while. Not sure why since all sprites should be deleted when off screen
    2. Gui glitches out after health resets

"""

import arcade
import os
import random
from arcade import Scene
from arcade.color import BLACK
from arcade.sprite import Sprite
from arcade import gui

SPRITE_SCALING = 0.5
TILE_SIZE = 8
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Side scrolling game"

SHOOT_SOUND = arcade.Sound("assets/gunshot.mp3")

MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 0.5
STARTING_SCROLL_SPEED = 5
BULLETS_PER_AMMO = 3


class Bullet(Sprite):

    BULLET_SPEED = 10

    def __init__(self, x, y):
        super().__init__(filename="assets/bullet.png", scale=0.5)
        self.center_x = x
        self.center_y = y

    def update(self):
        self.center_x += Bullet.BULLET_SPEED
        self.delete_if_off_screen()
        return super().update()

    def delete_if_off_screen(self):
        if(self.center_x > 800):
            self.remove_from_sprite_lists()
            del self


class Enemy(Sprite):

    def __init__(self, x, y, enemy_speed=6):
        super().__init__(filename="assets/enemy.png", scale=0.5)
        self.speed = enemy_speed
        self.center_x = x
        self.center_y = y

    def update(self):
        self.center_x -= self.speed
        self.delete_if_off_screen()
        return super().update()

    def delete_if_off_screen(self):
        if(self.center_x < 0):
            self.remove_from_sprite_lists()
            del self

    @staticmethod
    def spawn_randomly():
        return Enemy(
            random.randint(850, 1100),
            random.randint(MyGame.PLAYER_Y_MIN, MyGame.PLAYER_Y_MAX),
            random.randint(6, 8)
        )


class Ammo(Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__(filename="assets/ammo.png", scale=1)
        self.speed = speed
        self.center_x = x
        self.center_y = y

    def update(self):
        self.center_x -= self.speed
        self.delete_if_off_screen()
        return super().update()

    def delete_if_off_screen(self):
        if(self.center_x < 0):
            self.remove_from_sprite_lists()
            del self

    @staticmethod
    def spawn_randomly():
        return Ammo(
            random.randint(850, 1100),
            random.randint(MyGame.PLAYER_Y_MIN, MyGame.PLAYER_Y_MAX)
        )


class MyGame(arcade.Window):
    """ Main application class. """

    PLAYER_Y_MAX = 90
    PLAYER_Y_MIN = 25

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.manager = gui.UIManager()
        self.v_box = gui.UIBoxLayout(vertical=True, align="left")
        self.ammo_box = gui.UIBoxLayout(vertical=False, align="left")
        self.health_box = gui.UIBoxLayout(vertical=False, align="left")
        self.score_box = gui.UIBoxLayout(vertical=False, align="left")
        self.manager.enable()

        self.ammo = 10
        self.health = 100
        self.score = 0
        self.total_amount_scrolled = 0
        self.next_enemy_spawn = 50
        self.next_ammo_spawn = 50
        self.scroll_speed = STARTING_SCROLL_SPEED
        self.player_sprite = None
        self.player_y_speed = 0

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()

    def setup(self):
        self.setup_player()
        self.setup_background()
        self.setup_gui()
        arcade.set_background_color(arcade.color.AMAZON)

    def setup_gui(self):    
        """Draws all the gui"""

        ammo_label = gui.UITextArea(text="Ammo: ",
                                    font_size=30,
                                    text_color=BLACK,
                                    multiline=False
                                    )

        ammo_value = gui.UITextArea(text="           ", font_size=30,
                                    text_color=BLACK,
                                    multiline=False)

        @ammo_value.event("on_update")
        def update_score(event):
            ammo_value.text = str(self.ammo)

        ammo_value.fit_content()
        ammo_label.fit_content()

        self.ammo_box.add(ammo_label)
        self.ammo_box.add(ammo_value)

        health_text_label = gui.UITextArea(text="Health: ",
                                           font_size=30,
                                           text_color=BLACK,
                                           multiline=False
                                           )

        health_value = gui.UITextArea(text="           ",
                                      font_size=30,
                                      text_color=BLACK,
                                      multiline=False)

        @health_value.event("on_update")
        def update_score(event):
            health_value.text = str(self.health)

        health_value.fit_content()
        health_text_label.fit_content()
        self.health_box.add(health_text_label)
        self.health_box.add(health_value)


        score_text_label = gui.UITextArea(text="Score: ",
                                           font_size=30,
                                           text_color=BLACK,
                                           multiline=False
                                           )

        score_value = gui.UITextArea(text="           ",
                                      font_size=30,
                                      text_color=BLACK,
                                      multiline=False)

        @score_value.event("on_update")
        def update_score(event):
            score_value.text = str(self.score)

        score_value.fit_content()
        score_text_label.fit_content()
        self.score_box.add(score_text_label)
        self.score_box.add(score_value)

        self.v_box.add(self.ammo_box)
        self.v_box.add(self.health_box)
        self.v_box.add(self.score_box)

        self.manager.add(
            gui.UIAnchorWidget(child=self.v_box,
                               anchor_x="left", anchor_y="top")
        )
 
    def setup_player(self):
        self.player_sprite = arcade.Sprite("assets/player.png", SPRITE_SCALING)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 50

    def setup_background(self):
        bg1 = arcade.Sprite("assets/background/cloud_1.png")
        bg1.center_x = 0 + bg1.width//2
        bg1.center_y = 0 + bg1.height//2

        bg2 = arcade.Sprite("assets/background/cloud_2.png")
        bg2.center_x = 800 + bg2.width//2
        bg2.center_y = 0 + bg2.height//2

        self.background_list.append(bg1)
        self.background_list.append(bg2)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        self.background_list.draw()
        self.ammo_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if (key == arcade.key.UP or key == arcade.key.W) and self.player_sprite.center_y < MyGame.PLAYER_Y_MAX:
            self.player_y_speed = MOVEMENT_SPEED

        if (key == arcade.key.DOWN or key == arcade.key.S) and self.player_sprite.center_y > MyGame.PLAYER_Y_MIN:
            self.player_y_speed = -MOVEMENT_SPEED

        if (key == arcade.key.SPACE and self.ammo > 0):
            self.bullet_list.append(
                Bullet(self.player_sprite.center_x, self.player_sprite.center_y))
            self.bullet_list.draw()
            SHOOT_SOUND.play()
            self.ammo -= 1

    def on_key_release(self, key, modifiers):
        if (key == arcade.key.UP or key == arcade.key.W):
            self.player_y_speed = 0

        if (key == arcade.key.DOWN or key == arcade.key.S):
            self.player_y_speed = 0

    def on_update(self, delta_time):
        self.handle_background_scroll()
        self.handle_player_movement()
        self.handle_player_enemy_collision()
        self.handle_player_ammo_collision()
        self.handle_enemy_bullet_collisions()
        self.handle_enemy_spawning()
        self.handle_ammo_spawning()
        self.handle_game_over()
        self.bullet_list.update()
        self.enemy_list.update()
        self.ammo_list.update()

        print(len(self.bullet_list), len(self.enemy_list), len(self.ammo_list))

    def handle_background_scroll(self):
        for bg in self.background_list:
            bg.center_x -= self.scroll_speed
        self.total_amount_scrolled += self.scroll_speed

        for bg in self.background_list:
            if(bg.center_x < 0 - bg.width//2):
                other_bg = self.background_list[0] if self.background_list[0] != bg else self.background_list[1]
                bg.center_x = other_bg.center_x + 800

    def handle_player_movement(self):
        if(self.player_y_speed > 0 and self.player_sprite.center_y < MyGame.PLAYER_Y_MAX):
            self.player_sprite.center_y += self.player_y_speed

        if(self.player_y_speed < 0 and self.player_sprite.center_y > MyGame.PLAYER_Y_MIN):
            self.player_sprite.center_y += self.player_y_speed

    def handle_player_enemy_collision(self):
        collisions = self.player_sprite.collides_with_list(self.enemy_list)
        if(collisions):
            for collision in collisions:
                collision.remove_from_sprite_lists()
                self.health -= 10

    def handle_player_ammo_collision(self):
        collisions = self.player_sprite.collides_with_list(self.ammo_list)
        if(collisions):
            for collision in collisions:
                collision.remove_from_sprite_lists()
                self.ammo += BULLETS_PER_AMMO

    def handle_enemy_bullet_collisions(self):
        collisions = [
            enemy.collides_with_list(self.bullet_list) for enemy in self.enemy_list
        ]
        if collisions:
            for i, collision in enumerate(collisions):
                if collision:
                    self.score += 1
                    self.enemy_list[i].remove_from_sprite_lists()
                    [bullet.remove_from_sprite_lists() for bullet in collision]

    def handle_enemy_spawning(self):
        if(self.total_amount_scrolled > self.next_enemy_spawn):
            self.enemy_list.append(Enemy.spawn_randomly())
            self.next_enemy_spawn += random.randint(50, 200)
            self.score += 1

    def handle_ammo_spawning(self):
        if(self.total_amount_scrolled > self.next_ammo_spawn):
            self.ammo_list.append(Ammo.spawn_randomly())
            self.next_ammo_spawn += random.randint(200, 500)
    
    #Still need to figure out proper way to end game
    def handle_game_over(self):
        if(self.health <= 0):
            self.health = 100
            self.score = 0
            self.ammo = 10


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
