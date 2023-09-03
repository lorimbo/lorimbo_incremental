from __future__ import absolute_import
import imgui

import tooltips
from Game_logic import Gamelogic
from tooltips import actionTooltip
def numcon(n):
    if n>10000000:
        return f'{round(n/1000000,1)}M'
    elif n>1000000:
        return f'{round(n/1000000,2)}M'
    elif n>100000:
        return f'{round(n/1000,0)}K'
    elif n>10000:
        return f'{round(n/1000,1)}K'
    elif n>1000:
        return f'{round(n/1000,2)}K'
    return str(round(n,1))

class Graphics:
    flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE
    resourcesflags = imgui.WINDOW_NO_RESIZE
    new_font = None
    new_font2 = None

    @classmethod
    def notinusedecorator(cls,function,use):
        def inner1(*args,**kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.5)
            func=function(*args,**kwargs)
            imgui.pop_style_var(1)
            return func
        if use:
            return inner1
        else:
            return function
    @classmethod
    def disabledecorator(cls,function,use):
        def inner1(*args,**kwargs):
            imgui.push_style_var(imgui.STYLE_ALPHA, 0.2)
            func=function(*args,**kwargs)
            imgui.pop_style_var(1)
            return func
        if use:
            return inner1
        else:
            return function



    @classmethod
    def draw_main_menu(cls):
        # Main menu
        visible = [e for e in Gamelogic.mainelements if e.isvisible]
        imgui.set_next_window_size(105, 68 + 54 * len(visible))
        imgui.set_next_window_position(10, 0)
        imgui.begin('Main', False, cls.flags)
        for button in visible:
            use=not Gamelogic.tab == button.name
            if cls.notinusedecorator(imgui.button,use)(button.name, 90, 50):
                Gamelogic.tab = button.name
        if imgui.button('Save', 90, 50):
            Gamelogic.savegame()
        imgui.end()

    @classmethod
    def draw_main_submenu(cls):
        visible = [e for e in Gamelogic.mainsubelements if e.isvisible]
        for button in visible:
            use= not Gamelogic.subtab == button.name
            if cls.notinusedecorator(imgui.button,use)(button.name, 90, 50):
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
                use=button.isdisabled
                if cls.disabledecorator(imgui.button,use)(button.name, 120, 50) and not button.isdisabled:
                    Gamelogic.action = button.name
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(f"{button.name}")
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
                use=button.isdisabled
                if cls.disabledecorator(imgui.button,use)(button.name, 120, 50) and not button.isdisabled:
                    button.activation()
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(f"{button.name}")
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
                use= button.isdisabled
                if cls.disabledecorator(imgui.button,use)(button.name, 120, 50) and not button.isdisabled:
                    Gamelogic.upgradeaction = button.name
                if imgui.is_item_hovered():
                    with imgui.begin_tooltip():
                        imgui.text(f"{button.name}")
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
        visible=[e for e in Gamelogic.energies if e.isvisible]
        imgui.set_next_window_size(230, 35 * len(visible))
        imgui.set_next_window_position(1200, 0)
        imgui.begin('Energies', False, cls.resourcesflags)
        draw_list = imgui.get_window_draw_list()
        num = 0
        for energy in visible:
            color = energy.color
            color = [c / 255 for c in color]
            draw_list.path_clear()
            draw_list.add_rect_filled(1210, 30 + num * 25,
                                      1210 + 190 * energy.quantity / energy.max,
                                      50 + num * 25, imgui.get_color_u32_rgba(*color, 1), 0)
            imgui.invisible_button(energy.name,190,20)
            if imgui.is_item_hovered():
                with imgui.begin_tooltip():
                    imgui.text(f"{energy.name}")
                    tooltip = tooltips.energyTooltip(energy.name, energy.quantity, energy.max,energy.regen)
                    for i in tooltip:
                        imgui.text(f"{i}")
            draw_list.add_text(1220, 35 + num * 25, imgui.get_color_u32_rgba(1, 1, 1, 1), energy.name)
            draw_list.add_text(1320, 35 + num * 25, imgui.get_color_u32_rgba(1, 1, 1, 1),
                               str(round(energy.quantity, 1)) + '/' + str(
                                   round(energy.max, 0)))
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
        for category in Gamelogic.resources:
            for resource in Gamelogic.resources[category]:
                if resource.isvisible:
                    windowheight += 1
        if windowheight > 40:
            windowheight = 40
        visible=[e for e in Gamelogic.energies if e.isvisible]
        imgui.set_next_window_size(230, 15 + 21 * windowheight)
        imgui.set_next_window_position(1200, 35 * len(visible))
        imgui.begin('Resources', False, cls.resourcesflags)
        for key in Gamelogic.resources:
            if [e for e in Gamelogic.resources[key] if e.isvisible]:
                if imgui.tree_node(key, imgui.TREE_NODE_DEFAULT_OPEN):
                    for subkey in Gamelogic.resources[key]:
                        if subkey.isvisible:
                            space = ''
                            numofspace = 16 - len(subkey.name)
                            if not numofspace:
                                numofspace = 0
                            for i in range(numofspace):
                                space += ' '
                            imgui.text(subkey.name + space + numcon(subkey.quantity) + '/' + numcon(subkey.max))
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
        imgui.set_next_window_size(650, 70)
        imgui.set_next_window_position(330, 0)
        imgui.begin('Partytabs', False, cls.flags)
        visible = cls.get_visible_elements(Gamelogic.partyelements)
        for element in visible:
            with imgui.font(cls.new_font):
                use= not Gamelogic.partysubtab == element.name
                if cls.notinusedecorator(imgui.button,use)(element.name,120,50):
                    Gamelogic.partysubtab = element.name
                imgui.same_line()
        imgui.end()

    @classmethod
    def draw_Adventurer(cls):
        imgui.set_next_window_size(1050, 65)
        imgui.set_next_window_position(120, 70)
        imgui.begin('Adventurer', False, cls.flags)
        Stats = Gamelogic.corestats.finalstats()
        with imgui.font(cls.new_font2):
            imgui.same_line(position=150)
            imgui.text('[Core Stats]')
            imgui.same_line()
            for key in Stats:
                imgui.text(key + ':' + numcon(Stats[key]))
                imgui.same_line()
        imgui.end()


    @classmethod
    def draw_party_menu(cls):
        imgui.set_next_window_size(1050, 800)
        imgui.set_next_window_position(120, 180)
        imgui.begin('Partymenu', False, cls.flags)
        imgui.begin_child("Child 1", height=320, border=True)
        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.new_font):
                imgui.text(pokemon.name)
                imgui.same_line(position=150)
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=225)
                imgui.text(numcon(pokemon.actualhp))
                imgui.same_line(position=300)
                imgui.text(numcon(pokemon.actualpatk))
                imgui.same_line(position=375)
                imgui.text(numcon(pokemon.actualpdef))
                imgui.same_line(position=450)
                imgui.text(numcon(pokemon.actualmatk))
                imgui.same_line(position=525)
                imgui.text(numcon(pokemon.actualmdef))
                imgui.same_line(position=600)
                use= num==0
                if cls.disabledecorator(imgui.arrow_button,use)(f'downbutton##{num}', imgui.DIRECTION_UP):
                    Gamelogic.switch = num - 1

                imgui.same_line()
                use= num == len(Gamelogic.party)-1
                if cls.disabledecorator(imgui.arrow_button,use)(f'upbutton##{num}', imgui.DIRECTION_DOWN):
                    Gamelogic.switch = num


                imgui.same_line()
                use= (pokemon.name=='You')
                imgui.same_line(position=698)
                if cls.disabledecorator(imgui.button,use)(f'Remove##{num}', width=90) and not use:
                    Gamelogic.remove = num

        imgui.end_child()
        imgui.begin_child("Child 2", height=400, border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.new_font):
                imgui.text(pokemon.name)
                imgui.same_line(position=150)
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=225)
                imgui.text(numcon(pokemon.actualhp))
                imgui.same_line(position=300)
                imgui.text(numcon(pokemon.actualpatk))
                imgui.same_line(position=375)
                imgui.text(numcon(pokemon.actualpdef))
                imgui.same_line(position=450)
                imgui.text(numcon(pokemon.actualmatk))
                imgui.same_line(position=525)
                imgui.text(numcon(pokemon.actualmdef))
                use=not len(Gamelogic.party) < Gamelogic.partylenmax
                imgui.same_line(position=698)
                if cls.disabledecorator(imgui.button,use)(f'Add##{num}', 90) and not use:
                    Gamelogic.add = num

        imgui.end_child()
        imgui.end()

    @classmethod
    def draw_levelup_menu(cls):
        imgui.set_next_window_size(1050, 800)
        imgui.set_next_window_position(120, 180)
        imgui.begin('Levelupmenu', False, cls.flags)
        imgui.begin_child("Child 1", height=320, border=True)
        for num, pokemon in enumerate(Gamelogic.party):
            with imgui.font(cls.new_font):
                imgui.text(pokemon.name)
                imgui.same_line(position=150)
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=230)
                if imgui.button(f'Summon##{num}', 90):
                    Gamelogic.levelup = ['Party','Level',num]
                imgui.same_line(position=530)
                use= not Gamelogic.physseeds.quantity
                if cls.disabledecorator(imgui.button,use)(f'Physical##{num}', 90):
                    Gamelogic.levelup = ['Party','Physical',num]
                imgui.same_line(spacing=40)
                use= not Gamelogic.magicseeds.quantity
                if cls.disabledecorator(imgui.button,use)(f'Magical##{num}', 90):
                    Gamelogic.levelup = ['Party','Magical',num]
                imgui.same_line(spacing=40)
                use= not Gamelogic.specialseeds.quantity
                if cls.disabledecorator(imgui.button,use)(f'Special##{num}', 90):
                    Gamelogic.levelup = ['Party','Special',num]
            imgui.text('')
            imgui.same_line(position=560)
            imgui.text(numcon(pokemon.phys)+'/'+numcon(pokemon.lvl))
            imgui.same_line(position=690)
            imgui.text(numcon(pokemon.magic) + '/' + numcon(pokemon.lvl))
            imgui.same_line(position=820)
            imgui.text(numcon(pokemon.special) + '/' + numcon(pokemon.lvl))

        imgui.end_child()
        imgui.begin_child("Child 2", height=400, border=True)
        for num, pokemon in enumerate(Gamelogic.reserve):
            with imgui.font(cls.new_font):
                imgui.text(pokemon.name)
                imgui.same_line(position=150)
                imgui.text(numcon(pokemon.lvl) + '/' + numcon(pokemon.maxlvl))
                imgui.same_line(position=230)

                if imgui.button(f'Summon##{1000+num}', 90):
                    Gamelogic.levelup = ['Reserve','Level',num]
                imgui.same_line(position=530)

                use= not Gamelogic.physseeds.quantity
                if cls.disabledecorator(imgui.button,use)(f'Physical##{1000+num}', 90):
                    Gamelogic.levelup = ['Reserve','Physical',num]

                imgui.same_line(spacing=40)
                use= not Gamelogic.magicseeds.quantity
                if cls.disabledecorator(imgui.button,use)(f'Magical##{1000+num}', 90):
                    Gamelogic.levelup = ['Reserve','Magical',num]

                imgui.same_line(spacing=40)
                use= not Gamelogic.specialseeds.quantity
                if cls.disabledecorator(imgui.button,use)(f'Special##{1000+num}', 90):
                    Gamelogic.levelup = ['Reserve','Special',num]

            imgui.text('')
            imgui.same_line(position=560)
            imgui.text(numcon(pokemon.phys)+'/'+numcon(pokemon.lvl))
            imgui.same_line(position=690)
            imgui.text(numcon(pokemon.magic) + '/' + numcon(pokemon.lvl))
            imgui.same_line(position=820)
            imgui.text(numcon(pokemon.special) + '/' + numcon(pokemon.lvl))


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
            cls.draw_Adventurer()
            if Gamelogic.partysubtab == Gamelogic.partyelements[0].name:
                cls.draw_party_menu()
            elif Gamelogic.partysubtab == Gamelogic.partyelements[1].name:
                cls.draw_levelup_menu()

