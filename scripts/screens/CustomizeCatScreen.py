import pygame
import pygame_gui

from scripts.cat.cats import Cat
from scripts.cat.pelts import Pelt
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.ui_elements import UISurfaceImageButton
from scripts.screens.Screens import Screens
from scripts.ui.generate_button import get_button_dict, ButtonStyles
from scripts.ui.get_arrow import get_arrow
from scripts.utility import ui_scale, shorten_text_to_fit, generate_sprite, ui_scale_offset, ui_scale_dimensions, \
    get_text_box_theme

class CustomizeCatScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.the_cat = None
        self.cat_elements = {}
        self.life_stage = None
        self.cat_image = None
        self.back_button = None
        self.accessory_left_button = None
        self.accessory_right_button = None
        self.remove_accessory_button = None
        self.accessory_index = 0
        self.accessories = Pelt.plant_accessories + Pelt.wild_accessories + Pelt.tail_accessories + Pelt.collars

    def screen_switches(self):
        super().screen_switches()

        self.back_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((25, 25), (105, 30))),
            get_arrow(2) + " Back",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        self.accessory_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 600), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER,
        )
        self.accessory_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 600), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER,
        )
        self.remove_accessory_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((670, 600), (100, 30))),
            "Remove",
            get_button_dict(ButtonStyles.ROUNDED_RECT, (100, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER,
        )

        self.setup_cat()
        self.update_accessory_display()

    def setup_cat(self):
        self.the_cat = Cat.fetch_cat(game.switches["cat"])

        if self.the_cat.age in ["young adult", "adult", "senior adult"]:
            self.life_stage = "adult"
        else:
            self.life_stage = self.the_cat.age

        self.make_cat_sprite()

        title_text = ("customize " + str(self.the_cat.name))

        self.cat_elements["cat_name"] = pygame_gui.elements.UITextBox(
            title_text,
            ui_scale(pygame.Rect((0, 0), (-1, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter"),
            anchors={"centerx": "centerx"},
        )
        self.cat_elements["cat_name"].set_relative_position(ui_scale_offset((0, 100)))

    def make_cat_sprite(self):
        # remove the old cat image
        if "cat_image" in self.cat_elements:
            self.cat_elements["cat_image"].kill()

        self.cat_image = generate_sprite(self.the_cat, self.life_stage, False, False, True,
                                         True)

        self.cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((30, 200), (250, 250))),
            pygame.transform.scale(self.cat_image, ui_scale_dimensions((250, 250))),
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.change_screen("profile screen")
            elif event.ui_element == self.accessory_left_button:
                self.change_accessory(-1)
            elif event.ui_element == self.accessory_right_button:
                self.change_accessory(1)
            elif event.ui_element == self.remove_accessory_button:
                self.remove_accessory()

    def change_accessory(self, direction):
        if self.the_cat.pelt.accessory:
            self.the_cat.pelt.accessory = None

        self.accessory_index = (self.accessory_index + direction) % len(self.accessories)
        self.the_cat.pelt.accessory = self.accessories[self.accessory_index]
        self.update_accessory_display()
        self.make_cat_sprite()

    def remove_accessory(self):
        self.the_cat.pelt.accessory = None
        self.update_accessory_display()
        self.make_cat_sprite()

    def update_accessory_display(self):
        accessory_name = self.accessories[self.accessory_index] if self.the_cat.pelt.accessory else "no accessory"
        if "accessory_name" in self.cat_elements:
            self.cat_elements["accessory_name"].kill()

        self.cat_elements["accessory_name"] = pygame_gui.elements.UITextBox(
            accessory_name.lower(),
            ui_scale(pygame.Rect((400, 600), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter"),
        )

    def exit_screen(self):
        self.back_button.kill()
        self.cat_elements["cat_name"].kill()
        self.cat_elements["cat_image"].kill()
        self.cat_elements["accessory_name"].kill()
        self.accessory_left_button.kill()
        self.accessory_right_button.kill()
        self.remove_accessory_button.kill()
