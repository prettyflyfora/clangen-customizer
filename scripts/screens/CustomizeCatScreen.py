import random

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
from scripts.utility import ui_scale, generate_sprite, ui_scale_offset, ui_scale_dimensions, \
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
        self.enable_heterchromia_text = None
        self.eye_colours = Pelt.eye_colours
        self.pelt_length_left_button = None
        self.pelt_length_right_button = None
        self.pelt_lengths = Pelt.pelt_length
        self.pose_right_button = None
        self.pose_left_button = None
        self.poses = None
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
            manager=MANAGER
        )
        self.eye1_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 400), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.eye1_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 400), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.enable_heterchromia_text = pygame_gui.elements.UITextBox(
            "enable\nheterochromia",
            ui_scale(pygame.Rect((670, 400), (100, 100))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_22_horizcenter")
        )
        self.eye2_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 450), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.eye2_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 450), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.pose_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 500), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.pose_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 500), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.pelt_length_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 550), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.pelt_length_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 550), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.accessory_left_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((350, 600), (60, 30))),
            get_arrow(2),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.accessory_right_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((590, 600), (60, 30))),
            get_arrow(2, False),
            get_button_dict(ButtonStyles.ROUNDED_RECT, (60, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )
        self.remove_accessory_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((670, 600), (100, 30))),
            "Remove",
            get_button_dict(ButtonStyles.ROUNDED_RECT, (100, 30)),
            object_id="@buttonstyles_rounded_rect",
            manager=MANAGER
        )

        self.setup_cat()

    def setup_cat(self):
        self.the_cat = Cat.fetch_cat(game.switches["cat"])

        # check cat age to determine which sprite to show
        self.get_cat_age()
        self.make_cat_sprite()

        title_text = ("customize " + str(self.the_cat.name))
        self.cat_elements["cat_name"] = pygame_gui.elements.UITextBox(
            title_text,
            ui_scale(pygame.Rect((0, 0), (-1, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter"),
            anchors={"centerx": "centerx"}
        )
        self.cat_elements["cat_name"].set_relative_position(ui_scale_offset((0, 100)))

        # set the eye colour index to the current eye colours
        self.cat_elements["eye1_index"] = self.eye_colours.index(self.the_cat.pelt.eye_colour)
        if self.the_cat.pelt.eye_colour2 is None:
            self.cat_elements["eye2_index"] = "none"
            self.heterochromia = False
            self.eye2_left_button.disable()
            self.eye2_right_button.disable()
        else:
            self.cat_elements["eye2_index"] = self.eye_colours.index(self.the_cat.pelt.eye_colour2)
            self.heterochromia = True
        self.make_heterochromia_checkbox()
        self.update_eye_colour_display()

        # set the pose index to the current pose
        self.set_poses()
        self.cat_elements["current_pose"] = self.the_cat.pelt.cat_sprites[self.life_stage]
        self.update_pose_display()

        # set the pelt length index to the current pelt length
        self.cat_elements["pelt_length_index"] = self.pelt_lengths.index(self.the_cat.pelt.length)
        self.update_pelt_length_display()

        # set the accessory index to the current accessory
        if self.the_cat.pelt.accessory in self.accessories:
            self.cat_elements["accessory_index"] = self.accessories.index(self.the_cat.pelt.accessory)
        else:
            self.cat_elements["accessory_index"] = 0
        self.update_accessory_display()

    def get_cat_age(self):
        if self.the_cat.age in ["young adult", "adult", "senior adult"]:
            self.life_stage = "adult"
        else:
            self.life_stage = self.the_cat.age

    def make_cat_sprite(self):
        # remove the old cat image
        if "cat_image" in self.cat_elements:
            self.cat_elements["cat_image"].kill()

        self.cat_image = generate_sprite(self.the_cat, self.life_stage, False, False, True,
                                         True)
        self.cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((30, 200), (250, 250))),
            pygame.transform.scale(self.cat_image, ui_scale_dimensions((250, 250)))
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                # removes second eye colour if it's the same as the first
                if self.the_cat.pelt.eye_colour2 == self.the_cat.pelt.eye_colour:
                    self.the_cat.pelt.eye_colour2 = None
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
            elif event.ui_element == self.pelt_length_left_button:
                self.change_pelt_length(-1)
            elif event.ui_element == self.pelt_length_right_button:
                self.change_pelt_length(1)
            elif event.ui_element == self.pose_left_button:
                self.change_pose(-1)
            elif event.ui_element == self.pose_right_button:
                self.change_pose(1)
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
            ui_scale(pygame.Rect((400, 400), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter")
        )

        eye_colour2_text = self.the_cat.pelt.eye_colour2 if self.the_cat.pelt.eye_colour2 else "none"
        self.cat_elements["eye_colour2"] = pygame_gui.elements.UITextBox(
            eye_colour2_text.lower(),
            ui_scale(pygame.Rect((400, 450), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter")
        )

    def make_heterochromia_checkbox(self):
        if "heterochromia_checkbox" in self.cat_elements:
            self.cat_elements["heterochromia_checkbox"].kill()

        if self.heterochromia is True:
            self.heterochromia_checkbox = UIImageButton(
                ui_scale(pygame.Rect((705, 450), (30, 30))),
                "",
                object_id="@checked_checkbox",
                starting_height=2
            )
        else:
            self.heterochromia_checkbox = UIImageButton(
                ui_scale(pygame.Rect((705, 450), (30, 30))),
                "",
                object_id="@unchecked_checkbox",
                starting_height=2
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

    def set_poses(self):
        if self.life_stage == "kitten":
            self.poses = [0,1,2]
        elif self.life_stage == "adolescent":
            self.poses = [3,4,5]
        elif self.life_stage == "adult":
            if self.the_cat.pelt.length != "long":
                self.poses = [6,7,8]
            else:
                self.poses = [9,10,11]
        elif self.life_stage == "senior":
            self.poses = [12,13,14]

    def change_pose(self, direction):
        current_index = self.poses.index(self.cat_elements["current_pose"])
        new_index = (current_index + direction) % len(self.poses)
        self.cat_elements["current_pose"] = self.poses[new_index]
        self.the_cat.pelt.cat_sprites[self.the_cat.age] = self.cat_elements["current_pose"]
        self.the_cat.pelt.cat_sprites[self.life_stage] = self.cat_elements["current_pose"]
        self.update_pose_display()
        self.make_cat_sprite()

    def update_pose_display(self):
        if "pose" in self.cat_elements:
            self.cat_elements["pose"].kill()

        self.cat_elements["pose"] = pygame_gui.elements.UITextBox(
            str(self.cat_elements["current_pose"]),
            ui_scale(pygame.Rect((400, 500), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter")
        )

    def change_pelt_length(self, direction):
        previous_length = self.the_cat.pelt.length
        self.cat_elements["pelt_length_index"] = (self.cat_elements["pelt_length_index"] + direction) % len(
            self.pelt_lengths)
        self.the_cat.pelt.length = self.pelt_lengths[self.cat_elements["pelt_length_index"]]
        self.update_pelt_length_display()

        if (previous_length == "long" and self.the_cat.pelt.length != "long") or (
                previous_length != "long" and self.the_cat.pelt.length == "long"):
            self.set_poses()
            self.cat_elements["current_pose"] = self.poses[0]  # reset to the first pose in the updated list

            if self.life_stage == "adult":
                if self.the_cat.age in ["young adult", "senior adult"]:
                    # updates the young adult/senior adult sprite (temporary, doesn't affect clan_cats)
                    self.the_cat.pelt.cat_sprites[self.the_cat.age] = self.cat_elements["current_pose"]
                self.the_cat.pelt.cat_sprites[self.life_stage] = self.cat_elements["current_pose"]
                self.update_pose_display()
                self.make_cat_sprite()

    def update_pelt_length_display(self):
        if "pelt_length" in self.cat_elements:
            self.cat_elements["pelt_length"].kill()

        self.cat_elements["pelt_length"] = pygame_gui.elements.UITextBox(
            self.the_cat.pelt.length.lower(),
            ui_scale(pygame.Rect((400, 550), (200, 40))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_34_horizcenter")
        )

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
            object_id=get_text_box_theme("#text_box_34_horizcenter")
        )

    def exit_screen(self):
        self.back_button.kill()
        self._kill_cat_elements()

    def _kill_cat_elements(self):
        elements_to_kill = [
            "cat_name", "cat_image", "eye_colour", "eye_colour2", "pelt_length", "pose",
            "heterochromia_checkbox", "accessory_name"
        ]
        for element in elements_to_kill:
            if element in self.cat_elements:
                self.cat_elements[element].kill()
        self.eye1_left_button.kill()
        self.eye1_right_button.kill()
        self.eye2_left_button.kill()
        self.eye2_right_button.kill()
        self.enable_heterchromia_text.kill()
        self.pelt_length_left_button.kill()
        self.pelt_length_right_button.kill()
        self.pose_left_button.kill()
        self.pose_right_button.kill()
        self.accessory_left_button.kill()
        self.accessory_right_button.kill()
        self.remove_accessory_button.kill()
