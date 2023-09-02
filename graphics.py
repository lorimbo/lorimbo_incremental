from __future__ import absolute_import
import imgui

import tooltips
from Game_logic import Gamelogic
from tooltips import actionTooltip


class Graphics:
    flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE
    resourcesflags = imgui.WINDOW_NO_RESIZE
    new_font = None

    @classmethod
    def draw_main_menu(cls):
        # Main menu
        visible = [e for e in Gamelogic.mainelements if e.isvisible]
        imgui.set_next_window_size(105, 68 + 54 * len(visible))
        imgui.set_next_window_position(10, 0)
        imgui.begin('Main', False, cls.flags)
        for button in visible:
            if imgui.button(button.name, 90, 50):
                Gamelogic.tab = button.name

        if imgui.button('Save', 90, 50):
            Gamelogic.savegame()
        imgui.end()

    @classmethod
    def draw_main_submenu(cls):
        visible = [e for e in Gamelogic.mainsubelements if e.isvisible]
        for button in visible:
            if imgui.button(button.name, 90, 50):
                Gamelogic.subtab = button.name

    @classmethod
    def get_visible_elements(cls, list):
        return [e for e in list if e.isvisible]

    @classmethod
    def draw_area(cls):
        finishline=50
        for key in Gamelogic.instantactions:
            visible = cls.get_visible_elements(Gamelogic.instantactions[key])
            imgui.set_next_window_size(135, 34 + 54 * len(visible))
            imgui.set_next_window_position(230, finishline)
            imgui.begin(key, False, cls.resourcesflags)
            finishline += 34 + 54 * len(visible)
            for button in visible:
                if button.isdisabled:
                    imgui.push_style_var(imgui.STYLE_ALPHA, 0.2)
                if imgui.button(button.name, 120, 50) and not button.isdisabled:
                    Gamelogic.action = button.name
                if button.isdisabled:
                    imgui.pop_style_var(1)
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(f"{button.name}")
                        imgui.text(f"             ")
                        tooltip = tooltips.actionTooltip(button.name,button.cost,button.complete)
                        for i in tooltip:
                            imgui.text(f"{i}")
            imgui.end()
        finishline = 50
        for key in Gamelogic.loopactions:
            visible = cls.get_visible_elements(Gamelogic.loopactions[key])
            imgui.set_next_window_size(135, 34 + 77 * len(visible))
            imgui.set_next_window_position(375, finishline)
            imgui.begin(key, False, cls.resourcesflags)
            finishline+=34+77*len(visible)
            for button in visible:
                if button.isdisabled:
                    imgui.push_style_var(imgui.STYLE_ALPHA, 0.2)
                if imgui.button(button.name, 120, 50) and not button.isdisabled:
                    button.activation()
                if button.isdisabled:
                    imgui.pop_style_var(1)
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(f"{button.name}")
                        imgui.text(f"             ")
                        tooltip = tooltips.loopTooltip(button.name,button.cost,button.complete,button.progresscost,button.progresseffect)
                        for i in tooltip:
                            imgui.text(f"{i}")
                imgui.progress_bar(button.progress, (120, 20), 'Progress')
            imgui.end()
        finishline= 50
        for key in Gamelogic.upgradeactions[Gamelogic.subtab]:
            visible = cls.get_visible_elements(Gamelogic.upgradeactions[Gamelogic.subtab][key])
            if not len(visible):
                continue
            imgui.set_next_window_size(135, 34 + 54 * len(visible))
            imgui.set_next_window_position(520, finishline)
            imgui.begin(key, False, cls.resourcesflags)
            finishline+= 34 + 54 * len(visible)
            for button in visible:
                if button.isdisabled:
                    imgui.push_style_var(imgui.STYLE_ALPHA, 0.2)
                if imgui.button(button.name, 120, 50) and not button.isdisabled:
                    Gamelogic.upgradeaction = button.name
                if button.isdisabled:
                    imgui.pop_style_var(1)
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(f"{button.name}")
                        imgui.text(f"             ")
                        tooltip = tooltips.upgradeTooltip(button.name,button.cost,button.complete,button.requirements)
                        for i in tooltip:
                            imgui.text(f"{i}")


            imgui.end()

    @classmethod
    def draw_main(cls):
        visible = [e for e in Gamelogic.mainsubelements if e.isvisible]
        imgui.set_next_window_size(105, 14 + 54 * len(visible))
        imgui.set_next_window_position(120, 0)
        imgui.begin('Submenu', False, cls.flags)
        cls.draw_main_submenu()
        cls.draw_area()
        imgui.end()

    @classmethod
    def draw_energies(cls):
        imgui.set_next_window_size(230, 35 * len(Gamelogic.unlockedenergies))
        imgui.set_next_window_position(1200, 0)
        imgui.begin('Energies', False, cls.resourcesflags)
        draw_list = imgui.get_window_draw_list()
        num = 0
        for key in Gamelogic.unlockedenergies:
            color = Gamelogic.energies[key]['color']
            color = [c / 255 for c in color]
            draw_list.path_clear()
            draw_list.add_rect_filled(1210, 30 + num * 25,
                                      1210 + 190 * Gamelogic.energies[key]['current'] / Gamelogic.energies[key]['max'],
                                      50 + num * 25, imgui.get_color_u32_rgba(*color, 1), 0)
            draw_list.add_text(1220, 35 + num * 25, imgui.get_color_u32_rgba(1, 1, 1, 1), key)
            draw_list.add_text(1320, 35 + num * 25, imgui.get_color_u32_rgba(1, 1, 1, 1),
                               str(round(Gamelogic.energies[key]['current'], 1)) + '/' + str(
                                   round(Gamelogic.energies[key]['max'], 0)))
            draw_list.path_rect(1210, 30 + num * 25, 1210 + 190, 50 + num * 25)
            draw_list.path_stroke(imgui.get_color_u32_rgba(1, 1, 1, 1), flags=0, thickness=1)
            draw_list.path_clear()
            draw_list.path_line_to(1210, 30 + num * 25)
            draw_list.path_line_to(1210, 50 + num * 25)
            draw_list.path_stroke(imgui.get_color_u32_rgba(1, 1, 1, 1), flags=0, thickness=1)
            num += 1
        imgui.end()

    @classmethod
    def draw_resources(cls):
        windowheight = len(Gamelogic.resources)
        for key in Gamelogic.resources:
            for subkey in Gamelogic.resources[key]:
                if subkey.isvisible:
                    windowheight += 1
        if windowheight > 40:
            windowheight = 40
        imgui.set_next_window_size(230, 15 + 21 * windowheight)
        imgui.set_next_window_position(1200, 35 * len(Gamelogic.unlockedenergies))
        imgui.begin('Resources', False, cls.resourcesflags)
        for key in Gamelogic.resources:
            if [e for e in Gamelogic.resources[key] if e.isvisible]:
                if imgui.tree_node(key, imgui.TREE_NODE_DEFAULT_OPEN):
                    for subkey in Gamelogic.resources[key]:
                        if subkey.isvisible:
                            space = ''
                            numofspace = 20 - len(subkey.name)
                            if not numofspace:
                                numofspace = 0
                            for i in range(numofspace):
                                space += ' '
                            imgui.text(subkey.name + space + str(subkey.quantity) + '/' + str(subkey.max))

                    imgui.tree_pop()
        imgui.end()

    @classmethod

    def draw_party_tabs(cls):
        imgui.set_next_window_size(500, 70)
        imgui.set_next_window_position(400, 0)
        imgui.begin('Partytabs', False, cls.flags)
        visible = cls.get_visible_elements(Gamelogic.partyelements)
        for element in visible:
            if imgui.button(element.name,90,50):
                Gamelogic.partysubtab = element.name
            imgui.same_line()

        imgui.end()
    @classmethod
    def draw_party_menu(cls):
        imgui.set_next_window_size(1050, 800)
        imgui.set_next_window_position(120, 100)
        imgui.begin('Partymenu', False, cls.flags)
        imgui.begin_child("Child 1", height=320, border=True)
        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.new_font):
                imgui.text(pokemon.name)
                imgui.same_line(position=150)
                imgui.text(str(pokemon.lvl) + '/' + str(pokemon.maxlvl))
                imgui.same_line(position=225)
                imgui.text(str(pokemon.hp))
                imgui.same_line(position=300)
                imgui.text(str(pokemon.atk))
                imgui.same_line(position=375)
                imgui.text(str(pokemon.dif))
                imgui.same_line(position=450)
                imgui.text(str(pokemon.satk))
                imgui.same_line(position=525)
                imgui.text(str(pokemon.sdif))
                imgui.same_line(position=600)
                if imgui.arrow_button(f'downbutton##{num}', imgui.DIRECTION_UP):
                    Gamelogic.switch = num - 1
                imgui.same_line()
                if imgui.arrow_button(f'upbutton##{num}', imgui.DIRECTION_DOWN):
                    Gamelogic.switch = num
                imgui.same_line()
                if len(Gamelogic.party) > 1:
                    imgui.same_line(position=698)
                    if imgui.button(f'Remove##{num}', width=90):
                        Gamelogic.remove = num

        imgui.end_child()
        imgui.begin_child("Child 2", height=400, border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.new_font):
                imgui.text(pokemon.name)
                imgui.same_line(position=150)
                imgui.text(str(pokemon.lvl) + '/' + str(pokemon.maxlvl))
                imgui.same_line(position=225)
                imgui.text(str(pokemon.hp))
                imgui.same_line(position=300)
                imgui.text(str(pokemon.atk))
                imgui.same_line(position=375)
                imgui.text(str(pokemon.dif))
                imgui.same_line(position=450)
                imgui.text(str(pokemon.satk))
                imgui.same_line(position=525)
                imgui.text(str(pokemon.sdif))
                if len(Gamelogic.party) < Gamelogic.partylenmax:
                    imgui.same_line(position=698)
                    if imgui.button(f'Add##{num}', 90):
                        Gamelogic.add = num

        imgui.end_child()

        imgui.end()

    @classmethod
    def creategui(cls):

        # Main menu
        cls.draw_main_menu()
        cls.draw_energies()
        cls.draw_resources()

        # Submenu
        if Gamelogic.tab == Gamelogic.mainelements[0].name:
            cls.draw_main()
        if Gamelogic.tab == Gamelogic.mainelements[1].name:
            cls.draw_party_tabs()
            if Gamelogic.partysubtab == Gamelogic.partyelements[0].name:
                cls.draw_party_menu()

