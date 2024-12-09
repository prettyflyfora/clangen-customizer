import random
import time

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
from scripts.utility import ui_scale, generate_sprite, ui_scale_dimensions, get_text_box_theme


def create_text_box(text, pos, size, theme):
    return pygame_gui.elements.UITextBox(
        text,
        ui_scale(pygame.Rect(pos, size)),
        manager=MANAGER,
        object_id=get_text_box_theme(theme)
    )


def create_button(pos, size, text, style):
    return UISurfaceImageButton(
        ui_scale(pygame.Rect(pos, size)),
        text,
        get_button_dict(style, size),
        object_id=f"@buttonstyles_{style.name.lower()}",
        manager=MANAGER
    )


def create_dropdown(pos, size, options, selected_option="1"):
    return pygame_gui.elements.UIDropDownMenu(
        options,
        selected_option,
        ui_scale(pygame.Rect(pos, size)),
        manager=MANAGER,
        object_id="@dropdown"
    )


class CustomizeCatScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.the_cat = None
        self.cat_elements = {}
        self.life_stage = None
        self.cat_image = None
        self.back_button = None
        self.pelt_name_label = None
        self.pelt_name_dropdown = None
        self.pelt_names = list(Pelt.sprites_names.keys())
        self.pelt_colour_label = None
        self.pelt_colour_dropdown = None
        self.pelt_colours = [color.capitalize() for color in Pelt.pelt_colours]
        self.white_patches_label = None
        self.white_patches_dropdown = None
        self.white_patches = [patch.capitalize() for patch in
                              (Pelt.little_white + Pelt.mid_white + Pelt.high_white + Pelt.mostly_white)]
        self.white_patches.append(Pelt.white_sprites[6].capitalize())
        self.white_patches.insert(0, "None")
        self.vitiligo_label = None
        self.vitiligo_dropdown = None
        self.vitiligo_patterns = [pattern.capitalize() for pattern in Pelt.vit]
        self.vitiligo_patterns.insert(0, "None")
        self.points_label = None
        self.points_dropdown = None
        self.points_markings = [marking.capitalize() for marking in Pelt.point_markings]
        self.points_markings.insert(0, "None")
        self.pelt_length_label = None
        self.pelt_length_left_button = None
        self.pelt_length_right_button = None
        self.pelt_lengths = Pelt.pelt_length
        self.pose_right_button = None
        self.pose_left_button = None
        self.poses = None
        self.eye_colour1_label = None
        self.eye_colour2_label = None
        self.eye_colour1_dropdown = None
        self.eye_colour2_dropdown = None
        self.enable_heterochromia_text = None
        self.heterochromia = False
        self.eye_colours = [colour.capitalize() for colour in Pelt.eye_colours]
        self.eye_colours.insert(0, "None")
        self.reverse_button = None
        self.skin_left_button = None
        self.skin_right_button = None
        self.skins = Pelt.skin_sprites
        self.accessory_left_button = None
        self.accessory_right_button = None
        self.remove_accessory_button = None
        self.accessories = list(
            dict.fromkeys(Pelt.plant_accessories + Pelt.wild_accessories + Pelt.tail_accessories + Pelt.collars))

    def screen_switches(self):
        super().screen_switches()
        self.the_cat = Cat.fetch_cat(game.switches["cat"])
        self.setup_labels()
        self.setup_buttons()
        self.setup_dropdowns()
        self.setup_cat()

    def setup_labels(self):
        self.pelt_name_label = create_text_box("pelt name", (275, 45), (150, 40), "#text_box_30_horizleft")
        self.pelt_colour_label = create_text_box("pelt colour", (450, 45), (150, 40), "#text_box_30_horizleft")
        self.pelt_length_label = create_text_box("pelt length", (625, 45), (150, 40), "#text_box_30_horizleft")
        self.white_patches_label = create_text_box("white patches", (275, 120), (150, 40), "#text_box_30_horizleft")
        self.vitiligo_label = create_text_box("vitiligo", (450, 120), (150, 40), "#text_box_30_horizleft")
        self.points_label = create_text_box("point", (625, 120), (150, 40), "#text_box_30_horizleft")
        self.eye_colour1_label = create_text_box("eye colour 1", (275, 395), (150, 40), "#text_box_30_horizleft")
        self.enable_heterochromia_text = create_text_box("heterochromia", (470, 428), (150, 40),
                                                         "#text_box_30_horizcenter")
        self.eye_colour2_label = create_text_box("eye colour 2", (625, 395), (150, 40), "#text_box_30_horizleft")

    def setup_buttons(self):
        self.back_button = create_button((25, 25), (105, 30), get_arrow(2) + " Back", ButtonStyles.SQUOVAL)
        self.pelt_length_left_button = create_button((630, 80), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pelt_length_right_button = create_button((740, 80), (30, 30), get_arrow(1, False),
                                                      ButtonStyles.ROUNDED_RECT)
        self.pose_left_button = create_button((450, 350), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pose_right_button = create_button((590, 350), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.reverse_button = create_button((670, 500), (70, 30), "Reverse", ButtonStyles.ROUNDED_RECT)
        self.skin_left_button = create_button((450, 550), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.skin_right_button = create_button((590, 550), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.accessory_left_button = create_button((450, 600), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.accessory_right_button = create_button((590, 600), (30, 30), get_arrow(1, False),
                                                    ButtonStyles.ROUNDED_RECT)
        self.remove_accessory_button = create_button((670, 600), (70, 30), "Remove", ButtonStyles.ROUNDED_RECT)

    def setup_dropdowns(self):
        self.pelt_name_dropdown = create_dropdown((275, 75), (150, 40), self.pelt_names, self.the_cat.pelt.name)
        self.pelt_colour_dropdown = create_dropdown((450, 75), (150, 40), self.pelt_colours,
                                                    self.the_cat.pelt.colour.capitalize())
        self.white_patches_dropdown = create_dropdown((275, 150), (150, 40), self.white_patches,
                                                      self.the_cat.pelt.white_patches.capitalize() if self.the_cat.pelt.white_patches else "None")
        self.vitiligo_dropdown = create_dropdown((450, 150), (150, 40), self.vitiligo_patterns,
                                                 self.the_cat.pelt.vitiligo.capitalize() if self.the_cat.pelt.vitiligo else "None")
        self.points_dropdown = create_dropdown((625, 150), (150, 40), self.points_markings,
                                               self.the_cat.pelt.points.capitalize() if self.the_cat.pelt.points else "None")
        self.eye_colour1_dropdown = create_dropdown((275, 425), (150, 40), self.eye_colours,
                                                   self.the_cat.pelt.eye_colour.capitalize())
        self.eye_colour2_dropdown = create_dropdown((625, 425), (150, 40), self.eye_colours,
                                                   self.the_cat.pelt.eye_colour2.capitalize() if self.the_cat.pelt.eye_colour2 else self.eye_colour1_dropdown.selected_option[1].capitalize())

    def setup_cat(self):
        self.get_cat_age()
        self.make_cat_sprite()
        self.setup_cat_elements()

    def setup_cat_elements(self):
        self.cat_elements["cat_name"] = create_text_box(f"customize {self.the_cat.name}", (30, 150), (250, 40),
                                                        "#text_box_34_horizcenter")
        self.setup_pelt_length()
        self.setup_poses()
        self.setup_eye_colours()
        self.setup_reverse()
        self.setup_skin()
        self.setup_accessory()

    def setup_pelt_length(self):
        self.cat_elements["pelt_length_index"] = self.pelt_lengths.index(self.the_cat.pelt.length)
        self.update_pelt_length_display()

    def setup_poses(self):
        if self.life_stage == "newborn" or self.the_cat.pelt.paralyzed:
            self.pose_left_button.disable()
            self.pose_right_button.disable()
        self.set_poses()
        self.cat_elements["current_pose"] = self.the_cat.pelt.cat_sprites[self.life_stage]
        self.update_pose_display()

    def setup_eye_colours(self):
        if self.eye_colour2_dropdown.selected_option[1] == self.eye_colour1_dropdown.selected_option[1]:
            self.heterochromia = False
            self.eye_colour2_dropdown.disable()
        else:
            self.heterochromia = True
        self.make_heterochromia_checkbox()

    def setup_reverse(self):
        self.cat_elements["reverse_value"] = self.the_cat.pelt.reverse
        self.update_reverse_display()

    def setup_skin(self):
        self.cat_elements["skin_index"] = self.skins.index(self.the_cat.pelt.skin)
        self.update_skin_display()

    def setup_accessory(self):
        if self.the_cat.pelt.accessory in self.accessories:
            self.cat_elements["accessory_index"] = self.accessories.index(self.the_cat.pelt.accessory)
        else:
            self.cat_elements["accessory_index"] = 0
        self.update_accessory_display()

    def get_cat_age(self):
        self.life_stage = "adult" if self.the_cat.age in ["young adult", "adult", "senior adult"] else self.the_cat.age

    def make_cat_sprite(self):
        if "cat_image" in self.cat_elements:
            self.cat_elements["cat_image"].kill()
        self.cat_image = generate_sprite(self.the_cat, self.life_stage, False, False, True, True)
        self.cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((30, 200), (250, 250))),
            pygame.transform.scale(self.cat_image, ui_scale_dimensions((250, 250))),
            manager=MANAGER
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.handle_back_button()
            elif event.ui_element in [self.pelt_length_left_button, self.pelt_length_right_button]:
                self.handle_pelt_length_buttons(event.ui_element)
            elif event.ui_element in [self.pose_left_button, self.pose_right_button]:
                self.handle_pose_buttons(event.ui_element)
            elif event.ui_element == self.heterochromia_checkbox:
                self.handle_heterochromia_checkbox()
            elif event.ui_element == self.reverse_button:
                self.change_reverse()
            elif event.ui_element in [self.skin_left_button, self.skin_right_button]:
                self.handle_skin_buttons(event.ui_element)
            elif event.ui_element in [self.accessory_left_button, self.accessory_right_button]:
                self.handle_accessory_buttons(event.ui_element)
            elif event.ui_element == self.remove_accessory_button:
                self.remove_accessory()
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.pelt_name_dropdown:
                self.handle_pelt_name_dropdown()
            elif event.ui_element == self.pelt_colour_dropdown:
                self.handle_pelt_colour_dropdown()
            elif event.ui_element == self.white_patches_dropdown:
                self.handle_white_patches_dropdown()
            elif event.ui_element == self.vitiligo_dropdown:
                self.handle_vitiligo_dropdown()
            elif event.ui_element == self.points_dropdown:
                self.handle_points_dropdown()
            elif event.ui_element in [self.eye_colour1_dropdown, self.eye_colour2_dropdown]:
                self.handle_eye_colour_dropdown(event.ui_element)

    def handle_back_button(self):
        if self.the_cat.pelt.eye_colour2 == self.the_cat.pelt.eye_colour:
            self.the_cat.pelt.eye_colour2 = None
        self.change_screen("profile screen")

    def handle_pelt_name_dropdown(self):
        self.the_cat.pelt.name = self.pelt_name_dropdown.selected_option[1]
        self.make_cat_sprite()

    def handle_pelt_colour_dropdown(self):
        self.the_cat.pelt.colour = self.pelt_colour_dropdown.selected_option[1].upper()
        self.make_cat_sprite()

    def handle_white_patches_dropdown(self):
        selected_option = self.white_patches_dropdown.selected_option
        if selected_option[1] == "None":
            self.the_cat.pelt.white_patches = None
        else:
            self.the_cat.pelt.white_patches = selected_option[1].upper()
        self.make_cat_sprite()

    def handle_vitiligo_dropdown(self):
        selected_option = self.vitiligo_dropdown.selected_option
        if selected_option[1] == "None":
            self.the_cat.pelt.vitiligo = None
        else:
            self.the_cat.pelt.vitiligo = selected_option[1].upper()
        self.make_cat_sprite()

    def handle_points_dropdown(self):
        selected_option = self.points_dropdown.selected_option
        if selected_option[1] == "None":
            self.the_cat.pelt.points = None
        else:
            self.the_cat.pelt.points = selected_option[1].upper()
        self.make_cat_sprite()

    def handle_pelt_length_buttons(self, button):
        direction = -1 if button == self.pelt_length_left_button else 1
        self.change_pelt_length(direction)

    def handle_pose_buttons(self, button):
        direction = -1 if button == self.pose_left_button else 1
        self.change_pose(direction)

    def handle_eye_colour_dropdown(self, dropdown):
        if dropdown == self.eye_colour1_dropdown:
            self.the_cat.pelt.eye_colour = self.eye_colour1_dropdown.selected_option[1].upper()
        else:
            self.the_cat.pelt.eye_colour2 = self.eye_colour2_dropdown.selected_option[1].upper()
        self.make_cat_sprite()

    def handle_skin_buttons(self, button):
        direction = -1 if button == self.skin_left_button else 1
        self.change_skin(direction)

    def handle_accessory_buttons(self, button):
        direction = -1 if button == self.accessory_left_button else 1
        self.change_accessory(direction)

    def handle_sprites_for_pelt_length(self, previous_length):
        if (previous_length == "long" and self.the_cat.pelt.length != "long") or (
                previous_length != "long" and self.the_cat.pelt.length == "long"):
            self.set_poses()
            if self.life_stage != "newborn" and not self.the_cat.pelt.paralyzed:
                self.cat_elements["current_pose"] = self.poses[0]
            if self.life_stage == "adult":
                self.the_cat.pelt.cat_sprites[self.life_stage] = self.cat_elements["current_pose"]
                self.the_cat.pelt.cat_sprites[self.the_cat.age] = self.cat_elements["current_pose"]
                self.update_pose_display()
                self.make_cat_sprite()
            else:
                self.the_cat.pelt.cat_sprites['adult'] = random.randint(6,
                                                                        8) if previous_length == "long" else random.randint(
                    9, 11)
                self.the_cat.pelt.cat_sprites['sprite_para_adult'] = 15 if previous_length == "long" else 16

    def change_pelt_length(self, direction):
        previous_length = self.the_cat.pelt.length
        self.cat_elements["pelt_length_index"] = (self.cat_elements["pelt_length_index"] + direction) % len(
            self.pelt_lengths)
        self.the_cat.pelt.length = self.pelt_lengths[self.cat_elements["pelt_length_index"]]
        self.update_pelt_length_display()
        self.handle_sprites_for_pelt_length(previous_length)

    def update_pelt_length_display(self):
        self.kill_element("pelt_length")
        self.cat_elements["pelt_length"] = create_text_box(self.the_cat.pelt.length.lower(), (623, 78), (150, 40),
                                                           "#text_box_30_horizcenter")

    def set_poses(self):
        age_poses = {
            "kitten": [0, 1, 2],
            "adolescent": [3, 4, 5],
            "adult": [6, 7, 8] if self.the_cat.pelt.length != "long" else [9, 10, 11],
            "senior": [12, 13, 14]
        }
        self.poses = age_poses.get(self.life_stage, [])

    def change_pose(self, direction):
        current_index = self.poses.index(self.cat_elements["current_pose"])
        new_index = (current_index + direction) % len(self.poses)
        self.cat_elements["current_pose"] = self.poses[new_index]
        self.the_cat.pelt.cat_sprites[self.life_stage] = self.cat_elements["current_pose"]
        if self.life_stage == "adult":
            self.the_cat.pelt.cat_sprites[self.the_cat.age] = self.cat_elements["current_pose"]
        self.update_pose_display()
        self.make_cat_sprite()

    def update_pose_display(self):
        self.kill_element("pose")
        pose_text = "none" if (self.the_cat.pelt.paralyzed or self.life_stage == "newborn") else str(
            self.cat_elements["current_pose"])
        self.cat_elements["pose"] = create_text_box(pose_text, (435, 350), (200, 40), "#text_box_22_horizcenter")

    def make_heterochromia_checkbox(self):
        self.kill_element("heterochromia_checkbox")
        checkbox_id = "@checked_checkbox" if self.heterochromia else "@unchecked_checkbox"
        self.heterochromia_checkbox = UIImageButton(
            ui_scale(pygame.Rect((450, 430), (30, 30))),
            "",
            object_id=checkbox_id,
            starting_height=2
        )
        self.cat_elements["heterochromia_checkbox"] = self.heterochromia_checkbox

    def handle_heterochromia_checkbox(self):
        self.heterochromia = not self.heterochromia
        if self.heterochromia:
            self.the_cat.pelt.eye_colour2 = self.eye_colour2_dropdown.selected_option[1].upper()
            self.eye_colour2_dropdown.enable()
        else:
            self.the_cat.pelt.eye_colour2 = None
            self.eye_colour2_dropdown.kill()
            self.eye_colour2_dropdown = create_dropdown(
                (625, 425),
                (150, 40),
                self.eye_colours,
                self.eye_colour1_dropdown.selected_option[1].capitalize()
            )
            self.eye_colour2_dropdown.disable()
        self.make_heterochromia_checkbox()
        self.make_cat_sprite()

    def change_reverse(self):
        self.the_cat.pelt.reverse = not self.the_cat.pelt.reverse
        self.update_reverse_display()
        self.make_cat_sprite()

    def update_reverse_display(self):
        self.kill_element("reverse")
        reverse_text = "reversed" if self.the_cat.pelt.reverse else "normal"
        self.cat_elements["reverse"] = create_text_box(reverse_text, (435, 500), (200, 40), "#text_box_22_horizcenter")

    def change_skin(self, direction):
        self.the_cat.pelt.skin = self.skins[(self.skins.index(self.the_cat.pelt.skin) + direction) % len(self.skins)]
        self.update_skin_display()
        self.make_cat_sprite()

    def update_skin_display(self):
        self.kill_element("skin")
        self.cat_elements["skin"] = create_text_box(self.the_cat.pelt.skin.lower(), (435, 550), (200, 40),
                                                    "#text_box_22_horizcenter")

    def change_accessory(self, direction):
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
        accessory_name = self.accessories[
            self.cat_elements["accessory_index"]] if self.the_cat.pelt.accessory else "no accessory"
        self.kill_element("accessory_name")
        self.cat_elements["accessory_name"] = create_text_box(accessory_name.lower(), (435, 600), (200, 40),
                                                              "#text_box_22_horizcenter")

    def exit_screen(self):
        self.back_button.kill()
        self._kill_cat_elements()

    def _kill_cat_elements(self):
        elements_to_kill = [
            "cat_name", "cat_image", "pelt_length", "pose", "eye_colour", "eye_colour2",
            "heterochromia_checkbox", "reverse", "skin", "accessory_name"
        ]
        for element in elements_to_kill:
            self.kill_element(element)
        self.kill_ui_elements()

    def kill_element(self, element_name):
        if element_name in self.cat_elements:
            self.cat_elements[element_name].kill()

    def kill_ui_elements(self):
        ui_elements = [
            self.pelt_name_text, self.pelt_name_dropdown, self.pelt_colour_text, self.pelt_colour_dropdown,
            self.white_patches_label, self.white_patches_dropdown, self.vitiligo_label, self.vitiligo_dropdown,
            self.points_label, self.points_dropdown, self.eye_colour1_label, self.eye_colour2_label,
            self.enable_heterochromia_text, self.eye_colour1_dropdown, self.eye_colour2_dropdown,
            self.pelt_length_left_button, self.pelt_length_right_button, self.pose_left_button,
            self.pose_right_button, self.reverse_button, self.skin_left_button, self.skin_right_button,
            self.accessory_left_button, self.accessory_right_button,
            self.remove_accessory_button
        ]
        for ui_element in ui_elements:
            ui_element.kill()
