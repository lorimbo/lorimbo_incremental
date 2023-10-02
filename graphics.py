from __future__ import absolute_import
import imgui
import pygame.display
from pygame.locals import *
import datetime

import tooltips
from Game_logic import Gamelogic
from tooltips import actionTooltip

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
orange = (255, 100, 0)
grey = (105, 105, 105)
teal = (84, 186, 227)
brown = (139, 69, 19)
pink = (255, 161, 245)
purple = (128, 0, 128)
mediumblue = (0, 0, 205)
violet = (188, 122, 249)
steelblue = (39, 73, 114)
beige = (245, 245, 220)
backgroundpink = (145, 108, 173)
buttoncolor = (82, 56, 116)
buttontextcolor = (173, 241, 130)
evangelionorange = (220, 125, 104)


def autospacer155(text):
    list = text.split(" ")
    output = ""
    n = 0
    for num, i in enumerate(list):
        if len(" ".join(list[n:num])) > 140:
            output += "\n"
            output += " ".join(list[n:num - 1])
            n = num - 1
        if num == len(list) - 1:
            output += "\n"
            output += " ".join(list[n:num + 1])
    return [output[1:]]


Themes = {
    'EVA': {'backgroundhovercolor': (188, 122, 249), 'menubackgroundcolor': (145, 108, 173),
            'buttoncolor': (82, 56, 116),
            'buttonhovercolor': (188, 122, 249),
            'buttontextcolor': (173, 241, 130), 'mainbackground': (220, 125, 104), 'buttonactivecolor': (255, 161, 245),
            'darkerbuttoncolor': (128, 0, 128)},
    'rey': {'backgroundhovercolor': (188, 122, 249), 'menubackgroundcolor': (117, 154, 180),
            'buttoncolor': (165, 189, 214),
            'buttonhovercolor': (203, 214, 215),
            'buttontextcolor': (75, 0, 130), 'mainbackground': (245, 189, 218), 'buttonactivecolor': (255, 255, 255),
            'darkerbuttoncolor': (128, 0, 128)},
    'asuka': {'backgroundhovercolor': (188, 122, 249), 'menubackgroundcolor': (156, 0, 0), 'buttoncolor': (56, 1, 7),
              'buttonhovercolor': (100, 0, 0),
              'buttontextcolor': (214, 92, 48), 'mainbackground': (166, 111, 140), 'buttonactivecolor': (255, 161, 245),
              'darkerbuttoncolor': (128, 0, 128)}
}

Popups = {1: "[TUTORIAL] Welcome to Yet another shitty game!.I'm Lorimbo, the author of the game. You can start your adventure by "
             "clicking on the 'Ponder the future' button in the 'Actions' section to gain some Fate. Fate is used as the "
             "main way of progressing through the storyline. Once you have 5 Fate click on the 'Talk to father 1/12' "
             "quest to complete it and proceed with the story ",
          2:"[TUTORIAL] You can use the longaction 'Rest' to regain Energy and keep grinding Fate. Longactions go on in the "
            "background while you do other things.",
          3:"[TUTORIAL] You have now unlocked new actions, together with the Wood resource, try to proceed with the quest",
          4:"[TUTORIAL] You have now unlocked your first dungeon!You can find it in the top right corner of the main section."
            "In the dungeon your party will fight monsters and bosses!Dungeons also keep going on in the background."
            "The dungeon progression status is indicated by the bar under it.If you defeat all the monsters in the dungeon or"
            "if your party is defeated the dungeon will restart automatically.You can quit the current dungeon by going into the "
            "'Dungeon tab in the left menu and pressing the 'Quit' button"
            "Dungeons' layout and monsters are randomly generated.Monsters drop seeds and other useful loot that you can"
            " use to become more powerful",
          5:"[TUTORIAL] Congratulation adventurer,you've gotten your first seed!In the 'Party' tab in the left menu you can use Fate to level up your character and"
            "seeds to improve your stats",
          6:"[TUTORIAL] In this dungeon you will find your first actual monsters, they have a chance to drop their souls, which you can use in the 'Party' tab to"
            " unlock them as party members and level them up.To do so,press the 'Summon' Button in the 'Level up' menu and then add them in the party in the 'Party selection menu"}
for e in Popups:
    Popups[e] = autospacer155(Popups[e])


def tooltipdecorator(function, theme):
    def inner1(*args, **kwargs):
        imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        return func

    return inner1


def progressbardecorator(function, theme):
    def inner1(*args, **kwargs):
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in Themes[theme]['mainbackground']])
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, *[e / 255 for e in Themes[theme]['buttontextcolor']])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func

    return inner1


def dropdowndecorator(function, theme):
    def inner1(*args, **kwargs):
        imgui.push_item_width(100)
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED,
                               *[e / 255 for e in Themes[theme]['buttonhovercolor']])
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON, *[e / 255 for e in Themes[theme]['darkerbuttoncolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in Themes[theme]['buttontextcolor']])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func

    return inner1


def sliderdecorator(function, theme):
    def inner1(*args, **kwargs):
        imgui.push_item_width(100)
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED,
                               *[e / 255 for e in Themes[theme]['buttonhovercolor']])
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON, *[e / 255 for e in Themes[theme]['darkerbuttoncolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in Themes[theme]['buttontextcolor']])
        imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, *[e / 255 for e in Themes[theme]['buttontextcolor']])
        imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, *[e / 255 for e in Themes[theme]['darkerbuttoncolor']])
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE,
                               *[e / 255 for e in Themes[theme]['buttonactivecolor']])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func

    return inner1


def backgroundecorator(function, theme):
    def inner1(*args, **kwargs):
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *[e / 255 for e in Themes[theme]['buttonhovercolor']])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in Themes[theme]['buttontextcolor']])
        imgui.push_style_color(imgui.COLOR_SCROLLBAR_BACKGROUND, *[e / 255 for e in Themes[theme]['buttonhovercolor']])
        imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_HOVERED, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])
        imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_ACTIVE, *[e / 255 for e in Themes[theme]['menubackgroundcolor']])



        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        imgui.pop_style_color(1)
        return func

    return inner1


