import random

import pygame
import pygame_gui
from pygame import Rect
from pygame_gui.elements import UIDropDownMenu, UITextBox

from scripts.cat.cats import Cat
from scripts.cat.pelts import Pelt
from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game
from scripts.game_structure.screen_settings import MANAGER
from scripts.game_structure.ui_elements import UISurfaceImageButton, UIImageButton
from scripts.screens.Screens import Screens
from scripts.ui.generate_box import get_box, BoxStyles
from scripts.ui.generate_button import get_button_dict, ButtonStyles
from scripts.ui.get_arrow import get_arrow
from scripts.utility import ui_scale, generate_sprite, ui_scale_dimensions, get_text_box_theme


def create_text_box(text, pos, size, theme, anchors=None):
    return UITextBox(
        text,
        ui_scale(Rect(pos, size)),
        manager=MANAGER,
        object_id=get_text_box_theme(theme),
        anchors=anchors
    )


def create_button(pos, size, text, style, anchors=None, sound_id=None):
    return UISurfaceImageButton(
        ui_scale(Rect(pos, size)),
        text,
        get_button_dict(style, size),
        object_id=f"@buttonstyles_{style.name.lower()}",
        manager=MANAGER,
        anchors=anchors,
        sound_id=sound_id
    )


def create_dropdown(pos, size, options, selected_option, style=None):
    return UIDropDownMenu(
        options,
        selected_option,
        ui_scale(Rect(pos, size)),
        object_id=f"#{style}",
        manager=MANAGER
    )


def create_options_list(attribute, case):
    if case == "upper":
        return [(option.capitalize(), option.upper()) for option in attribute]
    elif case == "lower":
        return [(option.capitalize(), option.lower()) for option in attribute]
    else:
        return [(option.capitalize(), option) for option in attribute]


def get_selected_option(attribute, case):
    if isinstance(attribute, list):
        if len(attribute) > 0:
            return attribute[0].capitalize(), attribute[0].upper()
        else:
            return "None", "NONE"
    if attribute:
        if case == "upper":
            return attribute.capitalize(), attribute.upper()
        elif case == "lower":
            return attribute.capitalize(), attribute.lower()
        else:
            return attribute.capitalize(), attribute
    else:
        if case == "upper":
            return "None", "NONE"
        elif case == "lower":
            return "None", "none"
        else:
            return "None", "None"


