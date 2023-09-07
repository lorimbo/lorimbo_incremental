from __future__ import absolute_import
import imgui
import pygame.display
from pygame.locals import *

import tooltips
from Game_logic import Gamelogic
from tooltips import actionTooltip
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 100, 0)
grey = (105, 105, 105)
teal = (84, 186, 227)
brown = (139, 69, 19)
pink=(255, 161, 245)
mediumblue=(0,0,205)
violet=(188, 122, 249)
steelblue=(39,73,114)
beige=(245,245,220)
backgroundpink=(145,108,173)
buttoncolor=(82, 56, 116)
buttontextcolor=(173, 241, 130)
evangelionorange=(220, 125, 104)

def progressbardecorator(function):
    def inner1(*args,**kwargs):
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND,*[e / 255 for e in buttoncolor])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in evangelionorange])
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, *[e / 255 for e in buttontextcolor])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func
    return inner1


def backgroundecorator(function):
    def inner1(*args, **kwargs):
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *[e / 255 for e in backgroundpink])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND,*[e/255 for e in buttoncolor])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *[e/255 for e in buttoncolor])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED,*[e/255 for e in buttoncolor])
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *[e/255 for e in violet])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in buttontextcolor])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func

    return inner1
def actiondecorator(function):
    def inner1(*args,**kwargs):
        imgui.push_style_color(imgui.COLOR_BUTTON,*[e/255 for e in buttoncolor])
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED,*[e/255 for e in violet])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in buttontextcolor])
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE,*[e/255 for e in pink])
        imgui.push_style_color(imgui.COLOR_HEADER_HOVERED,*[e/255 for e in violet])
        func = function(*args,**kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func
    return inner1


def numcon(n):
    if n >= 10000000:
        return f'{round(n / 1000000, 1)}M'
    elif n >= 1000000:
        return f'{round(n / 1000000, 2)}M'
    elif n >= 100000:
        return f'{round(n / 1000, 0)}K'
    elif n >= 10000:
        return f'{round(n / 1000, 1)}K'
    elif n >= 1000:
        return f'{round(n / 1000, 2)}K'
    return str(round(n, 1))


class Graphics:
    flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE
    resourcesflags = imgui.WINDOW_NO_RESIZE
    Fonts = {'Helvetica': {}}
    heightfactor = 1
    widthfactor = 1
    fontfactor = 1
    toggles = {}
    beginbackground = backgroundecorator(imgui.begin)

    @classmethod
    def update_window_size(cls):
        size = list(pygame.display.get_window_size())
        cls.heightfactor = size[1] / 600
        cls.widthfactor = size[0] / 1500
        cls.fontfactor = min(cls.heightfactor, cls.widthfactor)

    @classmethod
    def resizeheight(cls, n):
        return round(cls.heightfactor * n, 0)

    @classmethod
    def resizewidth(cls, n):
        return round(cls.widthfactor * n, 0)
    @classmethod
    def notinusedecorator(cls, function, use):
        @actiondecorator
        def inner1(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.7)
            func = function(*args, **kwargs)
            imgui.pop_style_var(1)
            return func

        @actiondecorator
        def inner2(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 1)
            func = function(*args, **kwargs)
            imgui.pop_style_var(1)
            return func

        if use:
            return inner1
        else:
            return inner2

    @classmethod
    def disabledecorator(cls, function, use):
        @actiondecorator
        def inner1(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.5)
            func = function(*args, **kwargs)
            imgui.pop_style_var(1)

            return func
        @actiondecorator
        def inner2(*args,**kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 1)
            func = function(*args, **kwargs)
            imgui.pop_style_var(1)
            return func

        if use:
            return inner1
        else:
            return inner2

    @classmethod
    def draw_main_menu(cls):
        # Main menu
        visible = [e for e in Gamelogic.mainelements if e.isvisible]
        imgui.set_next_window_size(15 + cls.resizewidth(90),
                                   5 * (len(visible) - 1) + 18 + cls.resizeheight(30 * (len(visible) + 1)))
        imgui.set_next_window_position(cls.resizewidth(10), 0)
        cls.beginbackground('Main', False, cls.flags)
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            for button in visible:
                use = not Gamelogic.tab == button.name
                if cls.notinusedecorator(imgui.button, use)(button.name, cls.resizewidth(90), cls.resizeheight(30)):
                    Gamelogic.tab = button.name
            if actiondecorator(imgui.button)('Save', cls.resizewidth(90), cls.resizeheight(30)):
                Gamelogic.savegame()
        imgui.end()

    @classmethod
    def draw_main_submenu(cls):
        imgui.begin('Submenu')
        visible = [e for e in Gamelogic.mainsubelements if e.isvisible]
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            for button in visible:
                use = not Gamelogic.subtab == button.name
                if cls.notinusedecorator(imgui.button, use)(button.name, cls.resizewidth(90), cls.resizeheight(30)):
                    Gamelogic.subtab = button.name
        imgui.end()
    @classmethod
    def get_visible_elements(cls, list):
        return [e for e in list if e.isvisible]
    @classmethod
    def draw_instantactions(cls):
        finishline = cls.resizeheight(50)

        if 'instantactions' not in cls.toggles.keys():
            cls.toggles['instantactions'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(100)

        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(50 + cls.resizewidth(180), finishline
                                       )
        cls.beginbackground('Instantactions', False, cls.resourcesflags)
        for key in Gamelogic.instantactions:
            visible = cls.get_visible_elements(Gamelogic.instantactions[key])
            if not len(visible):
                continue
            if key not in cls.toggles['instantactions']:
                cls.toggles['instantactions'][key] = True

            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                if cls.toggles['instantactions'][key]:
                    direction = imgui.DIRECTION_DOWN
                else:
                    direction = imgui.DIRECTION_RIGHT
                if actiondecorator(imgui.arrow_button)(f'Toggle##{key}', direction):
                    cls.toggles['instantactions'][key] = not cls.toggles['instantactions'][key]
                imgui.same_line()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                actiondecorator(imgui.text)(f'{key}')
            if cls.toggles['instantactions'][key]:
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    for button in visible:
                        use = button.isdisabled
                        if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                   cls.resizeheight(50)) and not button.isdisabled:
                            Gamelogic.action = button.name
                        if imgui.is_item_hovered():
                            with imgui.begin_tooltip():
                                imgui.text(f"{button.name}")
                                tooltip = tooltips.actionTooltip(button.name, button.cost, button.complete)
                                for i in tooltip:
                                    imgui.text(f"{i}")
        imgui.end()
    @classmethod
    def draw_loopactions(cls):
        finishline = cls.resizeheight(50)
        if 'loopactions' not in cls.toggles.keys():
            cls.toggles['loopactions'] = {}
        height = list(pygame.display.get_window_size())[1]-cls.resizeheight(100)
        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(75 + cls.resizewidth(340), finishline
                                       )
        cls.beginbackground('Loopactions', False, cls.resourcesflags)

        for key in Gamelogic.loopactions:
            visible = cls.get_visible_elements(Gamelogic.loopactions[key])
            if not len(visible):
                continue
            if key not in cls.toggles['loopactions']:
                cls.toggles['loopactions'][key] = True
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                if cls.toggles['loopactions'][key]:
                    direction = imgui.DIRECTION_DOWN
                else:
                    direction = imgui.DIRECTION_RIGHT
                if actiondecorator(imgui.arrow_button)(f'Toggle##{key}', direction):
                    cls.toggles['loopactions'][key] = not cls.toggles['loopactions'][key]
                imgui.same_line()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                actiondecorator(imgui.text)(f'{key}')
            if cls.toggles['loopactions'][key]:
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    for button in visible:
                        use = button.isdisabled
                        if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                   cls.resizeheight(50)) and not button.isdisabled:
                            button.activation()
                        if imgui.is_item_hovered():
                            with imgui.begin_tooltip():
                                imgui.text(f"{button.name}")
                                tooltip = tooltips.loopTooltip(button.name, button.cost, button.complete,
                                                               button.progresscost,
                                                               button.progresseffect)
                                for i in tooltip:
                                    imgui.text(f"{i}")

                        progressbardecorator(imgui.progress_bar)(button.progress, (cls.resizewidth(160), cls.resizeheight(20)))
        imgui.end()
    @classmethod
    def draw_upgradeactions(cls):
        finishline = cls.resizeheight(50)

        if 'upgradeactions' not in cls.toggles.keys():
            cls.toggles['upgradeactions'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(100)
        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(100 + cls.resizewidth(500), finishline
                                       )
        cls.beginbackground('Upgradeactions', False, cls.resourcesflags)

        for key in Gamelogic.upgradeactions[Gamelogic.subtab]:
            visible = cls.get_visible_elements(Gamelogic.upgradeactions[Gamelogic.subtab][key])
            if not len(visible):
                continue
            if key not in cls.toggles['upgradeactions']:
                cls.toggles['upgradeactions'][key] = True

            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                if cls.toggles['upgradeactions'][key]:
                    direction = imgui.DIRECTION_DOWN
                else:
                    direction = imgui.DIRECTION_RIGHT
                if actiondecorator(imgui.arrow_button)(f'Toggle##{key}', direction):
                    cls.toggles['upgradeactions'][key] = not cls.toggles['upgradeactions'][key]
                imgui.same_line()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                actiondecorator(imgui.text)(f'{key}')
            if cls.toggles['upgradeactions'][key]:
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    for button in visible:
                        use = button.isdisabled
                        if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                   cls.resizeheight(50)) and not button.isdisabled:
                            Gamelogic.upgradeaction = button.name
                        if imgui.is_item_hovered():
                            with imgui.begin_tooltip():
                                imgui.text(f"{button.name}")
                                tooltip = tooltips.upgradeTooltip(button.name, button.cost, button.complete,
                                                                  button.requirements)
                                for i in tooltip:
                                    imgui.text(f"{i}")

        imgui.end()


    @classmethod
    def draw_area(cls):
        cls.draw_instantactions()
        cls.draw_loopactions()
        cls.draw_upgradeactions()

    @classmethod
    def draw_main(cls):
        visible = [e for e in Gamelogic.mainsubelements if e.isvisible]
        imgui.set_next_window_size(16 + cls.resizewidth(90),
                                   14 + cls.resizeheight(30 * len(visible)) + 5 * (len(visible) - 1))
        imgui.set_next_window_position(30 + cls.resizewidth(90), 0)
        cls.beginbackground('Submenu', False, cls.flags)
        imgui.end()
        cls.draw_main_submenu()
        cls.draw_area()


    @classmethod
    def draw_energies(cls):
        visible = [e for e in Gamelogic.energies if e.isvisible]
        imgui.set_next_window_size(cls.resizewidth(300), cls.resizeheight(37 * len(visible)))
        imgui.set_next_window_position(cls.resizewidth(660 + 540), 0)
        cls.beginbackground('Energies', False, cls.resourcesflags)
        draw_list = imgui.get_window_draw_list()
        num = 0
        for energy in visible:
            color = energy.color
            color = [c / 255 for c in color]
            draw_list.path_clear()
            draw_list.add_rect_filled(cls.resizewidth(1210), cls.resizeheight(30 + num * 25),
                                      cls.resizewidth(1210 + 270 * energy.quantity / energy.max),
                                      cls.resizeheight(50 + num * 25), imgui.get_color_u32_rgba(*color, 1), 0)
            mousepos = imgui.get_mouse_pos()

            if cls.resizewidth(1210) < mousepos[0] < cls.resizewidth(1210 + 270) and cls.resizeheight(30 + num * 25) < \
                    mousepos[1] < cls.resizeheight(50 + num * 25):
                with imgui.begin_tooltip():
                    imgui.text(f"{energy.name}")
                    tooltip = tooltips.energyTooltip(energy.name, energy.quantity, energy.max, energy.regen)
                    for i in tooltip:
                        imgui.text(f"{i}")
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                draw_list.add_text(cls.resizewidth(1220), cls.resizeheight(35 + num * 25),
                                   imgui.get_color_u32_rgba(*[e/255 for e in buttontextcolor], 1), energy.name)
                draw_list.add_text(cls.resizewidth(1320), cls.resizeheight(35 + num * 25),
                                   imgui.get_color_u32_rgba(*[e/255 for e in buttontextcolor], 1),
                                   str(round(energy.quantity, 1)) + '/' + str(
                                       round(energy.max, 0)))
                draw_list.path_rect(cls.resizewidth(1210), cls.resizeheight(30 + num * 25), cls.resizewidth(1210 + 270),
                                    cls.resizeheight(50 + num * 25))
            draw_list.path_stroke(imgui.get_color_u32_rgba(1, 1, 1, 1), flags=0, thickness=1)
            draw_list.path_clear()
            draw_list.path_line_to(cls.resizewidth(1210), cls.resizeheight(30 + num * 25))
            draw_list.path_line_to(cls.resizewidth(1210), cls.resizeheight(50 + num * 25))
            draw_list.path_stroke(imgui.get_color_u32_rgba(1, 1, 1, 1), flags=0, thickness=1)
            num += 1
        imgui.end()

    @classmethod
    def draw_resources(cls):
        windowheight = len(Gamelogic.resources)
        for category in Gamelogic.resources:
            for resource in Gamelogic.resources[category]:
                if resource.isvisible:
                    windowheight += 1
        if windowheight > 40:
            windowheight = 40
        visible = [e for e in Gamelogic.energies if e.isvisible]
        imgui.set_next_window_size(cls.resizewidth(300), 15 + cls.resizeheight(21 * windowheight))
        imgui.set_next_window_position(cls.resizewidth(1200), cls.resizeheight(37 * len(visible)))
        cls.beginbackground('Resources', False, cls.resourcesflags)
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            for key in Gamelogic.resources:
                if [e for e in Gamelogic.resources[key] if e.isvisible]:
                    if actiondecorator(imgui.tree_node)(key, imgui.TREE_NODE_DEFAULT_OPEN):
                        for subkey in Gamelogic.resources[key]:
                            if subkey.isvisible:
                                space = ''
                                numofspace = 20 - len(subkey.name)
                                if not numofspace:
                                    numofspace = 0
                                for i in range(numofspace):
                                    space += ' '

                                actiondecorator(imgui.text)(subkey.name + space + numcon(subkey.quantity) + '/' + numcon(subkey.max))
                                if imgui.is_item_hovered():
                                    with imgui.begin_tooltip():
                                        imgui.text(f"{subkey.name}")
                                        tooltip = tooltips.resourceTooltip(subkey.name, subkey.quantity, subkey.max)
                                        for i in tooltip:
                                            imgui.text(f"{i}")
                        imgui.tree_pop()
        imgui.end()

    @classmethod
    def draw_party_tabs(cls):
        imgui.set_next_window_size(48 + cls.resizewidth(600), 16 + cls.resizeheight(30))
        imgui.set_next_window_position(cls.resizewidth(330), 0)
        imgui.begin('Partytabs', False, cls.flags)
        visible = cls.get_visible_elements(Gamelogic.partyelements)
        for element in visible:
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                use = not Gamelogic.partysubtab == element.name
                if cls.notinusedecorator(imgui.button, use)(element.name, cls.resizewidth(120), cls.resizeheight(30)):
                    Gamelogic.partysubtab = element.name
                imgui.same_line()
        imgui.end()

    @classmethod
    def draw_Adventurer(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), cls.resizeheight(65))
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(30))
        imgui.begin('Adventurer', False, cls.flags)
        Stats = Gamelogic.corestats.finalstats()
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 30)}']):
            imgui.same_line(position=cls.resizewidth(150))
            imgui.text('[Core Stats]')
            imgui.same_line()
            for key in Stats:
                imgui.text(key + ':' + numcon(Stats[key]))
                imgui.same_line()
        imgui.end()

    @classmethod
    def draw_party_menu(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), 16 + cls.resizeheight(450))
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(95))
        imgui.begin('Partymenu', False, cls.flags)
        imgui.begin_child("Child 1", height=cls.resizeheight(150), border=True, flags=cls.resourcesflags)

        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.text(pokemon.name)
                imgui.same_line(position=cls.resizewidth(125))
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=cls.resizewidth(250))
                imgui.text(numcon(pokemon.actualhp))
                imgui.same_line(position=cls.resizewidth(350))
                imgui.text(numcon(pokemon.actualpatk))
                imgui.same_line(position=cls.resizewidth(450))
                imgui.text(numcon(pokemon.actualpdef))
                imgui.same_line(position=cls.resizewidth(550))
                imgui.text(numcon(pokemon.actualmatk))
                imgui.same_line(position=cls.resizewidth(650))
                imgui.text(numcon(pokemon.actualmdef))
                imgui.same_line(position=cls.resizewidth(750))
                use = num == 0
                if cls.disabledecorator(imgui.arrow_button, use)(f'downbutton##{num}', imgui.DIRECTION_UP):
                    Gamelogic.switch = num - 1

                imgui.same_line()
                use = num == len(Gamelogic.party) - 1
                if cls.disabledecorator(imgui.arrow_button, use)(f'upbutton##{num}', imgui.DIRECTION_DOWN):
                    Gamelogic.switch = num

                imgui.same_line()
                use = (pokemon.name == 'You')
                imgui.same_line(position=cls.resizewidth(850))
                if cls.disabledecorator(imgui.button, use)(f'Remove##{num}', width=cls.resizewidth(90)) and not use:
                    Gamelogic.remove = num

        imgui.end_child()
        imgui.begin_child("Child 2", height=cls.resizeheight(280), border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.text(pokemon.name)
                imgui.same_line(position=cls.resizewidth(125))
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=cls.resizewidth(250))
                imgui.text(numcon(pokemon.actualhp))
                imgui.same_line(position=cls.resizewidth(350))
                imgui.text(numcon(pokemon.actualpatk))
                imgui.same_line(position=cls.resizewidth(450))
                imgui.text(numcon(pokemon.actualpdef))
                imgui.same_line(position=cls.resizewidth(550))
                imgui.text(numcon(pokemon.actualmatk))
                imgui.same_line(position=cls.resizewidth(650))
                imgui.text(numcon(pokemon.actualmdef))
                use = not len(Gamelogic.party) < Gamelogic.partylenmax
                imgui.same_line(position=cls.resizewidth(850))
                if cls.disabledecorator(imgui.button, use)(f'Add##{num}', cls.resizewidth(90)) and not use:
                    Gamelogic.add = num

        imgui.end_child()
        imgui.end()

    @classmethod
    def draw_levelup_menu(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), cls.resizeheight(450))
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(95))
        imgui.begin('Levelupmenu', False, cls.flags)
        imgui.begin_child("Child 1", height=cls.resizeheight(150), border=True)
        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.text(pokemon.name)
                imgui.same_line(position=cls.resizewidth(150))
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=cls.resizewidth(280))
                if imgui.button(f'Summon##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Level', num]
                imgui.same_line(position=cls.resizewidth(530))
                use = not Gamelogic.physseeds.quantity
                if cls.disabledecorator(imgui.button, use)(f'Physical##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Physical', num]
                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.magicseeds.quantity
                if cls.disabledecorator(imgui.button, use)(f'Magical##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Magical', num]
                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.specialseeds.quantity
                if cls.disabledecorator(imgui.button, use)(f'Special##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Special', num]
            imgui.text('')
            imgui.same_line(position=cls.resizewidth(560))
            imgui.text(numcon(pokemon.phys) + '/' + numcon(pokemon.lvl))
            imgui.same_line(position=cls.resizewidth(690))
            imgui.text(numcon(pokemon.magic) + '/' + numcon(pokemon.lvl))
            imgui.same_line(position=cls.resizewidth(820))
            imgui.text(numcon(pokemon.special) + '/' + numcon(pokemon.lvl))

        imgui.end_child()
        imgui.begin_child("Child 2", height=cls.resizeheight(280), border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.text(pokemon.name)
                imgui.same_line(position=cls.resizewidth(150))
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=cls.resizewidth(280))

                if imgui.button(f'Summon##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Level', num]
                imgui.same_line(position=cls.resizewidth(530))

                use = not Gamelogic.physseeds.quantity
                if cls.disabledecorator(imgui.button, use)(f'Physical##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Physical', num]

                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.magicseeds.quantity
                if cls.disabledecorator(imgui.button, use)(f'Magical##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Magical', num]

                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.specialseeds.quantity
                if cls.disabledecorator(imgui.button, use)(f'Special##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Special', num]

            imgui.text('')
            imgui.same_line(position=cls.resizewidth(560))
            imgui.text(numcon(pokemon.phys) + '/' + numcon(pokemon.lvl))
            imgui.same_line(position=cls.resizewidth(690))
            imgui.text(numcon(pokemon.magic) + '/' + numcon(pokemon.lvl))
            imgui.same_line(position=cls.resizewidth(820))
            imgui.text(numcon(pokemon.special) + '/' + numcon(pokemon.lvl))

        imgui.end_child()

        imgui.end()




    @classmethod
    def creategui(cls):
        # window size thingy
        cls.update_window_size()

        # Main menu
        cls.draw_main_menu()
        cls.draw_energies()
        cls.draw_resources()

        # Submenu
        if Gamelogic.tab == Gamelogic.mainelements[0].name:
            cls.draw_main()
        if Gamelogic.tab == Gamelogic.mainelements[1].name:
            cls.draw_party_tabs()
            cls.draw_Adventurer()
            if Gamelogic.partysubtab == Gamelogic.partyelements[0].name:
                cls.draw_party_menu()
            elif Gamelogic.partysubtab == Gamelogic.partyelements[1].name:
                cls.draw_levelup_menu()
        if Gamelogic.tab == Gamelogic.mainelements[2].name:
            pass