def actiondecorator(function, theme):
    def inner1(*args, **kwargs):
        imgui.push_style_color(imgui.COLOR_BUTTON, *[e / 255 for e in Themes[theme]['buttoncolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *[e / 255 for e in Themes[theme]['buttonhovercolor']])
        imgui.push_style_color(imgui.COLOR_TEXT, *[e / 255 for e in Themes[theme]['buttontextcolor']])
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *[e / 255 for e in Themes[theme]['buttonactivecolor']])
        imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *[e / 255 for e in Themes[theme]['buttonhovercolor']])
        imgui.push_style_color(imgui.COLOR_HEADER_ACTIVE, *[e / 255 for e in Themes[theme]['buttonactivecolor']])
        func = function(*args, **kwargs)
        imgui.pop_style_color(1)
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
    theme = 'rey'

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
        def inner1(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.5)
            func = actiondecorator(function, cls.theme)(*args, **kwargs)
            imgui.pop_style_var(1)
            return func

        def inner2(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 1)
            func = actiondecorator(function, cls.theme)(*args, **kwargs)
            imgui.pop_style_var(1)
            return func

        if use:
            return inner1
        else:
            return inner2

    @classmethod
    def disabledecorator(cls, function, use):

        def inner1(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.3)
            func = actiondecorator(function, cls.theme)(*args, **kwargs)
            imgui.pop_style_var(1)

            return func

        def inner2(*args, **kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 1)
            func = actiondecorator(function, cls.theme)(*args, **kwargs)
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
        imgui.set_next_window_position(cls.resizewidth(10), cls.resizeheight(50))
        backgroundecorator(imgui.begin, cls.theme)('Main', False, cls.flags)
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            for button in visible:
                use = not Gamelogic.tab == button.name
                if cls.notinusedecorator(imgui.button, use)(button.name, cls.resizewidth(90), cls.resizeheight(30)):
                    Gamelogic.tab = button.name
            if actiondecorator(imgui.button, cls.theme)('Save', cls.resizewidth(90), cls.resizeheight(30)):
                Gamelogic.savegame()
                pass

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
        if 'areainstants' not in cls.toggles.keys():
            cls.toggles['areainstants'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(150)

        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(50 + cls.resizewidth(180), finishline
                                       )
        backgroundecorator(imgui.begin, cls.theme)('Actions', False, cls.resourcesflags)
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
                if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle##{key}', direction):
                    cls.toggles['instantactions'][key] = not cls.toggles['instantactions'][key]
                imgui.same_line()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                actiondecorator(imgui.text, cls.theme)(f'{key}')
            if cls.toggles['instantactions'][key]:
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    for button in visible:
                        use = button.isdisabled
                        if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                   cls.resizeheight(50)) and not button.isdisabled:
                            Gamelogic.action = button.name
                        if imgui.is_item_hovered():
                            with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                actiondecorator(imgui.text, cls.theme)(f"{button.name}")
                                tooltip = tooltips.actionTooltip(button.name, button.cost, button.complete)
                                for i in tooltip:
                                    actiondecorator(imgui.text, cls.theme)(f"{i}")

        if Gamelogic.subtab in Gamelogic.areainstants.keys():
            visible = cls.get_visible_elements(Gamelogic.areainstants[Gamelogic.subtab])
            if len(visible):
                if 'Area actions' not in cls.toggles['areainstants']:
                    cls.toggles['areainstants']['Area actions'] = True

                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                    if cls.toggles['areainstants']['Area actions']:
                        direction = imgui.DIRECTION_DOWN
                    else:
                        direction = imgui.DIRECTION_RIGHT
                    if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle', direction):
                        cls.toggles['areainstants']['Area actions'] = not cls.toggles['areainstants']['Area actions']
                    imgui.same_line()
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    actiondecorator(imgui.text, cls.theme)(f'Area actions')
                if cls.toggles['areainstants']['Area actions']:
                    with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                        for button in visible:
                            use = button.isdisabled
                            if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                       cls.resizeheight(50)) and not button.isdisabled:
                                Gamelogic.action = button.name
                            if imgui.is_item_hovered():
                                with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                    actiondecorator(imgui.text, cls.theme)(f"{button.name}")
                                    tooltip = tooltips.actionTooltip(button.name, button.cost, button.complete)
                                    for i in tooltip:
                                        actiondecorator(imgui.text, cls.theme)(f"{i}")
        imgui.end()

    @classmethod
    def draw_longactions(cls):
        finishline = cls.resizeheight(50)
        if 'longactions' not in cls.toggles.keys():
            cls.toggles['longactions'] = {}
        if 'arealongs' not in cls.toggles.keys():
            cls.toggles['arealongs'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(150)
        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(75 + cls.resizewidth(340), finishline
                                       )
        backgroundecorator(imgui.begin, cls.theme)('Long actions', False, cls.resourcesflags)

        for key in Gamelogic.longactions:
            visible = cls.get_visible_elements(Gamelogic.longactions[key])
            if not len(visible):
                continue
            if key not in cls.toggles['longactions']:
                cls.toggles['longactions'][key] = True
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                if cls.toggles['longactions'][key]:
                    direction = imgui.DIRECTION_DOWN
                else:
                    direction = imgui.DIRECTION_RIGHT
                if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle##{key}', direction):
                    cls.toggles['longactions'][key] = not cls.toggles['longactions'][key]
                imgui.same_line()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                actiondecorator(imgui.text, cls.theme)(f'{key}')
            if cls.toggles['longactions'][key]:
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    for button in visible:
                        use = button.isdisabled
                        if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                   cls.resizeheight(50)) and not button.isdisabled:
                            if button.name=='Rest':
                                for key in Gamelogic.longactions:
                                    for e in Gamelogic.longactions[key]:
                                        e.previouslyactive= False
                                for subtab in Gamelogic.mainsubelements:
                                    if subtab.name in Gamelogic.arealongs:
                                        for e in Gamelogic.arealongs[subtab.name]:
                                            e.previouslyactive = False
                            button.activation()
                        if imgui.is_item_hovered():
                            with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                actiondecorator(imgui.text, cls.theme)(f"{button.name}")
                                tooltip = tooltips.loopTooltip(button.name, button.cost, button.complete,
                                                               button.progresscost,
                                                               button.progresseffect)
                                for i in tooltip:
                                    actiondecorator(imgui.text, cls.theme)(f"{i}")

                        progressbardecorator(imgui.progress_bar, cls.theme)(button.progress,
                                                                            (
                                                                                cls.resizewidth(160),
                                                                                cls.resizeheight(20)))
        if Gamelogic.subtab in Gamelogic.arealongs.keys():
            visible = cls.get_visible_elements(Gamelogic.arealongs[Gamelogic.subtab])
            if len(visible):
                if 'Area actions' not in cls.toggles['arealongs']:
                    cls.toggles['arealongs']['Area actions'] = True
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                    if cls.toggles['arealongs']['Area actions']:
                        direction = imgui.DIRECTION_DOWN
                    else:
                        direction = imgui.DIRECTION_RIGHT
                    if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle', direction):
                        cls.toggles['arealongs']['Area actions'] = not cls.toggles['arealongs']['Area actions']
                    imgui.same_line()
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    actiondecorator(imgui.text, cls.theme)(f'Area actions')
                if cls.toggles['arealongs']['Area actions']:
                    with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                        for button in visible:
                            use = button.isdisabled
                            if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                       cls.resizeheight(50)) and not button.isdisabled:
                                button.activation()
                            if imgui.is_item_hovered():
                                with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                    actiondecorator(imgui.text, cls.theme)(f"{button.name}")
                                    tooltip = tooltips.loopTooltip(button.name, button.cost, button.complete,
                                                                   button.progresscost,
                                                                   button.progresseffect)
                                    for i in tooltip:
                                        actiondecorator(imgui.text, cls.theme)(f"{i}")

                            progressbardecorator(imgui.progress_bar, cls.theme)(button.progress,
                                                                                (
                                                                                    cls.resizewidth(160),
                                                                                    cls.resizeheight(20)))
        imgui.end()

    @classmethod
    def draw_proceedactions(cls):
        if 'proceedactions' not in cls.toggles.keys():
            cls.toggles['proceedactions'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(150)
        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(125 + cls.resizewidth(660), cls.resizeheight(50)
                                       )
        backgroundecorator(imgui.begin, cls.theme)('Proceed', False, cls.resourcesflags)
        if Gamelogic.subtab in Gamelogic.proceedactions:
            visible = cls.get_visible_elements(Gamelogic.proceedactions[Gamelogic.subtab])
            if Gamelogic.subtab not in cls.toggles['proceedactions']:
                cls.toggles['proceedactions'][Gamelogic.subtab] = True
            if len(visible):
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                    if cls.toggles['proceedactions'][Gamelogic.subtab]:
                        direction = imgui.DIRECTION_DOWN
                    else:
                        direction = imgui.DIRECTION_RIGHT
                    if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle##{Gamelogic.subtab}', direction):
                        cls.toggles['proceedactions'][Gamelogic.subtab] = not cls.toggles['proceedactions'][Gamelogic.subtab]
                    imgui.same_line()
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    actiondecorator(imgui.text, cls.theme)(f'{Gamelogic.subtab}')
            if cls.toggles['proceedactions'][Gamelogic.subtab]:
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    for button in visible:
                        use = button.isdisabled
                        if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                   cls.resizeheight(50)) and not button.isdisabled:
                            Gamelogic.action = button.name
                        if imgui.is_item_hovered():
                            with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                actiondecorator(imgui.text, cls.theme)(f"{button.name}")
                                tooltip = tooltips.questTooltip(button.name, button.cost, button.complete,[['Wood',0,0,0]]
                                                                  )
                                for i in tooltip:
                                    actiondecorator(imgui.text, cls.theme)(f"{i}")
        imgui.end()
    @classmethod
    def draw_quests(cls):
        finishline = cls.resizeheight(50)

        if 'quests' not in cls.toggles.keys():
            cls.toggles['quests'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(150)
        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(100 + cls.resizewidth(500), finishline
                                       )
        backgroundecorator(imgui.begin, cls.theme)('Quests', False, cls.resourcesflags)
        if Gamelogic.subtab in Gamelogic.quests:
            for key in Gamelogic.quests[Gamelogic.subtab]:
                visible = cls.get_visible_elements(Gamelogic.quests[Gamelogic.subtab][key])
                if not len(visible):
                    continue
                if key not in cls.toggles['quests']:
                    cls.toggles['quests'][key] = True

                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                    if cls.toggles['quests'][key]:
                        direction = imgui.DIRECTION_DOWN
                    else:
                        direction = imgui.DIRECTION_RIGHT
                    if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle##{key}', direction):
                        cls.toggles['quests'][key] = not cls.toggles['quests'][key]
                    imgui.same_line()
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    actiondecorator(imgui.text, cls.theme)(f'{key}')
                if cls.toggles['quests'][key]:
                    with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                        for button in visible:
                            use = button.isdisabled
                            if cls.disabledecorator(imgui.button, use)(button.name, cls.resizewidth(160),
                                                                       cls.resizeheight(50)) and not button.isdisabled:
                                Gamelogic.quest = button.name
                            if imgui.is_item_hovered():
                                with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                    actiondecorator(imgui.text, cls.theme)(f"{button.name}")
                                    tooltip = tooltips.questTooltip(button.name, button.cost, button.complete,
                                                                      button.requirements)
                                    for i in tooltip:
                                        actiondecorator(imgui.text, cls.theme)(f"{i}")

        imgui.end()

    @classmethod
    def draw_dungeons(cls):
        finishline = cls.resizeheight(50)
        if 'dungeons' not in cls.toggles.keys():
            cls.toggles['dungeons'] = {}
        height = list(pygame.display.get_window_size())[1] - cls.resizeheight(150)
        imgui.set_next_window_size(16 + cls.resizewidth(160),
                                   height)
        imgui.set_next_window_position(150 + cls.resizewidth(820), finishline
                                       )
        backgroundecorator(imgui.begin, cls.theme)('Dungeons', False, cls.resourcesflags)
        if Gamelogic.subtab in Gamelogic.dungeons.keys():
            for key in Gamelogic.dungeons[Gamelogic.subtab]:
                visible = cls.get_visible_elements(Gamelogic.dungeons[Gamelogic.subtab][key])
                if not len(visible):
                    continue
                if key not in cls.toggles['dungeons']:
                    cls.toggles['dungeons'][key] = True

                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.resizeheight(10))}']):
                    if cls.toggles['dungeons'][key]:
                        direction = imgui.DIRECTION_DOWN
                    else:
                        direction = imgui.DIRECTION_RIGHT
                    if actiondecorator(imgui.arrow_button, cls.theme)(f'Toggle##{key}', direction):
                        cls.toggles['dungeons'][key] = not cls.toggles['dungeons'][key]
                    imgui.same_line()
                with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                    actiondecorator(imgui.text, cls.theme)(f'{key}')

                if cls.toggles['dungeons'][key]:
                    with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                        for dungeon in visible:
                            use = dungeon.isdisabled
                            if cls.disabledecorator(imgui.button, use)(dungeon.name, cls.resizewidth(160),
                                                                       cls.resizeheight(50)) and not dungeon.isdisabled:
                                if Gamelogic.activedungeon is None or not Gamelogic.activedungeon.name == dungeon.name:
                                    dungeon.generate()
                                Gamelogic.activedungeon = dungeon
                                Gamelogic.activepartypokemon = 0
                                Gamelogic.activeenemypokemon = 0
                                Gamelogic.tab = 'Dungeon'
                            if dungeon == Gamelogic.activedungeon:
                                progressbardecorator(imgui.progress_bar, cls.theme)(
                                    (Gamelogic.activedungeon.floor + 1) / len(Gamelogic.activedungeon.currentlayout),
                                    (cls.resizewidth(160), cls.resizeheight(20)),
                                    f'({Gamelogic.activedungeon.floor + 1}/{len(Gamelogic.activedungeon.currentlayout)})')
                            else:
                                progressbardecorator(imgui.progress_bar, cls.theme)(0, (
                                    cls.resizewidth(160), cls.resizeheight(20)))

        imgui.end()

    @classmethod
    def draw_area(cls):
        cls.draw_instantactions()
        cls.draw_longactions()
        cls.draw_quests()
        cls.draw_proceedactions()
        cls.draw_dungeons()

    @classmethod
    def draw_main(cls):
        visible = [e for e in Gamelogic.mainsubelements if e.isvisible]
        imgui.set_next_window_size(16 + cls.resizewidth(90),
                                   16 + cls.resizeheight(30 * len(visible)) + 5 * (len(visible) - 1))
        imgui.set_next_window_position(30 + cls.resizewidth(90), cls.resizeheight(50))
        backgroundecorator(imgui.begin, cls.theme)('Submenu', False, cls.flags)
        imgui.end()
        cls.draw_main_submenu()
        cls.draw_area()

    @classmethod
    def draw_energies(cls):
        visible = [e for e in Gamelogic.energies if e.isvisible]
        imgui.set_next_window_size(cls.resizewidth(300),
                                   5 * len(visible) + cls.resizeheight(50) + cls.resizeheight(20 * len(visible)))
        imgui.set_next_window_position(cls.resizewidth(660 + 540), 0)
        backgroundecorator(imgui.begin, cls.theme)('Energies', False, cls.resourcesflags)
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
                with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                    actiondecorator(imgui.text, cls.theme)(f"{energy.name}")
                    tooltip = tooltips.energyTooltip(energy.name, energy.quantity, energy.max, energy.regen)
                    for i in tooltip:
                        actiondecorator(imgui.text, cls.theme)(f"{i}")
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
                draw_list.add_text(cls.resizewidth(1220), cls.resizeheight(35 + num * 25),
                                   imgui.get_color_u32_rgba(*[e / 255 for e in Themes[cls.theme]['buttontextcolor']],
                                                            1), energy.name)
                draw_list.add_text(cls.resizewidth(1320), cls.resizeheight(35 + num * 25),
                                   imgui.get_color_u32_rgba(*[e / 255 for e in Themes[cls.theme]['buttontextcolor']],
                                                            1),
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
        imgui.set_next_window_size(cls.resizewidth(300), list(pygame.display.get_window_size())[1] - (
                5 * len(visible) + cls.resizeheight(50) + cls.resizeheight(20 * len(visible))))
        imgui.set_next_window_position(cls.resizewidth(1200),
                                       5 * len(visible) + cls.resizeheight(50) + cls.resizeheight(20 * len(visible)))
        backgroundecorator(imgui.begin, cls.theme)('Resources', False, cls.resourcesflags)
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            for key in Gamelogic.resources:
                if [e for e in Gamelogic.resources[key] if e.isvisible]:
                    if actiondecorator(imgui.tree_node, cls.theme)(key, imgui.TREE_NODE_DEFAULT_OPEN):
                        for subkey in Gamelogic.resources[key]:
                            if subkey.isvisible:
                                space = ''
                                numofspace = 20 - len(subkey.name)
                                if not numofspace:
                                    numofspace = 0
                                for i in range(numofspace):
                                    space += ' '

                                actiondecorator(imgui.text, cls.theme)(
                                    subkey.name + space + numcon(subkey.quantity) + '/' + numcon(subkey.max))
                                if imgui.is_item_hovered():
                                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                                        actiondecorator(imgui.text, cls.theme)(f"{subkey.name}")
                                        tooltip = tooltips.resourceTooltip(subkey.name, subkey.quantity, subkey.max)
                                        for i in tooltip:
                                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                        imgui.tree_pop()
        imgui.end()

    @classmethod
    def draw_party_tabs(cls):
        imgui.set_next_window_size(48 + cls.resizewidth(600), 16 + cls.resizeheight(30))
        imgui.set_next_window_position(cls.resizewidth(330), cls.resizeheight(50))
        backgroundecorator(imgui.begin, cls.theme)('Partytabs', False, cls.flags)
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
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(80))
        backgroundecorator(imgui.begin, cls.theme)('Adventurer', False, cls.flags)
        Stats = Gamelogic.corestats.finalstats()
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 30)}']):
            imgui.same_line(position=cls.resizewidth(150))
            actiondecorator(imgui.text, cls.theme)('[Core Stats]')
            imgui.same_line()
            for key in Stats:
                actiondecorator(imgui.text, cls.theme)(key + ':' + numcon(Stats[key]))
                imgui.same_line()
        imgui.end()

    @classmethod
    def draw_party_menu(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), 16 + cls.resizeheight(335))
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(145))
        backgroundecorator(imgui.begin, cls.theme)('Partymenu', False, cls.flags)
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
            actiondecorator(imgui.text,cls.theme)('Templates')
            imgui.same_line()
            for num,template in enumerate(Gamelogic.templates):
                if actiondecorator(imgui.button,cls.theme)(f'{num}  ',cls.resizewidth(20),cls.resizeheight(20))and Gamelogic.templates[num]!=[]:
                    Gamelogic.changetemplateto(num)
                if template != []:
                    if imgui.is_item_hovered():
                        with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                            tooltip = tooltips.templatetooltip(template[0])
                            for i in tooltip:
                                actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line()
        imgui.new_line()
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 40)}']):
            actiondecorator(imgui.text, cls.theme)('Party')
        imgui.begin_child("Child 1", height=cls.resizeheight(80), border=True, flags=cls.resourcesflags)

        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                actiondecorator(imgui.text, cls.theme)(pokemon.name)
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(125))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(250))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualhp))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(350))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualpatk))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(450))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualpdef))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(550))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualmatk))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(650))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualmdef))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(750))
                use = num == 0
                if cls.disabledecorator(imgui.arrow_button, use)(f'downbutton##{num}', imgui.DIRECTION_UP):
                    Gamelogic.switch = num - 1
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

                imgui.same_line()
                use = num == len(Gamelogic.party) - 1
                if cls.disabledecorator(imgui.arrow_button, use)(f'upbutton##{num}', imgui.DIRECTION_DOWN):
                    Gamelogic.switch = num
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(840))
                if cls.disabledecorator(imgui.button, False)(f'Skill##{num}', width=cls.resizewidth(90)):
                    Gamelogic.changeskill = Gamelogic.party[num]
                    Gamelogic.partysubtab='Skill'
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")


                use = (pokemon.name == 'You')
                imgui.same_line(position=cls.resizewidth(940))
                if cls.disabledecorator(imgui.button, use)(f'Remove##{num}', width=cls.resizewidth(90)) and not use:
                    Gamelogic.remove = num
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

        imgui.end_child()
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 40)}']):
            actiondecorator(imgui.text, cls.theme)('Reserve')
        imgui.begin_child("Child 2", height=cls.resizeheight(140), border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                actiondecorator(imgui.text, cls.theme)(pokemon.name)
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(125))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(250))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualhp))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(350))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualpatk))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(450))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualpdef))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(550))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualmatk))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(650))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.actualmdef))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                use = not len(Gamelogic.party) < Gamelogic.partylenmax
                imgui.same_line(position=cls.resizewidth(850))
                if cls.disabledecorator(imgui.button, use)(f'Add##{num}', cls.resizewidth(90)) and not use:
                    Gamelogic.add = num
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

        imgui.end_child()
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
            if actiondecorator(imgui.button,cls.theme)('Save template',cls.resizewidth(150),cls.resizeheight(20)):
                Gamelogic.savingtotemplates=not Gamelogic.savingtotemplates
            imgui.same_line()
            if Gamelogic.savingtotemplates:
                actiondecorator(imgui.text,cls.theme)('Save to')
                imgui.same_line()
                for i in range(len(Gamelogic.templates)):
                    if actiondecorator(imgui.button,cls.theme)(f'{i} ',cls.resizewidth(20),cls.resizeheight(20)):
                        Gamelogic.templates[i]=[]
                        partycopy=[i.copy() for i in Gamelogic.party]
                        reservecopy = [i.copy() for i in Gamelogic.reserve]
                        Gamelogic.templates[i].append(partycopy)
                        Gamelogic.templates[i].append(reservecopy)


                    imgui.same_line()
        imgui.end()

    @classmethod
    def draw_levelup_menu(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), 16 + cls.resizeheight(335))
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(145))
        backgroundecorator(imgui.begin, cls.theme)('Levelupmenu', False, cls.flags)
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 40)}']):
            actiondecorator(imgui.text, cls.theme)('Party')
        imgui.begin_child("Child 1", height=cls.resizeheight(110), border=True)
        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if pokemon.name == 'You':
                    text10 = f'1 fate:({numcon(Gamelogic.fate.quantity)})'
                else:
                    text10 = f'1 {pokemon.name} soul ({numcon(Gamelogic.souls[pokemon.name])})'
                actiondecorator(imgui.text, cls.theme)(pokemon.name)
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party', text10)
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(150))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party', text10)
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(280))
                if pokemon.name == 'You':
                    use = not Gamelogic.fate.quantity or pokemon.lvl >= pokemon.maxlvl
                elif pokemon.name in Gamelogic.souls:
                    use = not Gamelogic.souls[pokemon.name] or pokemon.lvl >= pokemon.maxlvl
                else:
                    use = True
                if cls.disabledecorator(imgui.button, use)(f'Summon##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Level', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party', text10)
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(530))
                use = not Gamelogic.physgems.quantity or pokemon.phys >= pokemon.lvl
                if cls.disabledecorator(imgui.button, use)(f'Physical##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Physical', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party',
                                                          f'1 physical gem:({numcon(Gamelogic.physgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.magicgems.quantity or pokemon.magic >= pokemon.lvl
                if cls.disabledecorator(imgui.button, use)(f'Magical##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Magical', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party',
                                                          f'1 magical gem:({numcon(Gamelogic.magicgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.specialgems.quantity or pokemon.special >= pokemon.lvl
                if cls.disabledecorator(imgui.button, use)(f'Special##{num}', 90):
                    Gamelogic.levelup = ['Party', 'Special', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party',
                                                          f'1 special gem:({numcon(Gamelogic.specialgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
            imgui.text('')
            imgui.same_line(position=cls.resizewidth(560))
            actiondecorator(imgui.text, cls.theme)(numcon(pokemon.phys) + '/' + numcon(pokemon.lvl))
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party',
                                                          f'1 physical gem:({numcon(Gamelogic.physgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
            imgui.same_line(position=cls.resizewidth(690))
            actiondecorator(imgui.text, cls.theme)(numcon(pokemon.magic) + '/' + numcon(pokemon.lvl))
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party',
                                                          f'1 magical gem:({numcon(Gamelogic.magicgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
            imgui.same_line(position=cls.resizewidth(820))
            actiondecorator(imgui.text, cls.theme)(numcon(pokemon.special) + '/' + numcon(pokemon.lvl))
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'In the party',
                                                          f'1 special gem:({numcon(Gamelogic.specialgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

        imgui.end_child()
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 40)}']):
            actiondecorator(imgui.text, cls.theme)('Reserve')
        imgui.begin_child("Child 2", height=cls.resizeheight(170), border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                actiondecorator(imgui.text, cls.theme)(pokemon.name)
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free',
                                                          f'1 {pokemon.name} souls:({numcon(Gamelogic.souls[pokemon.name])})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(150))
                actiondecorator(imgui.text, cls.theme)(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free',
                                                          f'1 {pokemon.name} souls:({numcon(Gamelogic.souls[pokemon.name])})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(280))
                if pokemon.name in Gamelogic.souls:
                    use = not Gamelogic.souls[pokemon.name] or pokemon.lvl >= pokemon.maxlvl
                else:
                    use = True
                if cls.disabledecorator(imgui.button, use)(f'Summon##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Level', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free',
                                                          f'1 {pokemon.name} research:({numcon(Gamelogic.souls[pokemon.name])})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
                imgui.same_line(position=cls.resizewidth(530))

                use = not Gamelogic.physgems.quantity or pokemon.phys >= pokemon.lvl
                if cls.disabledecorator(imgui.button, use)(f'Physical##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Physical', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free',
                                                          f'1 physical gem:({numcon(Gamelogic.physgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.magicgems.quantity or pokemon.magic >= pokemon.lvl
                if cls.disabledecorator(imgui.button, use)(f'Magical##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Magical', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free',
                                                          f'1 magical gem:({numcon(Gamelogic.magicgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

                imgui.same_line(spacing=cls.resizewidth(40))
                use = not Gamelogic.specialgems.quantity or pokemon.special >= pokemon.lvl
                if cls.disabledecorator(imgui.button, use)(f'Special##{1000 + num}', 90):
                    Gamelogic.levelup = ['Reserve', 'Special', num]
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free',
                                                          f'1 special gem:({numcon(Gamelogic.specialgems.quantity)})')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")

            imgui.text('')
            imgui.same_line(position=cls.resizewidth(560))
            actiondecorator(imgui.text, cls.theme)(numcon(pokemon.phys) + '/' + numcon(pokemon.lvl))
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free', f'1 physical gem')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
            imgui.same_line(position=cls.resizewidth(690))
            actiondecorator(imgui.text, cls.theme)(numcon(pokemon.magic) + '/' + numcon(pokemon.lvl))
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free', f'1 magical gem')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
            imgui.same_line(position=cls.resizewidth(820))
            actiondecorator(imgui.text, cls.theme)(numcon(pokemon.special) + '/' + numcon(pokemon.lvl))
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                if imgui.is_item_hovered():
                    with tooltipdecorator(imgui.begin_tooltip, cls.theme)():
                        actiondecorator(imgui.text, cls.theme)(f"{pokemon.name}             lvl{numcon(pokemon.lvl)}")
                        tooltip = tooltips.pokemontooltip(pokemon, 'Free', f'1 special gem')
                        for i in tooltip:
                            actiondecorator(imgui.text, cls.theme)(f"{i}")
        pop = None
        for num, pokemon in enumerate(Gamelogic.unlockablepokemons):
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                actiondecorator(imgui.text, cls.theme)(pokemon.name)
                imgui.same_line(position=cls.resizewidth(280))
                if pokemon.name in Gamelogic.souls:
                    use = not Gamelogic.souls[pokemon.name]
                else:
                    use = True
                if cls.disabledecorator(imgui.button, use)(f'Unlock##{1000 + num}', 90):
                    Gamelogic.reserve.append(pokemon)
                    pop = num
                    Gamelogic.levelup = ['Reserve', 'Level', len(Gamelogic.reserve) - 1]
        if pop is not None:
            Gamelogic.unlockablepokemons.pop(pop)
            pop = None

        imgui.end_child()

        imgui.end()

    @classmethod
    def draw_settings(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), cls.resizeheight(350))
        imgui.set_next_window_position(cls.resizewidth(120), cls.resizeheight(100))
        backgroundecorator(imgui.begin, cls.theme)('Settingmenu', False, cls.flags)
        themes = ['rey', 'EVA', 'asuka']
        imgui.set_next_window_size_constraints((cls.resizewidth(20), cls.resizeheight(30)),
                                               (cls.resizewidth(80), cls.resizeheight(200)))
        with dropdowndecorator(imgui.begin_combo, cls.theme)('', cls.theme, imgui.COMBO_HEIGHT_LARGE) as combo:
            if combo.opened:
                for i, item in enumerate(themes):
                    is_selected = (i == cls.theme)
                    if actiondecorator(imgui.selectable, cls.theme)(item, is_selected)[0]:
                        cls.theme = item
        imgui.same_line()
        actiondecorator(imgui.text, cls.theme)('themes')
        changed, value = sliderdecorator(imgui.slider_int, cls.theme)('Sounds volume', Gamelogic.volume * 100, 0, 100)
        if changed:
            Gamelogic.volume = value / 100
        changed, value = sliderdecorator(imgui.slider_int, cls.theme)('Music volume', Gamelogic.musicvolume * 100, 0,
                                                                      100)
        if changed:
            Gamelogic.musicvolume = value / 100

        imgui.end()

    @classmethod
    def draw_bottombar(cls):
        imgui.set_next_window_size(list(pygame.display.get_window_size())[0] - cls.resizewidth(300),
                                   cls.resizeheight(100))
        imgui.set_next_window_position(cls.resizewidth(0),
                                       list(pygame.display.get_window_size())[1] - cls.resizeheight(100))
        backgroundecorator(imgui.begin, cls.theme)('Bottonbar', False, cls.flags)
        if Gamelogic.flags['Popup']:
            Gamelogic.bottomlog.insert(0,Popups[Gamelogic.flags['Popup']])
            now=datetime.datetime.now()
            Gamelogic.bottomtimes.insert(0,str(now.time())[0:8])
            Gamelogic.flags['Popup'] = 0

        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
            for num,i in enumerate(Gamelogic.bottomlog):
                actiondecorator(imgui.text, cls.theme)(Gamelogic.bottomtimes[num])
                imgui.same_line()
                for j in i:
                    actiondecorator(imgui.text, cls.theme)(j)

        imgui.end()

    @classmethod
    def draw_topbar(cls):
        imgui.set_next_window_size(list(pygame.display.get_window_size())[0] - cls.resizewidth(300),
                                   cls.resizeheight(50))
        imgui.set_next_window_position(0, 0)
        backgroundecorator(imgui.begin, cls.theme)('Topbar', False, cls.flags)

        imgui.end()

    @classmethod
    def draw_dungeon(cls):
        imgui.set_next_window_size(cls.resizewidth(1075), cls.resizeheight(440))
        imgui.set_next_window_position(cls.resizewidth(120), cls.resizeheight(55))
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            backgroundecorator(imgui.begin, cls.theme)('Dungeon', False, cls.flags)
            backgroundecorator(imgui.begin_child, cls.theme)("Child 4", height=cls.resizeheight(50), border=True)
            if Gamelogic.activedungeon is not None:
                progressbardecorator(imgui.progress_bar, cls.theme)(
                    (Gamelogic.activedungeon.floor + 1) / len(Gamelogic.activedungeon.currentlayout),
                    (cls.resizewidth(500), cls.resizeheight(40)),
                    f'{Gamelogic.activedungeon.name}   ({Gamelogic.activedungeon.floor + 1}/{len(Gamelogic.activedungeon.currentlayout)})')
            imgui.same_line(position=cls.resizewidth(530))
            if actiondecorator(imgui.button, cls.theme)('Quit', cls.resizewidth(90), cls.resizeheight(30)):
                Gamelogic.activedungeon = None
                Gamelogic.tab = 'Main'
            imgui.same_line(position=cls.resizewidth(630))
            if actiondecorator(imgui.button, cls.theme)('Back', cls.resizewidth(90), cls.resizeheight(30)):
                Gamelogic.tab = 'Main'

            imgui.end_child()
            imgui.text('')
            imgui.same_line(spacing=cls.resizewidth(20))
            if Gamelogic.activedungeon is not None:
                backgroundecorator(imgui.begin_child, cls.theme)("Your party", width=cls.resizewidth(970 / 3),
                                                                 height=cls.resizeheight(370), border=True)
                for pokemon in Gamelogic.activedungeon.party:
                    actiondecorator(imgui.text, cls.theme)(pokemon.name)
                    progressbardecorator(imgui.progress_bar, cls.theme)(pokemon.currenthp / pokemon.actualhp,
                                                                        (cls.resizewidth(250), cls.resizeheight(20)),
                                                                        f'{numcon(pokemon.currenthp)}/{numcon(pokemon.actualhp)}')
                    progressbardecorator(imgui.progress_bar, cls.theme)(
                        (1 - (pokemon.cd / (pokemon.skill.interval * 120))),
                        (cls.resizewidth(250), cls.resizeheight(20)),
                        str(pokemon.skill.name))
                imgui.end_child()

                imgui.same_line(spacing=cls.resizewidth(40))
                backgroundecorator(imgui.begin_child, cls.theme)("Child 2", width=cls.resizewidth(970 / 3),
                                                                 height=cls.resizeheight(370), border=True)
                dungeon = Gamelogic.activedungeon
                if dungeon is not None:
                    for pokemon in dungeon.currentlayout[dungeon.floor][
                                   0:min(5, len(dungeon.currentlayout[dungeon.floor]))]:
                        actiondecorator(imgui.text, cls.theme)(pokemon.name)
                        progressbardecorator(imgui.progress_bar, cls.theme)(pokemon.currenthp / pokemon.actualhp,
                                                                            (
                                                                            cls.resizewidth(250), cls.resizeheight(20)),
                                                                            f'{numcon(pokemon.currenthp)}/{numcon(pokemon.actualhp)}')
                        progressbardecorator(imgui.progress_bar, cls.theme)(
                            1 - (pokemon.cd / (pokemon.skill.interval * 120)),
                            (cls.resizewidth(250), cls.resizeheight(20)),
                            str(pokemon.skill.name))
                imgui.end_child()
                imgui.same_line(spacing=cls.resizewidth(30))
                backgroundecorator(imgui.begin_child, cls.theme)("Child 3", width=cls.resizewidth(970 / 3),
                                                                 height=cls.resizeheight(370), border=True)
                if dungeon is not None:
                    for string in dungeon.log:
                        every = 46
                        string = '\n'.join(string[i:i + every] for i in range(0, len(string), every))
                        actiondecorator(imgui.text, cls.theme)(string)
                    if len(dungeon.log) > 100:
                        for i in range(len(dungeon.log) - 100):
                            dungeon.log.pop(0)
                imgui.end_child()

        imgui.end()

    @classmethod
    def draw_training(cls):
        imgui.set_next_window_size(cls.resizewidth(1075), cls.resizeheight(440))
        imgui.set_next_window_position(cls.resizewidth(120), cls.resizeheight(55))
        with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 15)}']):
            backgroundecorator(imgui.begin, cls.theme)('Dungeon', False, cls.flags)

            imgui.end()
    @classmethod
    def draw_skill_menu(cls):
        imgui.set_next_window_size(cls.resizewidth(1050), 16 + cls.resizeheight(335))
        imgui.set_next_window_position(cls.resizewidth(120), 16 + cls.resizeheight(145))
        backgroundecorator(imgui.begin, cls.theme)('Skills', False, cls.flags)
        if Gamelogic.changeskill is not None:
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 30)}']):
                actiondecorator(imgui.text, cls.theme)(Gamelogic.changeskill.name)
                imgui.same_line(position=240)
                actiondecorator(imgui.text, cls.theme)('Name')
                imgui.same_line(position=490)
                actiondecorator(imgui.text, cls.theme)('Power')
                imgui.same_line(position=740)
                actiondecorator(imgui.text, cls.theme)('Interval')
                actiondecorator(imgui.text,cls.theme)('Default skill')
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.begin_child('Default skill',height=cls.resizeheight(25),border=True)
                imgui.same_line(position=250)
                actiondecorator(imgui.text,cls.theme)(Gamelogic.changeskill.originalskill.name)
                imgui.same_line(position=500)
                actiondecorator(imgui.text, cls.theme)(f'{Gamelogic.changeskill.originalskill.power}')
                imgui.same_line(position=750)
                actiondecorator(imgui.text, cls.theme)(f'{Gamelogic.changeskill.originalskill.interval}')
                imgui.end_child()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 30)}']):
                actiondecorator(imgui.text, cls.theme)('Active skill')
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.begin_child('Active skill', height=cls.resizeheight(25), border=True)
                imgui.same_line(position=250)
                actiondecorator(imgui.text, cls.theme)(Gamelogic.changeskill.skill.name)
                imgui.same_line(position=500)
                actiondecorator(imgui.text, cls.theme)(f'{Gamelogic.changeskill.skill.power}')
                imgui.same_line(position=750)
                actiondecorator(imgui.text, cls.theme)(f'{Gamelogic.changeskill.skill.interval}')
                imgui.same_line(position=940)
                if actiondecorator(imgui.button,cls.theme)('Remove',cls.resizewidth(90),cls.resizeheight(15)):
                    Gamelogic.changeskill.skill=Gamelogic.changeskill.originalskill.copy()
                    Gamelogic.changeskill=None
                    Gamelogic.partysubtab='Party selection'
                imgui.end_child()
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 30)}']):
                actiondecorator(imgui.text, cls.theme)('Skill list')
            with imgui.font(cls.Fonts['Helvetica'][f'{int(cls.fontfactor * 20)}']):
                imgui.begin_child('Skill list', border=True)
                for num,skill in enumerate(Gamelogic.availableskills):
                    imgui.same_line(position=250)
                    actiondecorator(imgui.text, cls.theme)(skill.name)
                    imgui.same_line(position=500)
                    actiondecorator(imgui.text, cls.theme)(f'{skill.power}')
                    imgui.same_line(position=750)
                    actiondecorator(imgui.text, cls.theme)(f'{skill.interval}')
                    imgui.same_line(position=940)
                if actiondecorator(imgui.button,cls.theme)(f'Assign###{num}',cls.resizewidth(90),cls.resizeheight(15)):
                    Gamelogic.changeskillfunction(Gamelogic.changeskill,skill)
                imgui.end_child()

        imgui.end()

    @classmethod
    def creategui(cls):
        # window size thingy
        cls.update_window_size()

        # Main menu
        cls.draw_topbar()
        cls.draw_bottombar()
        cls.draw_main_menu()
        cls.draw_energies()
        cls.draw_resources()

        # Submenu
        if Gamelogic.tab == 'Main':
            cls.draw_main()
        if Gamelogic.tab == 'Party':
            cls.draw_party_tabs()
            cls.draw_Adventurer()
            if Gamelogic.partysubtab == 'Party selection':
                cls.draw_party_menu()
            elif Gamelogic.partysubtab == 'Level up':
                cls.draw_levelup_menu()
            elif Gamelogic.partysubtab == 'Skill':
                cls.draw_skill_menu()
        if Gamelogic.tab == 'Training':
            cls.draw_training()
        if Gamelogic.tab == 'Dungeon':
            cls.draw_dungeon()
        if Gamelogic.tab == 'Settings':
            cls.draw_settings()

