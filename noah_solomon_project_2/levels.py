from typing import Union
import arcade
from arcade.application import Window
from arcade.gui import *
from arcade.scene import Scene
from arcade.csscolor import BLACK







#GUI for levels is below
def draw_information(parent, x = 5, y = 625, font_size = 20):
    arcade.draw_text(f"Money: {parent.money}", x, y,  font_size = font_size)
    arcade.draw_text(f"Health: {parent.health}", x, y - 1.5*font_size, font_size=font_size)
    arcade.draw_text(f"Stage: {parent.stage}", x, y - 3*font_size, font_size=font_size)

    

class InformationBox(UIAnchorWidget):


    def __init__(self, net_parent: Union[Scene, Window], **kwargs):
        self.net_parent = net_parent
        child = UIBorder(self.get_v_box()).with_space_around(left=5, top=5)
        super().__init__(child = child,anchor_x="left", anchor_y="top", background_color = BLACK, **kwargs)
    


    def get_v_box(self):
        children = self.get_children()
        v_box = UIBoxLayout(children=children)
        return v_box
    
    def get_children(self):

    

        health_label = UITextArea(text="Health:")
        health_label.fit_content()
        money_label = UITextArea(text="Money:")
        money_label.fit_content()
        stage_label = UITextArea(text="Stage:")
        stage_label.fit_content()




        return [
            UIBoxLayout(vertical=False, children=[
                health_label, HealthLabelValue(self.net_parent)
            ]).with_space_around(top=5, left=5, right = 5),
            UIBoxLayout(vertical=False, children=[
                money_label, MoneyLabelValue(self.net_parent)
            ]).with_space_around(top=5, left=5, right = 5),
            UIBoxLayout(vertical=False, children=[
                stage_label, StageLabelValue(self.net_parent)
            ]).with_space_around(top=5, left=5, bottom=5, right = 5)
        ]


class InformationLabelValue(UITextArea):
    def __init__(self, net_parent: Union[Scene, Window], **kwargs):
        self.net_parent = net_parent 
        super().__init__(text="        ", **kwargs)
        self.fit_content()
        
    def on_update(self, dt):
        self.text = self.get_text()
        self.fit_content()
        return super().on_update(dt)


    def get_text(self):
        """Abstract method for updating text"""

class HealthLabelValue(InformationLabelValue):
    def get_text(self):
        return str(self.net_parent.health)

class StageLabelValue(InformationLabelValue):
    def get_text(self):
        return str(self.net_parent.stage)

class MoneyLabelValue(InformationLabelValue):


    def get_text(self):
        return str(self.net_parent.money)
