import json
import initialization_elements

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


class Gamelogic:
    energies = []
    unlockedenergies = []
    resources = {}
    flags = {'Main': 0, 'Dubious home': 0}
    action = None
    upgradeaction = None
    tab = 'Main'
    subtab = 'Village'
    partysubtab = 'Main'
    mainelements = []
    mainsubelements = []
    partyelements = []
    instantactions = {'Common actions': [], 'Common actions 2': []}
    loopactions = {'Common loopactions': [], 'Common loopactions 2': [], 'Common loopactions 3': []}
    upgradeactions = {'Village': {'old house': [], 'old house 2': [], 'old house 3': []}, 'Forest': {},
                      'City': {'old house': []},
                      'Coast': {}, 'Jungle': {}, 'Astral plane': {}}
    dungeons = {}
    activedungeon= None
    nextactions = []
    pokemonlist = []
    reserve = []
    party = []
    switch = None
    remove = None
    add = None
    levelup = None
    partylenmax = 7
    fps = 240

    @classmethod
    def checkflags(cls):
        elements=[cls.instantactions, cls.loopactions]
        if cls.subtab in cls.dungeons.keys():
            elements.append(cls.dungeons[cls.subtab])
        if cls.subtab in cls.upgradeactions.keys():
            elements.append(cls.upgradeactions[cls.subtab])
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
                        action.isvisible = True
        for key in cls.resources:
            for resource in cls.resources[key]:
                resource.isvisible = False
                temp = 1
                if resource.unlockflags is not None:
                    for key2 in resource.unlockflags.keys():
                        if resource.unlockflags[key2] > cls.flags[key2]:
                            temp = 0
                if temp:
                    resource.isvisible = True
        for key in cls.mainsubelements:
            key.isvisible = False
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
                    if e.progress == 0:
                        e.docost()
                    e.progress += e.speed
                    if e.progress > 1:
                        e.progress = 0
                        e.dofinishaction()

    @classmethod
    def initializegame(cls):
        cls.corestats = initialization_elements.Corestats(cls)
        initialization_elements.createmenu(cls)
        initialization_elements.createmainsubmenu(cls)
        initialization_elements.createinstantactions(cls)
        initialization_elements.createloopactions(cls)
        initialization_elements.createpokemon(cls)
        initialization_elements.createpartytabs(cls)
        initialization_elements.createupgradeactions(cls)
        initialization_elements.createresources(cls)
        initialization_elements.createenergies(cls)
        initialization_elements.createdungeons(cls)

    @classmethod
    def savegame(cls):
        f = open("gamestate.json")
        Information = json.load(f)
        Information['basepokemons'] = []
        Information['party'] = []
        Information['reserve'] = []

        for x in cls.pokemonlist:
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
            Information["basepokemons"].append(pokemondict)
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
        for key in cls.upgradeactions:
            for location in cls.upgradeactions[key]:
                for i in cls.upgradeactions[key][location]:
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

    @classmethod
    def levelupfunction(cls, information):
        num = information[2]
        if information[0] == 'Party':
            pokemon = cls.party[num]
        else:
            pokemon = cls.reserve[num]
        if information[1] == 'Level':
            if pokemon.lvl < pokemon.maxlvl:
                pokemon.lvl += 1
        elif information[1] == 'Physical':
            if pokemon.phys < pokemon.lvl and cls.physseeds.quantity:
                pokemon.phys += 1
                cls.physseeds.quantity -= 1

        elif information[1] == 'Magical' and cls.magicseeds.quantity:
            if pokemon.magic < pokemon.lvl:
                pokemon.magic += 1
                cls.magicseeds.quantity -= 1

        elif information[1] == 'Special' and cls.specialseeds.quantity:
            if pokemon.special < pokemon.lvl:
                pokemon.special += 1
                cls.specialseeds.quantity -= 1
        pokemon.updatestats()
        cls.levelup = None

    @classmethod
    def frameaction(cls):
        cls.updatebuttons()
        cls.regenenergies()

        cls.loopactionprogress()
        cls.checkflags()
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
        if cls.upgradeaction is not None:
            for key in cls.upgradeactions[cls.subtab]:
                for i in cls.upgradeactions[cls.subtab][key]:
                    if i.name == cls.upgradeaction:
                        i.docost()
