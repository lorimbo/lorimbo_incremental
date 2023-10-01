import json
import initialization_elements
import random
import pygame
import datetime

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


class Gamelogic:
    energies = []
    unlockedenergies = []
    resources = {}
    flags = {}
    action = None
    quest = None
    tab = 'Main'
    subtab = 'Village'
    partysubtab = 'Party selection'
    mainelements = []
    mainsubelements = []
    partyelements = []
    instantactions = {}
    proceedactions={}
    loopactions = {}
    quests = {}
    areainstants={}
    arealoops = {}
    bottomlog=[]
    bottomtimes=[]
    exp = 0
    dungeons = {}
    activedungeon = None
    activepartypokemon = 0
    activeenemypokemon = 0
    souls = {}
    pokemonlist = []
    reserve = []
    party = []
    templates=[[],[]]
    savingtotemplates=False
    unlockablepokemons = []
    switch = None
    remove = None
    add = None
    levelup = None
    partylenmax = 5
    fps = 240
    volume = 0.2
    musicvolume = 0.3


    @classmethod
    def changetemplateto(cls,num):
        cls.party=cls.templates[num][0]
        cls.reserve = cls.templates[num][1]


    @classmethod
    def checkflags(cls):
        elements = [cls.instantactions, cls.loopactions]
        if cls.subtab in cls.quests.keys():
            elements.append(cls.quests[cls.subtab])
        if cls.subtab in cls.dungeons.keys():
            elements.append(cls.dungeons[cls.subtab])
        areaactions=[]
        if cls.subtab in cls.areainstants.keys():
            for key in cls.areainstants[cls.subtab]:
                areaactions.append(key)
        if cls.subtab in cls.arealoops.keys():
            for key in cls.arealoops[cls.subtab]:
                areaactions.append(key)
        if cls.subtab in cls.proceedactions.keys():
            for action in cls.proceedactions[cls.subtab]:
                temp = 0
                if action.closingflags is not None:
                    for key in action.closingflags.keys():
                        if action.closingflags[key] <= cls.flags[key]:
                            temp = 1
                if action.unlockflags is not None:
                    for key in action.unlockflags.keys():
                        if action.unlockflags[key] > cls.flags[key]:
                            temp = 1
                if temp:
                    action.isvisible = False
                else:
                    if not action.isvisible:
                        cls.bottomlog.insert(0, [f"Unlocked the {action.name} option to proceed in the {cls.subtab} location!"])
                        now = datetime.datetime.now()
                        cls.bottomtimes.insert(0, str(now.time())[0:8])
                    action.isvisible = True

        for action in areaactions:
            temp = 0
            if action.closingflags is not None:
                for key in action.closingflags.keys():
                    if action.closingflags[key] <= cls.flags[key]:
                        temp = 1
            if action.unlockflags is not None:
                for key in action.unlockflags.keys():
                    if action.unlockflags[key] > cls.flags[key]:
                        temp = 1
            if temp:
                action.isvisible = False
            else:
                if not action.isvisible:
                    cls.bottomlog.insert(0,[f"Unlocked the {action.name} action in the {cls.subtab} location!"])
                    now = datetime.datetime.now()
                    cls.bottomtimes.insert(0,str(now.time())[0:8])
                action.isvisible = True
        for actionlist in elements:
            for key1 in actionlist:
                for action in actionlist[key1]:
                    temp = 0
                    if action.closingflags is not None:
                        for key in action.closingflags.keys():
                            if action.closingflags[key] <= cls.flags[key]:
                                temp = 1
                    if action.unlockflags is not None:
                        for key in action.unlockflags.keys():
                            if action.unlockflags[key] > cls.flags[key]:
                                temp = 1
                    if temp:
                        action.isvisible = False
                    else:
                        if not action.isvisible:
                            now = datetime.datetime.now()
                            cls.bottomtimes.insert(0,str(now.time())[0:8])
                            if actionlist is cls.dungeons[cls.subtab]:
                                cls.bottomlog.insert(0, [f"Unlocked the {action.name} dungeon!"])
                            elif actionlist is cls.quests[cls.subtab]:
                                cls.bottomlog.insert(0,[f"Unlocked the {action.name} quest!"])
                            else:
                                cls.bottomlog.insert(0, [f"Unlocked the {action.name} action!"])
                        action.isvisible = True
        for element in cls.mainelements:
            temp = 0
            if element.closingflags is not None:
                for key in element.closingflags.keys():
                    if element.closingflags[key] <= cls.flags[key]:
                        temp = 1
            if element.unlockflags is not None:
                for key in element.unlockflags.keys():
                    if element.unlockflags[key] > cls.flags[key]:
                        temp = 1
            if temp:
                element.isvisible = False
            else:
                if not element.isvisible:
                    now = datetime.datetime.now()
                    cls.bottomtimes.insert(0,str(now.time())[0:8])
                    cls.bottomlog.insert(0,[f"Unlocked the {element.name} Menu!"])
                element.isvisible = True
        for key in cls.resources:
            for resource in cls.resources[key]:
                temp = 1
                if resource.unlockflags is not None:
                    for key2 in resource.unlockflags.keys():
                        if resource.unlockflags[key2] > cls.flags[key2]:
                            temp = 0
                if temp:
                    resource.isvisible = True
        for key in cls.mainsubelements:
            temp = 1
            if key.unlockflags is not None:
                for key2 in key.unlockflags.keys():
                    if key.unlockflags[key2] > cls.flags[key2]:
                        temp = 0
            if temp:
                key.isvisible = True


    @classmethod
    def deactivateloopactions(cls):
        for key in cls.loopactions:
            for e in cls.loopactions[key]:
                e.isactive = False
        for location in cls.arealoops:
            for e in cls.arealoops[location]:
                e.isactive=False

    @classmethod
    def switchparty(cls, pos):
        if pos != -1:
            cls.party.insert(pos + 1, cls.party.pop(pos))
        cls.switch = None

    @classmethod
    def removepokemonfromparty(cls, pos):
        cls.reserve.append(cls.party.pop(pos))
        cls.remove = None

    @classmethod
    def addpokemontoparty(cls, pos):
        cls.party.append(cls.reserve.pop(pos))
        cls.add = None

    @classmethod
    def loopactionprogress(cls):
        for key in cls.loopactions:
            for e in cls.loopactions[key]:
                if e.isactive:
                    e.dopassiveaction()
                    if e.progress <= 0:
                        cls.loopactions['Common loopactions'][0].activation()
                        if e.docost():
                            e.activation()
                        else:
                            e.progress = 0
                            return
                    e.progress += e.speed
                    if e.progress > 1:
                        e.progress = 0
                        e.dofinishaction()
        for location in cls.arealoops:
            for e in cls.arealoops[location]:
                if e.isactive:
                    e.dopassiveaction()
                    if e.progress <= 0:
                        cls.loopactions['Common loopactions'][0].activation()
                        if e.docost():
                            e.activation()
                        else:
                            e.progress = 0
                            return
                    e.progress += e.speed
                    if e.progress > 1:
                        e.progress = 0
                        e.dofinishaction()

    @classmethod
    def initializegame(cls):
        cls.corestats = initialization_elements.Corestats(cls)
        initialization_elements.loadflags(cls)
        initialization_elements.createmenu(cls)
        initialization_elements.createmainsubmenu(cls)
        initialization_elements.createinstantactions(cls)
        initialization_elements.createareainstant(cls)
        initialization_elements.createloopactions(cls)
        initialization_elements.createarealoops(cls)
        initialization_elements.createproceedactions(cls)
        initialization_elements.createpokemon(cls)
        initialization_elements.createpartytabs(cls)
        initialization_elements.createquests(cls)
        initialization_elements.createresources(cls)
        initialization_elements.createenergies(cls)
        initialization_elements.createdungeons(cls)

    @classmethod
    def savegame(cls):
        f = open("gamestate.json")
        Information = json.load(f)
        Information['party'] = []
        Information['reserve'] = []
        Information['resources']={}
        Information['flags']={}
        for flag in cls.flags:
            Information['flags'][flag]=cls.flags[flag]
        for category in cls.resources:
            for resource in cls.resources[category]:
                Information['resources'][resource.name]=(resource.quantity,resource.max,resource.unlockflags,resource.category,resource.regen)
        for x in cls.party:
            pokemondict = {}
            pokemondict["name"] = x.name
            pokemondict["hp"] = x.hp
            pokemondict["atk"] = x.patk
            pokemondict["dif"] = x.pdef
            pokemondict["satk"] = x.matk
            pokemondict["sdif"] = x.mdef
            pokemondict["maxlvl"] = x.maxlvl
            pokemondict["unlocked"] = x.unlocked
            pokemondict["lvl"] = x.lvl
            pokemondict["phys"] = x.phys
            pokemondict["magic"] = x.magic
            pokemondict["special"] = x.special
            pokemondict["drop"]=x.drop
            Information["party"].append(pokemondict)
        for x in cls.reserve:
            pokemondict = {}
            pokemondict["name"] = x.name
            pokemondict["hp"] = x.hp
            pokemondict["atk"] = x.patk
            pokemondict["dif"] = x.pdef
            pokemondict["satk"] = x.matk
            pokemondict["sdif"] = x.mdef
            pokemondict["maxlvl"] = x.maxlvl
            pokemondict["unlocked"] = x.unlocked
            pokemondict["lvl"] = x.lvl
            pokemondict["phys"] = x.phys
            pokemondict["magic"] = x.magic
            pokemondict["special"] = x.special
            pokemondict["drop"] = x.drop
            Information["reserve"].append(pokemondict)

        out_file = open("gamestate.json", "w")

        json.dump(Information, out_file, indent=6)

        out_file.close()

    @classmethod
    def regenenergies(cls):
        for energy in cls.energies:
            if energy.quantity < energy.max:
                energy.quantity += energy.regen

    @classmethod
    def updatebuttons(cls):
        for key in cls.quests:
            for location in cls.quests[key]:
                for i in cls.quests[key][location]:
                    i.update()
        for key in cls.loopactions:
            for i in cls.loopactions[key]:
                i.update()
        for key in cls.instantactions:
            for i in cls.instantactions[key]:
                i.update()
        for key in cls.dungeons:
            for location in cls.dungeons[key]:
                for i in cls.dungeons[key][location]:
                    i.update()
        for key in cls.areainstants:
            for i in cls.areainstants[key]:
                i.update()
        for key in cls.arealoops:
            for i in cls.arealoops[key]:
                i.update()
        for key in cls.proceedactions:
            for i in cls.proceedactions[key]:
                i.update()

    @classmethod
    def levelupfunction(cls, information):
        num = information[2]
        if information[0] == 'Party':
            pokemon = cls.party[num]
        else:
            pokemon = cls.reserve[num]
        if information[1] == 'Level':
            if pokemon.lvl < pokemon.maxlvl:
                if pokemon.name == 'You':
                    if cls.fate.quantity:
                        cls.fate.quantity -= 1
                        pokemon.lvl += 1
                elif cls.souls[pokemon.name]:
                    cls.souls[pokemon.name] -= 1
                    pokemon.lvl += 1
        elif information[1] == 'Physical':
            if pokemon.phys < pokemon.lvl and cls.physgems.quantity:
                pokemon.phys += 1
                cls.physgems.quantity -= 1

        elif information[1] == 'Magical' and cls.magicgems.quantity:
            if pokemon.magic < pokemon.lvl:
                pokemon.magic += 1
                cls.magicgems.quantity -= 1

        elif information[1] == 'Special' and cls.specialgems.quantity:
            if pokemon.special < pokemon.lvl:
                pokemon.special += 1
                cls.specialgems.quantity -= 1
        pokemon.updatestats()
        cls.levelup = None

    @classmethod
    def dungeonprogress(cls):
        alive = [pokemon for pokemon in cls.activedungeon.party if pokemon.currenthp]
        alive2 = [pokemon for pokemon in cls.activedungeon.currentlayout[cls.activedungeon.floor] if pokemon.currenthp]

        alive[cls.activepartypokemon].cd -= 1
        if alive[cls.activepartypokemon].cd == 0:
            damagedealt = alive[cls.activepartypokemon].skill.useskill(alive[cls.activepartypokemon], alive2[0])
            if cls.tab == cls.mainelements[5].name:
                hit = pygame.mixer.Sound('Sounds/hitting.wav')
                hit.set_volume(cls.volume)
                pygame.mixer.Sound.play(hit)
            alive[cls.activepartypokemon].cd = alive[cls.activepartypokemon].skill.interval * 240
            cls.activedungeon.log.append(
                f'{alive[cls.activepartypokemon].name} dealt {numcon(damagedealt)} dmg to {alive2[0].name}')
            if alive2[0].currenthp == 0:
                alive2[0].cd = alive2[0].skill.interval * 240
                cls.activedungeon.log.append(
                    f'Enemy {alive2[0].name} fainted!')
                cls.exp += alive2[0].drop['exp']
                droplog = f'Enemy {alive2[0].name} dropped {alive2[0].drop["exp"]} exp'
                for resource in alive2[0].drop['resources']:
                    name = resource[0]
                    quantity = resource[1]
                    lootchance = resource[2]
                    for x in cls.resources.keys():
                        for resource2 in [e for e in cls.resources[x] if e.name == name]:
                            n = random.randint(0, 100)
                            if n <= lootchance:
                                resource2.quantity += quantity
                                if resource2.quantity > resource2.max:
                                    resource2.quantity = resource2.max
                                droplog += f', {quantity} {name}'
                    n = random.randint(0, 100)
                    souldrop = 1
                    if n <= 10 and alive2[0].name not in ['Training dummy']:
                        if alive2[0].name not in cls.souls:
                            pokemontounlock = alive2[0].copy()
                            cls.souls[pokemontounlock.name] = 0
                            pokemontounlock.phys = 1
                            pokemontounlock.magic = 1
                            pokemontounlock.special = 1
                            pokemontounlock.lvl = 5
                            pokemontounlock.wild = False

                            cls.unlockablepokemons.append(pokemontounlock)
                        cls.souls[alive2[0].name] += souldrop

                        droplog += f',{souldrop} {alive2[0].name} soul'

                cls.activedungeon.log.append(droplog)
                alive2 = [pokemon for pokemon in cls.activedungeon.currentlayout[cls.activedungeon.floor] if
                          pokemon.currenthp]
                cls.activeenemypokemon = max(0, cls.activeenemypokemon - 1)
                if not len(alive2):
                    cls.activepartypokemon = 0
                    cls.activeenemypokemon = 0
                    cls.activedungeon.floor += 1

                    if cls.activedungeon.floor >= len(cls.activedungeon.currentlayout):
                        cls.activedungeon.generate()
                        cls.activedungeon.log.append('You cleared the dungeon!')
                        victory=pygame.mixer.Sound('Sounds/victory.mp3')
                        victory.set_volume(cls.volume)
                        pygame.mixer.Sound.play(victory)
                        cls.regenpokemonhealt(cls.party[0:5])
                        cls.activedungeon.docomplete()
                        if cls.activedungeon.changeflags is not None:
                            for key in cls.activedungeon.changeflags:
                                cls.flags[key] += cls.activedungeon.changeflags[key]
                        cls.activedungeon.changeflags = None
                    return

            cls.activepartypokemon += 1
            if cls.activepartypokemon > len(alive) - 1:
                cls.activepartypokemon = 0

        alive2[cls.activeenemypokemon].cd -= 1
        if alive2[cls.activeenemypokemon].cd == 0:
            damagedealt = alive2[cls.activeenemypokemon].skill.useskill(alive2[cls.activeenemypokemon], alive[0])
            if cls.tab == cls.mainelements[5].name:
                hit = pygame.mixer.Sound('Sounds/ouch.wav')
                hit.set_volume(cls.volume)
                pygame.mixer.Sound.play(hit)
            alive2[cls.activeenemypokemon].cd = alive2[cls.activeenemypokemon].skill.interval * 240
            cls.activedungeon.log.append(
                f'Enemy {alive2[cls.activeenemypokemon].name} dealt {numcon(damagedealt)} dmg to {alive[0].name}')
            if alive[0].currenthp == 0:
                cls.activedungeon.log.append(
                    f'{alive[0].name} fainted!')
                alive[0].cd = alive[0].skill.interval * 240
                alive = [pokemon for pokemon in cls.activedungeon.party if pokemon.currenthp]
                cls.activepartypokemon = max(0, cls.activepartypokemon - 1)
                if not len(alive):
                    cls.activepartypokemon = 0
                    cls.activeenemypokemon = 0
                    cls.activedungeon.generate()
                    cls.activedungeon.log.append('You and your party were defeated')
                    cls.regenpokemonhealt(cls.party[0:5])
                return
            cls.activeenemypokemon += 1
            if cls.activeenemypokemon > len(alive2) - 1:
                cls.activeenemypokemon = 0

    @classmethod
    def regenpokemonhealt(cls, list):
        for pokemon in list:
            pokemon.currenthp = pokemon.actualhp

    @classmethod
    def frameaction(cls):
        cls.updatebuttons()
        cls.regenenergies()
        cls.loopactionprogress()
        cls.checkflags()
        if cls.activedungeon is not None:
            cls.dungeonprogress()
        if cls.switch is not None:
            cls.switchparty(cls.switch)
        if cls.remove is not None:
            cls.removepokemonfromparty(cls.remove)
        if cls.add is not None:
            cls.addpokemontoparty(cls.add)
        if cls.levelup is not None:
            cls.levelupfunction(cls.levelup)
        if cls.action is not None:
            for key in cls.instantactions:
                for i in cls.instantactions[key]:
                    if i.name == cls.action:
                        i.docost()
            for i in cls.areainstants[cls.subtab]:
                if i.name == cls.action:
                    i.docost()
            for i in cls.proceedactions[cls.subtab]:
                if i.name == cls.action:
                    i.docost()
        if cls.quest is not None:
            for key in cls.quests[cls.subtab]:
                for i in cls.quests[cls.subtab][key]:
                    if i.name == cls.quest:
                        i.docost()