class CustomizeCatScreen(Screens):
    def __init__(self, name=None):
        super().__init__(name)
        self.the_cat = None
        self.next_cat = None
        self.previous_cat = None
        self.cat_elements = {}
        self.life_stage = None
        self.frame_image = None
        self.cat_image = None
        self.previous_cat_button = None
        self.back_button = None
        self.next_cat_button = None
        self.reset_button = None
        self.initial_state = None
        self.pelt_name_label = None
        self.pelt_name_dropdown = None
        self.pelt_names = list(Pelt.sprites_names.keys())
        self.pelt_colour_label = None
        self.pelt_colour_dropdown = None
        self.pelt_colours = Pelt.pelt_colours
        self.pelt_length_label = None
        self.pelt_length_left_button = None
        self.pelt_length_right_button = None
        self.pelt_lengths = Pelt.pelt_length
        self.pattern_label = None
        self.pattern_dropdown = None
        self.patterns = Pelt.tortiepatterns
        self.tortie_base_label = None
        self.tortie_base_dropdown = None
        self.tortie_bases = Pelt.tortiebases
        self.tortie_colour_label = None
        self.tortie_colour_dropdown = None
        self.tortie_colours = self.pelt_colours
        self.tortie_pattern_label = None
        self.tortie_pattern_dropdown = None
        self.tortie_patterns = self.tortie_bases
        self.white_patches_label = None
        self.white_patches_dropdown = None
        self.white_patches = Pelt.little_white + Pelt.mid_white + Pelt.high_white + Pelt.mostly_white
        self.white_patches.append(Pelt.white_sprites[6])
        self.white_patches.insert(0, "None")
        self.vitiligo_label = None
        self.vitiligo_dropdown = None
        self.vitiligo_patterns = [pattern.capitalize() for pattern in Pelt.vit]
        self.vitiligo_patterns.insert(0, "None")
        self.points_label = None
        self.points_dropdown = None
        self.points_markings = [marking.capitalize() for marking in Pelt.point_markings]
        self.points_markings.insert(0, "None")
        self.white_patches_tint_label = None
        self.white_patches_tint_dropdown = None
        self.white_patches_tints = ["None"] + [tint for tint in sprites.white_patches_tints["tint_colours"].keys() if
                                               tint != "none"]
        self.tint_label = None
        self.tint_dropdown = None
        self.tints = [tint for tint in list(sprites.cat_tints["tint_colours"].keys()) + list(
            sprites.cat_tints["dilute_tint_colours"].keys()) if tint != "none"]
        self.tints.insert(0, "None")
        self.skin_label = None
        self.skin_dropdown = None
        self.skins = Pelt.skin_sprites
        self.pose_label = None
        self.pose_right_button = None
        self.pose_left_button = None
        self.poses = None
        self.eye_colour1_label = None
        self.heterochromia_text = None
        self.eye_colour2_label = None
        self.eye_colour1_dropdown = None
        self.eye_colour2_dropdown = None
        self.heterochromia = False
        self.eye_colours = [colour.capitalize() for colour in Pelt.eye_colours]
        self.reverse_label = None
        self.reverse_button = None
        self.accessory_label = None
        self.accessory_dropdown = None
        self.accessories = ["None"] + list(
            dict.fromkeys(Pelt.plant_accessories + Pelt.wild_accessories + Pelt.tail_accessories + Pelt.collars))
        self.scar_message = None
        self.scar1_label = None
        self.scar2_label = None
        self.scar3_label = None
        self.scar4_label = None
        self.scar1_dropdown = None
        self.scar2_dropdown = None
        self.scar3_dropdown = None
        self.scar4_dropdown = None
        self.scars = ["None"] + Pelt.scars1 + Pelt.scars2 + Pelt.scars3
        self.initial_scar_selection = {}
        self.previous_scar_selection = {}

    # for testing purposes
    def print_pelt_attributes(self):
        print("\n*** PELT START ***")
        pelt_attributes = vars(self.the_cat.pelt)
        for attribute, value in pelt_attributes.items():
            print(f"{attribute}: {value}")
        print("*** PELT END ***")

    def screen_switches(self):
        super().screen_switches()
        self.setup_labels()
        self.frame_image = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((25, 150), (270, 270))), get_box(BoxStyles.FRAME, (250, 250)), starting_height=1
        )
        self.build_cat_page()


    def build_cat_page(self):
        self.the_cat = Cat.fetch_cat(game.switches["cat"])
        (self.next_cat, self.previous_cat) = self.the_cat.determine_next_and_previous_cats()
        self.cat_elements["cat_name"] = create_text_box("customize " + str(self.the_cat.name), (0, 25), (250, 40), "#text_box_34_horizcenter", {"centerx": "centerx"})
        self.setup_buttons()
        self.setup_next_and_previous_cat()
        self.setup_dropdowns()
        self.setup_cat()
        self.capture_initial_state()

    def setup_labels(self):
        self.pelt_name_label = create_text_box("pelt name", (275, 100), (130, 40), "#text_box_22_horizleft")
        self.pelt_colour_label = create_text_box("pelt colour", (450, 100), (130, 40), "#text_box_22_horizleft")
        self.pelt_length_label = create_text_box("pelt length", (224, 495), (130, 40), "#text_box_22_horizleft")
        self.pattern_label = create_text_box("pattern", (625, 100), (130, 40), "#text_box_22_horizleft")
        self.tortie_base_label = create_text_box("tortie base", (275, 175), (130, 40), "#text_box_22_horizleft")
        self.tortie_colour_label = create_text_box("tortie colour", (450, 175), (130, 40), "#text_box_22_horizleft")
        self.tortie_pattern_label = create_text_box("tortie pattern", (625, 175), (130, 40), "#text_box_22_horizleft")
        self.white_patches_label = create_text_box("white patches", (275, 260), (130, 40), "#text_box_22_horizleft")
        self.vitiligo_label = create_text_box("vitiligo", (450, 260), (130, 40), "#text_box_22_horizleft")
        self.points_label = create_text_box("point", (625, 260), (130, 40), "#text_box_22_horizleft")
        self.white_patches_tint_label = create_text_box("white patches tint", (275, 335), (130, 40),
                                                        "#text_box_22_horizleft")
        self.tint_label = create_text_box("tint", (450, 335), (130, 40), "#text_box_22_horizleft")
        self.skin_label = create_text_box("skin", (625, 335), (130, 40), "#text_box_22_horizleft")
        self.eye_colour1_label = create_text_box("eye colour 1", (275, 420), (130, 40), "#text_box_22_horizleft")
        self.heterochromia_text = create_text_box("heterochromia", (465, 447), (130, 40), "#text_box_22_horizcenter")
        self.eye_colour2_label = create_text_box("eye colour 2", (625, 420), (130, 40), "#text_box_22_horizleft")
        self.accessory_label = create_text_box("accessory", (568, 495), (130, 40), "#text_box_22_horizleft")
        self.pose_label = create_text_box("pose", (406, 495), (110, 40), "#text_box_22_horizleft")
        self.reverse_label = create_text_box("reverse", (52, 495), (130, 40), "#text_box_22_horizleft")
        self.scar_message = create_text_box("Adding/removing scars will not affect a cat's conditions or history.",
                                            (52, 650), (500, 40), "#text_box_26_horizleft")
        self.scar1_label = create_text_box("scar 1", (56, 580), (130, 40), "#text_box_22_horizleft")
        self.scar2_label = create_text_box("scar 2", (242, 580), (130, 40), "#text_box_22_horizleft")
        self.scar3_label = create_text_box("scar 3", (428, 580), (130, 40), "#text_box_22_horizleft")
        self.scar4_label = create_text_box("scar 4", (614, 580), (130, 40), "#text_box_22_horizleft")

    def setup_buttons(self):
        self.previous_cat_button = create_button((25, 25), (153, 30), get_arrow(2, arrow_left=True) + " Previous Cat", ButtonStyles.SQUOVAL, sound_id="page_flip")
        self.back_button = create_button((25, 60), (105, 30), get_arrow(2) + " Back", ButtonStyles.SQUOVAL)
        self.next_cat_button = create_button((622, 25), (153, 30), "Next Cat " + get_arrow(3, arrow_left=False), ButtonStyles.SQUOVAL, sound_id="page_flip")
        self.pelt_length_left_button = create_button((224, 525), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pelt_length_right_button = create_button((324, 525), (30, 30), get_arrow(1, False),
                                                      ButtonStyles.ROUNDED_RECT)
        self.pose_left_button = create_button((406, 525), (30, 30), get_arrow(1), ButtonStyles.ROUNDED_RECT)
        self.pose_right_button = create_button((486, 525), (30, 30), get_arrow(1, False), ButtonStyles.ROUNDED_RECT)
        self.reverse_button = create_button((102, 525), (70, 30), "Reverse", ButtonStyles.ROUNDED_RECT)
        self.reset_button = create_button((0, 65), (105, 30), "Reset", ButtonStyles.SQUOVAL, {"centerx": "centerx"})

    def setup_dropdowns(self):
        self.pelt_name_dropdown = create_dropdown((275, 125), (130, 40),
                                                  create_options_list(self.pelt_names, "capitalize"),
                                                  get_selected_option(self.the_cat.pelt.name, "capitalize"))
        self.pelt_colour_dropdown = create_dropdown((450, 125), (130, 40),
                                                    create_options_list(self.pelt_colours, "upper"),
                                                    get_selected_option(self.the_cat.pelt.colour, "upper"))
        self.pattern_dropdown = create_dropdown((625, 125), (130, 40), create_options_list(self.patterns, "upper"),
                                                get_selected_option(self.the_cat.pelt.pattern, "upper"))
        self.tortie_base_dropdown = create_dropdown((275, 200), (130, 40),
                                                    create_options_list(self.tortie_bases, "lower"),
                                                    get_selected_option(self.the_cat.pelt.tortiebase, "lower"))
        self.tortie_colour_dropdown = create_dropdown((450, 200), (130, 40),
                                                      create_options_list(self.tortie_colours, "upper"),
                                                      get_selected_option(self.the_cat.pelt.tortiecolour, "upper"))
        self.tortie_pattern_dropdown = create_dropdown((625, 200), (130, 40),
                                                       create_options_list(self.tortie_bases, "lower"),
                                                       get_selected_option(self.the_cat.pelt.tortiepattern, "lower"))
        self.white_patches_dropdown = create_dropdown((275, 285), (130, 40),
                                                      create_options_list(self.white_patches, "upper"),
                                                      get_selected_option(self.the_cat.pelt.white_patches, "upper"))
        self.vitiligo_dropdown = create_dropdown((450, 285), (130, 40),
                                                 create_options_list(self.vitiligo_patterns, "upper"),
                                                 get_selected_option(self.the_cat.pelt.vitiligo, "upper"))
        self.points_dropdown = create_dropdown((625, 285), (130, 40),
                                               create_options_list(self.points_markings, "upper"),
                                               get_selected_option(self.the_cat.pelt.points, "upper"))
        self.white_patches_tint_dropdown = create_dropdown((275, 360), (130, 40),
                                                           create_options_list(self.white_patches_tints, "lower"),
                                                           get_selected_option(self.the_cat.pelt.white_patches_tint,
                                                                               "lower"))
        self.tint_dropdown = create_dropdown((450, 360), (130, 40), create_options_list(self.tints, "lower"),
                                             get_selected_option(self.the_cat.pelt.tint, "lower"))
        self.skin_dropdown = create_dropdown((625, 360), (130, 40), create_options_list(self.skins, "upper"),
                                             get_selected_option(self.the_cat.pelt.skin, "upper"))
        self.eye_colour1_dropdown = create_dropdown((295, 445), (130, 40),
                                                    create_options_list(self.eye_colours, "upper"),
                                                    get_selected_option(self.the_cat.pelt.eye_colour, "upper"))
        self.eye_colour2_dropdown = create_dropdown((645, 445), (130, 40),
                                                    create_options_list(self.eye_colours, "upper"), (
                                                        get_selected_option(self.the_cat.pelt.eye_colour2,
                                                                            "upper") if self.the_cat.pelt.eye_colour2 else get_selected_option(
                                                            self.the_cat.pelt.eye_colour, "upper")))
        self.accessory_dropdown = create_dropdown((568, 520), (180, 40), create_options_list(self.accessories, "upper"),
                                                  get_selected_option(self.the_cat.pelt.accessory, "upper"), "dropup")

        scars = self.the_cat.pelt.scars
        self.scar1_dropdown = create_dropdown((52, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars, "upper"), "dropup")
        self.scar2_dropdown = create_dropdown((238, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars[1:], "upper"), "dropup")
        self.scar3_dropdown = create_dropdown((424, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars[2:], "upper"), "dropup")
        self.scar4_dropdown = create_dropdown((610, 605), (135, 40), create_options_list(self.scars, "upper"),
                                              get_selected_option(scars[3:], "upper"), "dropup")

        self.initial_scar_selection[self.scar1_dropdown] = self.scar1_dropdown.selected_option[1]
        self.initial_scar_selection[self.scar2_dropdown] = self.scar2_dropdown.selected_option[1]
        self.initial_scar_selection[self.scar3_dropdown] = self.scar3_dropdown.selected_option[1]
        self.initial_scar_selection[self.scar4_dropdown] = self.scar4_dropdown.selected_option[1]

    def setup_cat(self):
        self.get_cat_age()
        self.make_cat_sprite()
        self.setup_cat_elements()

    def setup_next_and_previous_cat(self):
        if self.next_cat == 0:
            self.next_cat_button.disable()
        else:
            self.next_cat_button.enable()

        if self.previous_cat == 0:
            self.previous_cat_button.disable()
        else:
            self.previous_cat_button.enable()

    def setup_cat_elements(self):
        self.setup_pelt_length()
        self.setup_tortie()
        self.setup_white_patches_tint()
        self.setup_eye_colours()
        self.setup_accessory()
        self.setup_poses()
        self.setup_reverse()
        self.capture_initial_state()

    def setup_pelt_length(self):
        self.cat_elements["pelt_length_index"] = self.pelt_lengths.index(self.the_cat.pelt.length)
        self.update_pelt_length_display()

    def setup_tortie(self):
        if self.the_cat.pelt.name not in ["Calico", "Tortie"]:
            self.pattern_dropdown.disable()
            self.tortie_base_dropdown.disable()
            self.tortie_colour_dropdown.disable()
            self.tortie_pattern_dropdown.disable()

    def setup_white_patches_tint(self):
        if self.the_cat.pelt.white_patches is None and self.the_cat.pelt.points is None:
            self.white_patches_tint_dropdown.disable()

    def setup_eye_colours(self):
        if self.eye_colour2_dropdown.selected_option[1] == self.eye_colour1_dropdown.selected_option[1]:
            self.heterochromia = False
            self.eye_colour2_dropdown.disable()
        else:
            self.heterochromia = True
        self.make_heterochromia_checkbox()

    def setup_accessory(self):
        if self.life_stage == "newborn":
            self.accessory_dropdown.disable()

    def setup_poses(self):
        if self.life_stage == "newborn" or self.the_cat.pelt.paralyzed:
            self.pose_left_button.disable()
            self.pose_right_button.disable()
        self.set_poses()
        self.cat_elements["current_pose"] = self.the_cat.pelt.cat_sprites[self.life_stage]
        self.update_pose_display()

    def setup_reverse(self):
        self.cat_elements["reverse_value"] = self.the_cat.pelt.reverse
        self.update_reverse_display()

    def capture_initial_state(self):
        self.initial_state = {
            "name": self.the_cat.pelt.name,
            "colour": self.the_cat.pelt.colour,
            "length": self.the_cat.pelt.length,
            "pattern": self.the_cat.pelt.pattern,
            "tortiebase": self.the_cat.pelt.tortiebase,
            "tortiecolour": self.the_cat.pelt.tortiecolour,
            "tortiepattern": self.the_cat.pelt.tortiepattern,
            "white_patches": self.the_cat.pelt.white_patches,
            "vitiligo": self.the_cat.pelt.vitiligo,
            "points": self.the_cat.pelt.points,
            "white_patches_tint": self.the_cat.pelt.white_patches_tint,
            "tint": self.the_cat.pelt.tint,
            "skin": self.the_cat.pelt.skin,
            "eye_colour": self.the_cat.pelt.eye_colour,
            "eye_colour2": self.the_cat.pelt.eye_colour2,
            "accessory": self.the_cat.pelt.accessory,
            "scars": self.the_cat.pelt.scars.copy(),
            "reverse": self.the_cat.pelt.reverse,
            "pose": self.cat_elements["current_pose"],
            "cat_sprites": {
                "young_adult": self.the_cat.pelt.cat_sprites.get("young adult"),
                "adult": self.the_cat.pelt.cat_sprites.get("adult"),
                "senior_adult": self.the_cat.pelt.cat_sprites.get("senior adult")
            }
        }

    def reset_attributes(self):
        for attribute, value in self.initial_state.items():
            if attribute == "scars":
                self.the_cat.pelt.scars = value.copy()
            elif attribute == "pose":
                self.cat_elements["current_pose"] = value
                self.the_cat.pelt.cat_sprites[self.life_stage] = value
            elif attribute == "cat_sprites":
                self.the_cat.pelt.cat_sprites["young adult"] = value["young_adult"]
                self.the_cat.pelt.cat_sprites["adult"] = value["adult"]
                self.the_cat.pelt.cat_sprites["senior adult"] = value["senior_adult"]
            else:
                setattr(self.the_cat.pelt, attribute, value)
        self.update_ui_elements()

    def update_ui_elements(self):
        self.kill_cat_elements()
        self.kill_buttons()
        self.kill_dropdowns()
        self.setup_buttons()
        self.setup_dropdowns()
        self.setup_cat_elements()
        self.make_cat_sprite()

    def get_cat_age(self):
        self.life_stage = "adult" if self.the_cat.age in ["young adult", "adult", "senior adult"] else self.the_cat.age

    def make_cat_sprite(self):
        if "cat_image" in self.cat_elements:
            self.cat_elements["cat_image"].kill()
        self.cat_image = generate_sprite(self.the_cat, self.life_stage, False, False, True, True)
        self.cat_elements["cat_image"] = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((35, 160), (250, 250))),
            pygame.transform.scale(self.cat_image, ui_scale_dimensions((250, 250))),
            manager=MANAGER
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.previous_cat_button:
                if isinstance(Cat.fetch_cat(self.previous_cat), Cat):
                    game.switches["cat"] = self.previous_cat
                    self.kill_cat_elements()
                    self.kill_buttons()
                    self.kill_dropdowns()
                    self.build_cat_page()
                else:
                    print("invalid previous cat", self.previous_cat)
            elif event.ui_element == self.next_cat_button:
                if isinstance(Cat.fetch_cat(self.next_cat), Cat):
                    game.switches["cat"] = self.next_cat
                    self.kill_cat_elements()
                    self.kill_buttons()
                    self.kill_dropdowns()
                    self.build_cat_page()
                else:
                    print("invalid next cat", self.previous_cat)
            elif event.ui_element == self.back_button:
                self.handle_back_button()
            elif event.ui_element == self.reset_button:
                self.reset_attributes()
            elif event.ui_element in [self.pelt_length_left_button, self.pelt_length_right_button]:
                self.handle_pelt_length_buttons(event.ui_element)
            elif event.ui_element == self.heterochromia_checkbox:
                self.handle_heterochromia_checkbox()
            elif event.ui_element in [self.pose_left_button, self.pose_right_button]:
                self.handle_pose_buttons(event.ui_element)
            elif event.ui_element == self.reverse_button:
                self.change_reverse()
            self.print_pelt_attributes()  # for testing purposes
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.pelt_name_dropdown:
                self.handle_pelt_name_dropdown()
            elif event.ui_element == self.pelt_colour_dropdown:
                self.handle_dropdown_change(self.pelt_colour_dropdown, "colour")
            elif event.ui_element == self.pattern_dropdown:
                self.handle_dropdown_change(self.pattern_dropdown, "pattern")
            elif event.ui_element == self.tortie_base_dropdown:
                self.handle_dropdown_change(self.tortie_base_dropdown, "tortiebase")
            elif event.ui_element == self.tortie_colour_dropdown:
                self.handle_dropdown_change(self.tortie_colour_dropdown, "tortiecolour")
            elif event.ui_element == self.tortie_pattern_dropdown:
                self.handle_dropdown_change(self.tortie_pattern_dropdown, "tortiepattern")
            elif event.ui_element == self.white_patches_dropdown:
                self.handle_white_patches_dropdown()
            elif event.ui_element == self.vitiligo_dropdown:
                self.handle_vitiligo_dropdown()
            elif event.ui_element == self.points_dropdown:
                self.handle_points_dropdown()
            elif event.ui_element == self.white_patches_tint_dropdown:
                self.handle_dropdown_change(self.white_patches_tint_dropdown, "white_patches_tint")
            elif event.ui_element == self.tint_dropdown:
                self.handle_dropdown_change(self.tint_dropdown, "tint")
            elif event.ui_element == self.skin_dropdown:
                self.handle_dropdown_change(self.skin_dropdown, "skin")
            elif event.ui_element in [self.eye_colour1_dropdown, self.eye_colour2_dropdown]:
                self.handle_eye_colour_dropdown(event.ui_element)
            elif event.ui_element == self.accessory_dropdown:
                self.handle_accessory_dropdown()
            elif event.ui_element in [self.scar1_dropdown, self.scar2_dropdown, self.scar3_dropdown,
                                      self.scar4_dropdown]:
                self.handle_scar_dropdown(event.ui_element)
            self.print_pelt_attributes()  # for testing purposes

    def handle_dropdown_change(self, dropdown, attribute):
        selected_option = dropdown.selected_option[1]
        setattr(self.the_cat.pelt, attribute, selected_option)
        self.make_cat_sprite()

    def handle_back_button(self):
        if self.the_cat.pelt.eye_colour2 == self.the_cat.pelt.eye_colour:
            self.the_cat.pelt.eye_colour2 = None

        self.the_cat.pelt.scars = list(set(self.the_cat.pelt.scars))

        self.change_screen("profile screen")

    def handle_pelt_name_dropdown(self):
        self.the_cat.pelt.name = self.pelt_name_dropdown.selected_option[1]
        self.check_if_tortie()
        self.make_cat_sprite()

    def handle_pelt_length_buttons(self, button):
        direction = -1 if button == self.pelt_length_left_button else 1
        self.change_pelt_length(direction)

    def handle_white_patches_dropdown(self):
        selected_option = self.white_patches_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.white_patches = None
        else:
            self.the_cat.pelt.white_patches = selected_option[1]
        self.make_cat_sprite()
        self.check_white_patches_tint()

    def handle_vitiligo_dropdown(self):
        selected_option = self.vitiligo_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.vitiligo = None
        else:
            self.the_cat.pelt.vitiligo = selected_option[1]
        self.make_cat_sprite()

    def handle_points_dropdown(self):
        selected_option = self.points_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.points = None
        else:
            self.the_cat.pelt.points = selected_option[1]
        self.make_cat_sprite()
        self.check_white_patches_tint()

    def handle_eye_colour_dropdown(self, dropdown):
        if dropdown == self.eye_colour1_dropdown:
            self.the_cat.pelt.eye_colour = self.eye_colour1_dropdown.selected_option[1]
        else:
            self.the_cat.pelt.eye_colour2 = self.eye_colour2_dropdown.selected_option[1]
        self.make_cat_sprite()

    def handle_pose_buttons(self, button):
        direction = -1 if button == self.pose_left_button else 1
        self.change_pose(direction)

    def handle_accessory_dropdown(self):
        selected_option = self.accessory_dropdown.selected_option
        if selected_option[0] == "None":
            self.the_cat.pelt.accessory = None
        else:
            self.the_cat.pelt.accessory = selected_option[1]
        self.make_cat_sprite()

    def handle_scar_dropdown(self, dropdown):
        selected_option = dropdown.selected_option[1]
        previous_selection = self.previous_scar_selection.get(dropdown, self.initial_scar_selection[dropdown])

        if previous_selection != "NONE" and previous_selection in self.the_cat.pelt.scars:
            self.the_cat.pelt.scars.remove(previous_selection)

        if selected_option != "NONE":
            self.the_cat.pelt.scars.append(selected_option)

        self.previous_scar_selection[dropdown] = selected_option

        self.make_cat_sprite()

    def handle_sprites_for_pelt_length(self, previous_length):
        is_long_to_not_long = previous_length == "long" and self.the_cat.pelt.length != "long"
        is_not_long_to_long = previous_length != "long" and self.the_cat.pelt.length == "long"

        if is_long_to_not_long or is_not_long_to_long:
            self.set_poses()
            if self.life_stage != "newborn" and not self.the_cat.pelt.paralyzed:
                self.cat_elements["current_pose"] = self.poses[0]

            if self.life_stage == "adult":
                if not self.the_cat.pelt.paralyzed:
                    self.the_cat.pelt.cat_sprites["young adult"] = self.cat_elements["current_pose"]
                    self.the_cat.pelt.cat_sprites["adult"] = self.cat_elements["current_pose"]
                    self.the_cat.pelt.cat_sprites["senior adult"] = self.cat_elements["current_pose"]
                else:
                    random_adult_sprite = random.randint(6, 8) if previous_length == "long" else random.randint(9, 11)
                    self.the_cat.pelt.cat_sprites["young adult"] = random_adult_sprite
                    self.the_cat.pelt.cat_sprites["adult"] = random_adult_sprite
                    self.the_cat.pelt.cat_sprites["senior adult"] = random_adult_sprite
            else:
                random_adult_sprite = random.randint(6, 8) if previous_length == "long" else random.randint(9, 11)
                self.the_cat.pelt.cat_sprites["young adult"] = random_adult_sprite
                self.the_cat.pelt.cat_sprites["adult"] = random_adult_sprite
                self.the_cat.pelt.cat_sprites["senior adult"] = random_adult_sprite

            self.update_pose_display()
            self.make_cat_sprite()

    def change_pelt_length(self, direction):
        previous_length = self.the_cat.pelt.length
        self.cat_elements["pelt_length_index"] = (self.cat_elements["pelt_length_index"] + direction) % len(
            self.pelt_lengths)
        self.the_cat.pelt.length = self.pelt_lengths[self.cat_elements["pelt_length_index"]]
        self.update_pelt_length_display()
        self.handle_sprites_for_pelt_length(previous_length)

    def update_pelt_length_display(self):
        self.kill_cat_element("pelt_length")
        self.cat_elements["pelt_length"] = create_text_box(self.the_cat.pelt.length.lower(), (254, 528), (70, 40),
                                                           "#text_box_26_horizcenter")

    def check_if_tortie(self):
        dropdowns = [
            self.pattern_dropdown,
            self.tortie_base_dropdown,
            self.tortie_colour_dropdown,
            self.tortie_pattern_dropdown
        ]
        if self.the_cat.pelt.name in ["Calico", "Tortie"]:
            for dropdown in dropdowns:
                dropdown.kill()

            self.the_cat.pelt.pattern = self.patterns[0]
            self.the_cat.pelt.tortiebase = self.tortie_bases[0]
            self.the_cat.pelt.tortiecolour = self.tortie_colours[0]
            self.the_cat.pelt.tortiepattern = self.tortie_bases[0]

            self.pattern_dropdown = create_dropdown((625, 125), (130, 40), create_options_list(self.patterns, "upper"),
                                                    get_selected_option(self.the_cat.pelt.pattern, "upper"))
            self.tortie_base_dropdown = create_dropdown((275, 200), (130, 40),
                                                        create_options_list(self.tortie_bases, "lower"),
                                                        get_selected_option(self.the_cat.pelt.tortiebase, "lower"))
            self.tortie_colour_dropdown = create_dropdown((450, 200), (130, 40),
                                                          create_options_list(self.tortie_colours, "upper"),
                                                          get_selected_option(self.the_cat.pelt.tortiecolour, "upper"))
            self.tortie_pattern_dropdown = create_dropdown((625, 200), (130, 40),
                                                           create_options_list(self.tortie_bases, "lower"),
                                                           get_selected_option(self.the_cat.pelt.tortiepattern,
                                                                               "lower"))

        else:
            for dropdown in dropdowns:
                dropdown.kill()

            self.pattern_dropdown = create_dropdown((625, 125), (130, 40), "None", "None")
            self.tortie_base_dropdown = create_dropdown((275, 200), (130, 40), "None", "None")
            self.tortie_colour_dropdown = create_dropdown((450, 200), (130, 40), "None", "None")
            self.tortie_pattern_dropdown = create_dropdown((625, 200), (130, 40), "None", "None")

            self.the_cat.pelt.pattern = None
            self.the_cat.pelt.tortiebase = None
            self.the_cat.pelt.tortiecolour = None
            self.the_cat.pelt.tortiepattern = None

            for dropdown in [self.pattern_dropdown, self.tortie_base_dropdown, self.tortie_colour_dropdown,
                             self.tortie_pattern_dropdown]:
                dropdown.disable()

    def check_white_patches_tint(self):
        if self.the_cat.pelt.points is None and self.the_cat.pelt.white_patches is None:
            self.the_cat.pelt.white_patches_tint = "none"
            self.white_patches_tint_dropdown.kill()
            self.white_patches_tint_dropdown = create_dropdown((275, 300), (130, 40),
                                                               create_options_list(self.white_patches_tints, "lower"),
                                                               get_selected_option(self.the_cat.pelt.white_patches_tint,
                                                                                   "lower"))
            self.white_patches_tint_dropdown.disable()
        else:
            self.white_patches_tint_dropdown.enable()

    def make_heterochromia_checkbox(self):
        self.kill_cat_element("heterochromia_checkbox")
        checkbox_id = "@checked_checkbox" if self.heterochromia else "@unchecked_checkbox"
        self.heterochromia_checkbox = UIImageButton(
            ui_scale(pygame.Rect((465, 450), (30, 30))),
            "",
            object_id=checkbox_id,
            starting_height=2
        )
        self.cat_elements["heterochromia_checkbox"] = self.heterochromia_checkbox

    def handle_heterochromia_checkbox(self):
        self.heterochromia = not self.heterochromia
        if self.heterochromia:
            self.the_cat.pelt.eye_colour2 = self.eye_colour2_dropdown.selected_option[1]
            self.eye_colour2_dropdown.enable()
        else:
            self.the_cat.pelt.eye_colour2 = None
            self.eye_colour2_dropdown.kill()
            self.eye_colour2_dropdown = create_dropdown((645, 445), (130, 40),
                                                        create_options_list(self.eye_colours, "upper"), (
                                                            get_selected_option(self.the_cat.pelt.eye_colour2,
                                                                                "upper") if self.the_cat.pelt.eye_colour2 else get_selected_option(
                                                                self.the_cat.pelt.eye_colour, "upper")))
            self.eye_colour2_dropdown.disable()
        self.make_heterochromia_checkbox()
        self.make_cat_sprite()

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
            self.the_cat.pelt.cat_sprites["young adult"] = self.cat_elements["current_pose"]
            self.the_cat.pelt.cat_sprites["senior adult"] = self.cat_elements["current_pose"]
        self.update_pose_display()
        self.make_cat_sprite()

    def update_pose_display(self):
        self.kill_cat_element("pose")
        pose_text = "none" if (self.the_cat.pelt.paralyzed or self.life_stage == "newborn") else str(
            self.cat_elements["current_pose"])
        self.cat_elements["pose"] = create_text_box(pose_text, (436, 528), (50, 40), "#text_box_26_horizcenter")

    def change_reverse(self):
        self.the_cat.pelt.reverse = not self.the_cat.pelt.reverse
        self.update_reverse_display()
        self.make_cat_sprite()

    def update_reverse_display(self):
        self.kill_cat_element("reverse")
        reverse_text = "true" if self.the_cat.pelt.reverse else "false"
        self.cat_elements["reverse"] = create_text_box(reverse_text, (52, 528), (45, 40), "#text_box_26_horizcenter")

    def exit_screen(self):
        self.kill_cat_elements()
        self.kill_labels()
        self.kill_buttons()
        self.kill_dropdowns()
        self.frame_image.kill()

    def kill_cat_elements(self):
        elements_to_kill = [
            "cat_name", "cat_image", "pelt_length", "pose", "heterochromia_checkbox", "reverse"
        ]
        for element in elements_to_kill:
            self.kill_cat_element(element)

    def kill_cat_element(self, element_name):
        if element_name in self.cat_elements:
            self.cat_elements[element_name].kill()

    def kill_labels(self):
        labels = [
            self.pelt_name_label, self.pelt_colour_label, self.pelt_length_label,
            self.pattern_label, self.tortie_base_label, self.tortie_colour_label, self.tortie_pattern_label,
            self.white_patches_label, self.vitiligo_label, self.points_label, self.white_patches_tint_label,
            self.tint_label, self.skin_label, self.eye_colour1_label, self.eye_colour2_label, self.heterochromia_text,
            self.pose_label, self.reverse_label, self.accessory_label, self.scar_message, self.scar1_label,
            self.scar2_label, self.scar3_label, self.scar4_label
        ]
        for label in labels:
            label.kill()

    def kill_buttons(self):
        buttons = [
            self.previous_cat_button, self.back_button, self.next_cat_button, self.reset_button,
            self.pelt_length_left_button, self.pelt_length_right_button, self.pose_left_button,
            self.pose_right_button, self.reverse_button
        ]
        for button in buttons:
            button.kill()

    def kill_dropdowns(self):
        dropdowns = [
            self.pelt_name_dropdown, self.pelt_colour_dropdown, self.pattern_dropdown, self.tortie_base_dropdown,
            self.tortie_colour_dropdown, self.tortie_pattern_dropdown, self.white_patches_dropdown, self.vitiligo_dropdown,
            self.points_dropdown, self.skin_dropdown, self.white_patches_tint_dropdown, self.tint_dropdown,
            self.eye_colour1_dropdown, self.eye_colour2_dropdown, self.accessory_dropdown,
            self.scar1_dropdown, self.scar2_dropdown, self.scar3_dropdown, self.scar4_dropdown
        ]
        for dropdown in dropdowns:
            dropdown.kill()
