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
from scripts.utility import ui_scale, generate_sprite, ui_scale_offset, ui_scale_dimensions, get_text_box_theme


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
        self.pelt_name_dropdown = None
        self.pelt_names = list(Pelt.sprites_names.keys())
        self.pelt_colour_dropdown = None
        self.pelt_colours = [color.capitalize() for color in Pelt.pelt_colours]
        self.pelt_length_left_button = None
        self.pelt_length_right_button = None
        self.pelt_lengths = Pelt.pelt_length
        self.pose_right_button = None
        self.pose_left_button = None
        self.poses = None
        self.eye1_left_button = None
        self.eye1_right_button = None
        self.eye2_left_button = None
        self.eye2_right_button = None
        self.enable_heterochromia_text = None
        self.eye_colours = Pelt.eye_colours
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
        self.setup_buttons()
        self.setup_cat()
        self.setup_dropdowns()

    def setup_buttons(self):
        self.back_button = create_button((25, 25), (105, 30), get_arrow(2) + " Back", ButtonStyles.SQUOVAL)
        self.pelt_length_left_button = create_button((450, 300), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pelt_length_right_button = create_button((590, 300), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.pose_left_button = create_button((450, 350), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pose_right_button = create_button((590, 350), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.eye1_left_button = create_button((450, 400), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.eye1_right_button = create_button((590, 400), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.eye2_left_button = create_button((450, 450), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.eye2_right_button = create_button((590, 450), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.enable_heterochromia_text = create_text_box("enable\nheterochromia", (670, 400), (100, 100), "#text_box_22_horizcenter")
        self.reverse_button = create_button((670, 500), (70, 30), "Reverse", ButtonStyles.ROUNDED_RECT)
        self.skin_left_button = create_button((450, 550), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.skin_right_button = create_button((590, 550), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.accessory_left_button = create_button((450, 600), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.accessory_right_button = create_button((590, 600), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.remove_accessory_button = create_button((670, 600), (70, 30), "Remove", ButtonStyles.ROUNDED_RECT)

    def setup_dropdowns(self):
        self.pelt_name_dropdown = create_dropdown((435, 200), (200, 40), self.pelt_names, self.the_cat.pelt.name)
        self.pelt_colour_dropdown = create_dropdown((435, 250), (200, 40), self.pelt_colours, self.the_cat.pelt.colour.capitalize())

    def setup_cat(self):
        self.the_cat = Cat.fetch_cat(game.switches["cat"])
        self.get_cat_age()
        self.make_cat_sprite()
        self.setup_cat_elements()

    def setup_cat_elements(self):
        self.cat_elements["cat_name"] = create_text_box(f"customize {self.the_cat.name}", (30, 150), (250, 40), "#text_box_34_horizcenter")
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
            elif event.ui_element in [self.eye1_left_button, self.eye1_right_button, self.eye2_left_button, self.eye2_right_button]:
                self.handle_eye_buttons(event.ui_element)
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

    def handle_pelt_length_buttons(self, button):
        direction = -1 if button == self.pelt_length_left_button else 1
        self.change_pelt_length(direction)

    def handle_pose_buttons(self, button):
        direction = -1 if button == self.pose_left_button else 1
        self.change_pose(direction)

    def handle_eye_buttons(self, button):
        direction = 1 if button in [self.eye1_left_button, self.eye2_left_button] else -1
        eye = "left" if button in [self.eye1_left_button, self.eye1_right_button] else "right"
        self.change_eye_colour(direction, eye)

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
                self.the_cat.pelt.cat_sprites['adult'] = random.randint(6, 8) if previous_length == "long" else random.randint(9, 11)
                self.the_cat.pelt.cat_sprites['sprite_para_adult'] = 15 if previous_length == "long" else 16

    def change_pelt_length(self, direction):
        previous_length = self.the_cat.pelt.length
        self.cat_elements["pelt_length_index"] = (self.cat_elements["pelt_length_index"] + direction) % len(self.pelt_lengths)
        self.the_cat.pelt.length = self.pelt_lengths[self.cat_elements["pelt_length_index"]]
        self.update_pelt_length_display()
        self.handle_sprites_for_pelt_length(previous_length)

    def update_pelt_length_display(self):
        self.kill_element("pelt_length")
        self.cat_elements["pelt_length"] = create_text_box(self.the_cat.pelt.length.lower(), (435, 300), (200, 40), "#text_box_22_horizcenter")

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
        pose_text = "none" if (self.the_cat.pelt.paralyzed or self.life_stage == "newborn") else str(self.cat_elements["current_pose"])
        self.cat_elements["pose"] = create_text_box(pose_text, (435, 350), (200, 40), "#text_box_22_horizcenter")

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
        self.kill_element("eye_colour")
        self.kill_element("eye_colour2")
        self.cat_elements["eye_colour"] = create_text_box(self.the_cat.pelt.eye_colour.lower(), (435, 400), (200, 40), "#text_box_22_horizcenter")
        eye_colour2_text = self.the_cat.pelt.eye_colour2 if self.the_cat.pelt.eye_colour2 else "none"
        self.cat_elements["eye_colour2"] = create_text_box(eye_colour2_text.lower(), (435, 450), (200, 40), "#text_box_22_horizcenter")

    def make_heterochromia_checkbox(self):
        self.kill_element("heterochromia_checkbox")
        checkbox_id = "@checked_checkbox" if self.heterochromia else "@unchecked_checkbox"
        self.heterochromia_checkbox = UIImageButton(
            ui_scale(pygame.Rect((705, 450), (30, 30))),
            "",
            object_id=checkbox_id,
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
        self.cat_elements["skin"] = create_text_box(self.the_cat.pelt.skin.lower(), (435, 550), (200, 40), "#text_box_22_horizcenter")

    def change_accessory(self, direction):
        self.the_cat.pelt.accessory = None
        self.cat_elements["accessory_index"] = (self.cat_elements["accessory_index"] + direction) % len(self.accessories)
        self.the_cat.pelt.accessory = self.accessories[self.cat_elements["accessory_index"]]
        self.update_accessory_display()
        self.make_cat_sprite()

    def remove_accessory(self):
        self.the_cat.pelt.accessory = None
        self.update_accessory_display()
        self.make_cat_sprite()

    def update_accessory_display(self):
        accessory_name = self.accessories[self.cat_elements["accessory_index"]] if self.the_cat.pelt.accessory else "no accessory"
        self.kill_element("accessory_name")
        self.cat_elements["accessory_name"] = create_text_box(accessory_name.lower(), (435, 600), (200, 40), "#text_box_22_horizcenter")

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
            self.pelt_name_dropdown, self.pelt_colour_dropdown,
            self.pelt_length_left_button, self.pelt_length_right_button,
            self.pose_left_button, self.pose_right_button, self.eye1_left_button, self.eye1_right_button,
            self.eye2_left_button, self.eye2_right_button, self.enable_heterochromia_text, self.reverse_button,
            self.skin_left_button, self.skin_right_button, self.accessory_left_button, self.accessory_right_button,
            self.remove_accessory_button
        ]
        for ui_element in ui_elements:
            ui_element.kill()