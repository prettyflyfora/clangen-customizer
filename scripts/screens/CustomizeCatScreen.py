import pygame
import pygame_gui

from scripts.cat.cats import Cat
from scripts.cat.pelts import Pelt
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.ui_elements import UISurfaceImageButton, UIImageButton
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
        self.eye1_left_button = None
        self.eye1_right_button = None
        self.eye2_left_button = None
        self.eye2_right_button = None
        self.eye_colours = Pelt.eye_colours
        self.accessory_left_button = None
        self.accessory_right_button = None
        self.remove_accessory_button = None
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
        self.eye1_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 500), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER,
        )
        self.eye1_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 500), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER,
        )
        self.eye2_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 550), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER,
        )
        self.eye2_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 550), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
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

    def setup_cat(self):
        self.the_cat = Cat.fetch_cat(game.switches["cat"])

        # check cat age to determine which sprite to show
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

        # Set the accessory index to the current accessory
        if self.the_cat.pelt.accessory in self.accessories:
            self.cat_elements["accessory_index"] = self.accessories.index(self.the_cat.pelt.accessory)
        else:
            self.cat_elements["accessory_index"] = 0
        self.update_accessory_display()

        # Set the eye colour index to the current eye colours
        self.eye1_index = self.eye_colours.index(self.the_cat.pelt.eye_colour)
        if self.the_cat.pelt.eye_colour2 is None:
            self.eye2_index = "none"
            self.heterochromia = False
            self.eye2_left_button.disable()
            self.eye2_right_button.disable()
        else:
            self.eye2_index = self.eye_colours.index(self.the_cat.pelt.eye_colour2)
            self.heterochromia = True
        self.make_heterochromia_checkbox()
        self.update_eye_colour_display()

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
            elif event.ui_element == self.eye1_left_button:
                self.change_eye_colour(1, "left")
            elif event.ui_element == self.eye1_right_button:
                self.change_eye_colour(-1, "left")
            elif event.ui_element == self.eye2_left_button:
                self.change_eye_colour(1, "right")
            elif event.ui_element == self.eye2_right_button:
                self.change_eye_colour(-1, "right")
            elif event.ui_element == self.heterochromia_checkbox:
                self.handle_heterochromia_checkbox()
            elif event.ui_element == self.accessory_left_button:
                self.change_accessory(-1)
            elif event.ui_element == self.accessory_right_button:
                self.change_accessory(1)
            elif event.ui_element == self.remove_accessory_button:
                self.remove_accessory()

    def change_eye_colour(self, direction, eye):
        if eye == "left":
            self.the_cat.pelt.eye_colour = self.eye_colours[
                (self.eye_colours.index(self.the_cat.pelt.eye_colour) + direction) % len(self.eye_colours)
                ]
        else:
            self.the_cat.pelt.eye_colour2 = self.eye_colours[
                (self.eye_colours.index(self.the_cat.pelt.eye_colour2) + direction) % len(self.eye_colours)
                ]
        self.update_eye_colour_display()
        self.make_cat_sprite()

    def update_eye_colour_display(self):
        if "eye_colour" in self.cat_elements:
            self.cat_elements["eye_colour"].kill()
        if "eye_colour2" in self.cat_elements:
            self.cat_elements["eye_colour2"].kill()

        self.cat_elements["eye_colour"] = pygame_gui.elements.UITextBox(
            self.the_cat.pelt.eye_colour.lower(),
            ui_scale(pygame.Rect((400, 500), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter"),
        )

        eye_colour2_text = self.the_cat.pelt.eye_colour2 if self.the_cat.pelt.eye_colour2 else "none"
        self.cat_elements["eye_colour2"] = pygame_gui.elements.UITextBox(
            eye_colour2_text.lower(),
            ui_scale(pygame.Rect((400, 550), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter"),
        )

    def make_heterochromia_checkbox(self):
        if "heterochromia_checkbox" in self.cat_elements:
            self.cat_elements["heterochromia_checkbox"].kill()

        if self.heterochromia is True:
            self.heterochromia_checkbox = UIImageButton(
                ui_scale(pygame.Rect((675, 525), (50, 50))),
                "",
                object_id="@checked_checkbox",
                starting_height=2,
            )
        else:
            self.heterochromia_checkbox = UIImageButton(
                ui_scale(pygame.Rect((675, 525), (50, 50))),
                "",
                object_id="@unchecked_checkbox",
                starting_height=2,
            )
        self.cat_elements["heterochromia_checkbox"] = self.heterochromia_checkbox

    def handle_heterochromia_checkbox(self):
        self.heterochromia = not self.heterochromia
        if self.heterochromia:
            self.the_cat.pelt.eye_colour2 = self.eye_colours[0]
            self.eye2_left_button.enable()
            self.eye2_right_button.enable()
        else:
            self.the_cat.pelt.eye_colour2 = None
            self.eye2_left_button.disable()
            self.eye2_right_button.disable()
        self.make_heterochromia_checkbox()
        self.update_eye_colour_display()
        self.make_cat_sprite()

    def change_accessory(self, direction):
        if self.the_cat.pelt.accessory:
            self.the_cat.pelt.accessory = None

        self.cat_elements["accessory_index"] = (self.cat_elements["accessory_index"] + direction) % len(
            self.accessories)
        self.the_cat.pelt.accessory = self.accessories[self.cat_elements["accessory_index"]]
        self.update_accessory_display()
        self.make_cat_sprite()

    def remove_accessory(self):
        self.the_cat.pelt.accessory = None
        self.update_accessory_display()
        self.make_cat_sprite()

    def update_accessory_display(self):
        accessory_name = self.accessories[self.cat_elements["accessory_index"]] if self.the_cat.pelt.accessory else "no accessory"
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
        self._kill_cat_elements()

    def _kill_cat_elements(self):
        elements_to_kill = [
            "cat_name", "cat_image", "eye_colour", "eye_colour2",
            "heterochromia_checkbox", "accessory_name"
        ]
        for element in elements_to_kill:
            if element in self.cat_elements:
                self.cat_elements[element].kill()
        self.eye1_left_button.kill()
        self.eye1_right_button.kill()
        self.eye2_left_button.kill()
        self.eye2_right_button.kill()
        self.accessory_left_button.kill()
        self.accessory_right_button.kill()
        self.remove_accessory_button.kill()
