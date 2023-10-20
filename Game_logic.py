import json
import initialization_elements
import random
import pygame
import datetime
import math

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
Weak={'Fire':['Water','Ground'],'Grass':['Fire'],'Water':['Electric','Grass'],'Ground':['Water','Grass'],'Electric':['Ground']}
Strong={'Fire':['Grass'],'Grass':['Water','Ground'],'Water':['Fire','Ground'],'Ground':['Fire','Electric'],'Electric':['Water'],'Dark':['Light'],'Light':['Dark']}


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
    auto=False
    mainname='You'
    ritualsubtab='Rank'
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
    buyablematerials=[]
    partyelements = []
    availableskills=[]
    learnableskills = []
    instantactions = {}
    proceedactions={}
    longactions = {}
    quests = {}
    areainstants={}
    arealongs = {}
    bottomlog=[]
    storylog=[]
    bottomlogpreviouslen=len(bottomlog)
    bottomtimes=[]
    dungeons = {}
    activedungeon = None
    pokemonattacking=None
    stageofselection = 0
    souls = {}
    pokemonlist = []
    reserve = []
    party = []
    templates=[]
    savingtotemplates=False
    unlockablepokemons = []
    switch = None
    remove = None
    add = None
    levelup = None
    changeskill = None
    addskill=None
    removeskill=None
    partylenmax = 5
    fps = 120
    fpscounter=''
    volume = 0.1
    musicvolume = 0.1
    cleareddungeons=[]
    corestats=None
    framecounter=0



    @classmethod
    def changetemplateto(cls,num):
        partycopy=[e.copy() for e in cls.templates[num][0]]
        reservecopy=[e.copy() for e in cls.templates[num][1]]
        cls.passiveremove()
        cls.party=partycopy
        cls.reserve = reservecopy
        cls.passivesadd()


    @classmethod
    def checkflags(cls):
        elements = [cls.instantactions, cls.longactions]
        if cls.subtab in cls.quests.keys():
            elements.append(cls.quests[cls.subtab])
        if cls.subtab in cls.dungeons.keys():
            elements.append(cls.dungeons[cls.subtab])
        areaactions=[]
        if cls.subtab in cls.areainstants.keys():
            for key in cls.areainstants[cls.subtab]:
                areaactions.append(key)
        if cls.subtab in cls.arealongs.keys():
            for key in cls.arealongs[cls.subtab]:
                areaactions.append(key)
        for item in cls.buyablematerials:
            temp = 0
            if item.closingflags is not None:
                for key in item.closingflags.keys():
                    if item.closingflags[key] <= cls.flags[key]:
                        temp = 1
            if item.unlockflags is not None:
                for key in item.unlockflags.keys():
                    if item.unlockflags[key] > cls.flags[key]:
                        temp = 1
            if temp:
                item.isvisible = False
            else:
                item.isvisible = True
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
                    if not action.isvisible and cls.framecounter!=0 and cls.framecounter!=1:
                        cls.bottomlog.append( [f"Unlocked the {action.name} option to proceed in the {cls.subtab} location!"])
                        now = datetime.datetime.now()
                        cls.bottomtimes.append( str(now.time())[0:8])
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
                if not action.isvisible and cls.framecounter!=0 and cls.framecounter!=1:
                    cls.bottomlog.append([f"Unlocked the {action.name} action in the {cls.subtab} location!"])
                    now = datetime.datetime.now()
                    cls.bottomtimes.append(str(now.time())[0:8])
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
                        if not action.isvisible and cls.framecounter!=0 and cls.framecounter!=1:
                            now = datetime.datetime.now()
                            cls.bottomtimes.append(str(now.time())[0:8])
                            if actionlist is cls.dungeons[cls.subtab]:
                                cls.bottomlog.append( [f"Unlocked the {action.name} dungeon!"])
                            elif actionlist is cls.quests[cls.subtab]:
                                cls.bottomlog.append([f"Unlocked the {action.name} quest!"])
                            else:
                                cls.bottomlog.append( [f"Unlocked the {action.name} action!"])
                        action.isvisible = True
        for menulist in [cls.mainelements,cls.mainsubelements,cls.partyelements]:
            for element in menulist:
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
                    if not element.isvisible and cls.framecounter!=0 and cls.framecounter!=1:
                        now = datetime.datetime.now()
                        cls.bottomtimes.append(str(now.time())[0:8])
                        cls.bottomlog.append([f"Unlocked the {element.name} Menu!"])
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


    @classmethod
    def deactivatelongactions(cls):
        for key in cls.longactions:
            for e in cls.longactions[key]:
                e.isactive = False
        for location in cls.arealongs:
            for e in cls.arealongs[location]:
                e.isactive=False

    @classmethod
    def switchparty(cls, pos):
        if pos != -1:
            cls.party.insert(pos + 1, cls.party.pop(pos))
        cls.switch = None

    @classmethod
    def removepokemonfromparty(cls, pos):
        cls.passiveremove()
        cls.reserve.append(cls.party.pop(pos))
        cls.passivesadd()
        cls.remove = None

    @classmethod
    def addpokemontoparty(cls, pos):
        cls.passiveremove()
        cls.party.append(cls.reserve.pop(pos))
        cls.passivesadd()

        cls.add = None

    @classmethod
    def longactionprogress(cls):
        for key in cls.longactions:
            for e in cls.longactions[key]:
                if e.isactive:
                    e.dopassiveaction()
                    if e.progress <= 0:
                        cls.longactions['Common longactions'][0].activation()
                        if e.docost():
                            e.activation()
                        else:
                            e.progress = 0
                            return
                    e.progress += e.speed
                    if e.progress > 1:
                        e.progress = 0
                        e.dofinishaction()
        for location in cls.arealongs:
            for e in cls.arealongs[location]:
                if e.isactive:
                    e.dopassiveaction()
                    if e.progress <= 0:
                        cls.longactions['Common longactions'][0].activation()
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
        initialization_elements.createcorestats(cls)
        initialization_elements.loadflags(cls)
        initialization_elements.createskilllists(cls)
        initialization_elements.createmenu(cls)
        initialization_elements.createshopitems(cls)
        initialization_elements.createmainsubmenu(cls)
        initialization_elements.createinstantactions(cls)
        initialization_elements.createareainstant(cls)
        initialization_elements.createlongactions(cls)
        initialization_elements.createarealongs(cls)
        initialization_elements.createproceedactions(cls)
        initialization_elements.createpokemon(cls)
        initialization_elements.createtemplates(cls)
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
        Information['unlockablepokemons']=[]
        Information['resources']={}
        Information['flags']={}
        Information['templates']=[]
        Information['cleareddungeons']=cls.cleareddungeons
        Information["corestats"]={}
        Information["corestats"]["basestats"]=cls.corestats.basestats
        Information["corestats"]["modifiers"] = cls.corestats.modifiers
        Information["corestats"]["baseexp"]=cls.corestats.baseexp
        Information["corestats"]["rank"]=cls.corestats.rank
        Information["corestats"]["exprequiredtorank"]=cls.corestats.exprequiredtorank
        Information["corestats"]["improvedactions"] = cls.corestats.improvedactions
        Information["corestats"]["expdropbonus"] = cls.corestats.expdropbonus
        Information["souls"]=cls.souls
        Information["mainname"]=cls.mainname
        Information["availableskill"]=[]
        Information["learnableskills"]=[]
        Information['storylog']=cls.storylog
        for skill in cls.learnableskills:
            Information["learnableskills"].append([[skill[0].name, skill[0].power, skill[0].interval, skill[0].category, skill[0].cost, skill[0].type, skill[0].effect,skill[0].unlockflags],skill[1]])
        for skill in cls.availableskills:
            Information["availableskill"].append([skill.name, skill.power, skill.interval, skill.category, skill.cost, skill.type, skill.effect,skill.unlockflags])
        for flag in cls.flags:
            if cls.flags[flag]!=0:
                Information['flags'][flag]=cls.flags[flag]
        for category in cls.resources:
            for resource in cls.resources[category]:
                Information['resources'][resource.name]=(resource.quantity,resource.max,resource.unlockflags,resource.category,resource.regen)
        for num,template in enumerate(cls.templates):
            if template==[]:
                Information["templates"].append([])

            elif template!=[]:
                Information["templates"].append([[],[]])
                for x in (template[0]):
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
                    pokemondict["num"] = x.number
                    pokemondict["velocity"]=x.velocity
                    pokemondict["type"]=x.type
                    skilllist=[]
                    for singleskill in x.skill:
                        skilllist.append([singleskill.name, singleskill.power, singleskill.interval, singleskill.category, singleskill.cost, singleskill.type, singleskill.effect,singleskill.unlockflags])
                    pokemondict["Skill"]=skilllist
                    pokemondict["Original skill"] = [x.originalskill.name, x.originalskill.power, x.originalskill.interval, x.originalskill.category,
                                            x.originalskill.cost, x.originalskill.type, x.originalskill.effect,x.originalskill.unlockflags]

                    Information["templates"][num][0].append(pokemondict)
                for x in (template[1]):
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
                    pokemondict["num"] = x.number
                    pokemondict["velocity"] = x.velocity
                    pokemondict["type"] = x.type
                    skilllist = []
                    for singleskill in x.skill:
                        skilllist.append(
                            [singleskill.name, singleskill.power, singleskill.interval, singleskill.category,
                             singleskill.cost, singleskill.type, singleskill.effect, singleskill.unlockflags])
                    pokemondict["Skill"] = skilllist
                    pokemondict["Original skill"] = [x.originalskill.name, x.originalskill.power,
                                                     x.originalskill.interval, x.originalskill.category,
                                                     x.originalskill.cost, x.originalskill.type, x.originalskill.effect,x.originalskill.unlockflags]
                    Information["templates"][num][1].append(pokemondict)


        for x in cls.unlockablepokemons:
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
            pokemondict["num"] = x.number
            pokemondict["velocity"] = x.velocity
            pokemondict["type"] = x.type
            skilllist = []
            for singleskill in x.skill:
                skilllist.append(
                    [singleskill.name, singleskill.power, singleskill.interval, singleskill.category, singleskill.cost,
                     singleskill.type, singleskill.effect, singleskill.unlockflags])
            pokemondict["Skill"] = skilllist
            pokemondict["Original skill"] = [x.originalskill.name, x.originalskill.power, x.originalskill.interval,
                                             x.originalskill.category,
                                             x.originalskill.cost, x.originalskill.type, x.originalskill.effect,x.originalskill.unlockflags]
            Information["unlockablepokemon"].append(pokemondict)


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
            pokemondict["num"]=x.number
            pokemondict["velocity"] = x.velocity
            pokemondict["type"] = x.type
            skilllist = []
            for singleskill in x.skill:
                skilllist.append(
                    [singleskill.name, singleskill.power, singleskill.interval, singleskill.category, singleskill.cost,
                     singleskill.type, singleskill.effect, singleskill.unlockflags])
            pokemondict["Skill"] = skilllist
            pokemondict["Original skill"] = [x.originalskill.name, x.originalskill.power, x.originalskill.interval,
                                             x.originalskill.category,
                                             x.originalskill.cost, x.originalskill.type, x.originalskill.effect,x.originalskill.unlockflags]
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
            pokemondict["num"] = x.number
            pokemondict["velocity"] = x.velocity
            pokemondict["type"] = x.type
            skilllist = []
            for singleskill in x.skill:
                skilllist.append(
                    [singleskill.name, singleskill.power, singleskill.interval, singleskill.category, singleskill.cost,
                     singleskill.type, singleskill.effect, singleskill.unlockflags])
            pokemondict["Skill"] = skilllist
            pokemondict["Original skill"] = [x.originalskill.name, x.originalskill.power, x.originalskill.interval,
                                             x.originalskill.category,
                                             x.originalskill.cost, x.originalskill.type, x.originalskill.effect,x.originalskill.unlockflags]
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
    def regenitems(cls):
        for key in cls.resources:
            for item in cls.resources[key]:
                if item.regen:
                    time=int(round(120/item.regen,0))
                    if cls.framecounter%time==0:
                        item.quantity+=1
                        if item.quantity>item.max:
                            item.quantity=item.max

    @classmethod
    def updatebuttons(cls):
        for key in cls.quests:
            for location in cls.quests[key]:
                for i in cls.quests[key][location]:
                    i.update()
        for key in cls.longactions:
            for i in cls.longactions[key]:
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
        for key in cls.arealongs:
            for i in cls.arealongs[key]:
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
                if pokemon.name == cls.mainname:
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
                if pokemon.special<31:
                    cls.corestats.expdropbonus=round(pokemon.special/6,1)
                else:
                    cls.corestats.expdropbonus=round(0.1+5.5*math.log(pokemon.special/10,3),1)

        pokemon.updatestats()
        cls.levelup = None

    @classmethod
    def monsterai(cls,pokemon):
        if pokemon.name=="Training dummy":
            return [0,1,1,0,0][pokemon.turn%5]
        return random.randint(0,len(pokemon.skill)-1)

    @classmethod
    def dungeonprogress(cls):
        alive = [pokemon for pokemon in cls.activedungeon.party if pokemon.currenthp]
        alive2 = [pokemon for pokemon in cls.activedungeon.currentlayout[cls.activedungeon.floor] if pokemon.currenthp]
        if cls.pokemonattacking is None:
            for num,pokemon in enumerate(alive):
                pokemon.cd+=pokemon.velocity/480
                if pokemon.cd>1:
                    cls.pokemonattacking=pokemon
                    Gamelogic.stageofselection =1
            for num,pokemon in enumerate(alive2):
                pokemon.cd+=pokemon.velocity/480
                if pokemon.cd>1:
                    skillnum=cls.monsterai(alive2[num])
                    alive2[num].cd=1-alive2[num].skill[skillnum].interval/4
                    alive2[num].turn+=1
                    target=alive[random.randint(0,len(alive)-1)]
                    damagedealt = alive2[num].skill[skillnum].useskill(alive2[num], target)
                    if alive2[num].skill[skillnum].type in Strong and target.type in Strong[alive2[num].skill[skillnum].type]:
                        cls.activedungeon.log.append(
                            f"Enemy {alive2[num].name} used {alive2[num].skill[skillnum].name} and dealt {numcon(damagedealt)} dmg to {target.name}. It's super effective")
                    elif target.type in Weak and alive2[num].skill[skillnum].type in Weak[target.type]:
                        cls.activedungeon.log.append(
                            f"Enemy {alive2[num].name} used {alive2[num].skill[skillnum].name} and dealt {numcon(damagedealt)} dmg to {target.name}. It's not very effective")
                    else:
                        cls.activedungeon.log.append(
                        f'Enemy {alive2[num].name} used {alive2[num].skill[skillnum].name} and dealt {numcon(damagedealt)} dmg to {target.name}')
                    if cls.tab == "Dungeon":
                        hit = pygame.mixer.Sound('Sounds/ouch.wav')
                        hit.set_volume(cls.volume)
                        pygame.mixer.Sound.play(hit)
                    if target.currenthp == 0:
                        cls.activedungeon.log.append(
                            f'{target.name} fainted!')
                        target.cd = 0
                        target.turn=0
                        alive = [pokemon for pokemon in cls.activedungeon.party if pokemon.currenthp]
                        if not len(alive):
                            cls.activedungeon.generate()
                            cls.activedungeon.log.append('You and your party were defeated')
                            cls.regenpokemonhealt(cls.party[0:5])
                            cls.pokemonattacking=None
                            Gamelogic.stageofselection = 0
                            return
        else:
            if cls.auto:
                if cls.pokemonattacking.originalskill.effect is not False and "aoe" in cls.pokemonattacking.originalskill.effect:
                    cls.attackchosen(cls.pokemonattacking, alive2,
                                     cls.pokemonattacking.originalskill)
                elif cls.pokemonattacking.originalskill.effect is not False and "heal" in cls.pokemonattacking.originalskill.effect:
                    if "aoe" in cls.pokemonattacking.originalskill.effect:
                        cls.attackchosen(cls.pokemonattacking, alive,
                                         cls.pokemonattacking.originalskill)
                    else:
                        pokemontoheal=alive[0]
                        for pokemon in alive:
                            if pokemon.currenthp<=pokemontoheal.currenthp:
                                pokemontoheal=pokemon
                        cls.attackchosen(cls.pokemonattacking, [pokemontoheal],
                                         cls.pokemonattacking.originalskill)


                else:
                    cls.attackchosen(cls.pokemonattacking, [alive2[0]],
                                       cls.pokemonattacking.originalskill)
                cls.pokemonattacking = None
                cls.stageofselection = 0
    @classmethod
    def attackchosen(cls,pokemon,target,skill):
        for target1 in target:
            damagedealt = skill.useskill(pokemon, target1)
            pokemon.cd=1-skill.interval/4
            if skill.effect is not False and "heal" in skill.effect:
                cls.activedungeon.log.append(
                    f'{pokemon.name} restored {numcon(damagedealt)} hp of {target1.name}')

            else:
                if skill.type in Strong and target1.type in Strong[skill.type]:
                    cls.activedungeon.log.append(
                        f"{pokemon.name} dealt {numcon(damagedealt)} dmg to enemy {target1.name}. It's super effective")
                elif target1.type in Weak and skill.type in Weak[target1.type]:
                    cls.activedungeon.log.append(
                        f"{pokemon.name} dealt {numcon(damagedealt)} dmg to enemy {target1.name}. It's not very effective")
                else:
                    cls.activedungeon.log.append(
                    f'{pokemon.name} dealt {numcon(damagedealt)} dmg to enemy {target1.name}')
                if cls.tab == "Dungeon":
                    hit = pygame.mixer.Sound('Sounds/hitting.wav')
                    hit.set_volume(cls.volume)
                    pygame.mixer.Sound.play(hit)
                if target1.currenthp == 0:
                    target1.cd = 0
                    target1.turn= 0
                    cls.activedungeon.log.append(
                        f'Enemy {target1.name} fainted!')
                    cls.corestats.baseexp += (target1.drop['exp'] + cls.corestats.expdropbonus)
                    cls.corestats.baseexp = (round(cls.corestats.baseexp, 1))
                    droplog = f'Enemy {target1.name} dropped {target1.drop["exp"]} exp'
                    for resource in target1.drop['resources']:
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
                    if n <= 33 and target1.name not in ['Training dummy']:
                        if target1.name not in cls.souls:
                            pokemontounlock = target1.copy()
                            cls.souls[pokemontounlock.name] = 0
                            pokemontounlock.phys = 1
                            pokemontounlock.magic = 1
                            pokemontounlock.special = 1
                            pokemontounlock.lvl = 5
                            pokemontounlock.wild = False

                            cls.unlockablepokemons.append(pokemontounlock)
                        cls.souls[target1.name] += souldrop

                        droplog += f',{souldrop} {target1.name} soul'

                    cls.activedungeon.log.append(droplog)
                    alive2 = [pokemon for pokemon in cls.activedungeon.currentlayout[cls.activedungeon.floor] if
                              pokemon.currenthp]
                    if not len(alive2):
                        cls.activedungeon.floor += 1
                        if cls.activedungeon.floor >= len(cls.activedungeon.currentlayout):
                            cls.activedungeon.generate()
                            cls.activedungeon.log.append('You cleared the dungeon!')
                            victory = pygame.mixer.Sound('Sounds/victory.mp3')
                            victory.set_volume(cls.volume)
                            pygame.mixer.Sound.play(victory)
                            cls.regenpokemonhealt(cls.party[0:5])
                            cls.activedungeon.docomplete()
                            if cls.activedungeon.changeflags is not None:
                                for key in cls.activedungeon.changeflags:
                                    cls.flags[key] += cls.activedungeon.changeflags[key]
                            cls.activedungeon.changeflags = None
                        return

    @classmethod
    def regenpokemonhealt(cls, list):
        for pokemon in list:
            pokemon.currenthp = pokemon.actualhp
    @classmethod
    def addskillfunction(cls,pokemon,skill):
        pokemon.skill.append(skill.copy())
        cls.addskill = None
    @classmethod
    def removeskillfunction(cls,pokemon,num):
        pokemon.skill.pop(num)
        cls.removeskill =None


    @classmethod
    def reorderreserve(cls):
        final=[]
        for i in range(len(cls.reserve)+20):
            for e in cls.reserve:
                if e.number==i:
                    final.append(e)
        cls.reserve=final

    @classmethod
    def passivesadd(cls):
        resourcelist=[resource for key in cls.resources for resource in cls.resources[key]]
        for pokemon in cls.party:
            for passive in [passive for passive in pokemon.passive if passive.type=="resourcemax"]:
                for resource in [resource for resource in resourcelist if resource.name==passive.thing]:
                    resource.max+=passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type=="resourceregen"]:
                for resource in [resource for resource in resourcelist if resource.name==passive.thing]:
                    resource.regen+=passive.quantity

            for passive in [passive for passive in pokemon.passive if passive.type == "energymax"]:
                for energy in [energy for energy in cls.energies if energy.name==passive.thing]:
                    energy.max+=passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type == "energyregen"]:
                for energy in [energy for energy in cls.energies if energy.name==passive.thing]:
                    energy.regen+=passive.quantity/120
            for passive in [passive for passive in pokemon.passive if passive.type == "addstats"]:
                cls.corestats.modifiers["Party additive"][passive.thing] += passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type == "mulstats"]:
                cls.corestats.modifiers["Party multiplicative"][passive.thing] += passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type == "longimprove"]:
                if passive.thing not in cls.corestats.improvedactions:
                    cls.corestats.improvedactions[passive.thing]=0
                cls.corestats.improvedactions[passive.thing]+=passive.quantity

    @classmethod
    def passiveremove(cls):
        resourcelist = [resource for key in cls.resources for resource in cls.resources[key]]
        for pokemon in cls.party:
            for passive in [passive for passive in pokemon.passive if passive.type == "resourcemax"]:
                for resource in [resource for resource in resourcelist if resource.name == passive.thing]:
                    resource.max -= passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type=="resourceregen"]:
                for resource in [resource for resource in resourcelist if resource.name==passive.thing]:
                    resource.regen-=passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type == "energymax"]:
                for energy in [energy for energy in cls.energies if energy.name==passive.thing]:
                    energy.max-=passive.quantity
                    energy.quantity=max(0,energy.quantity-passive.quantity)
            for passive in [passive for passive in pokemon.passive if passive.type == "energyregen"]:
                for energy in [energy for energy in cls.energies if energy.name==passive.thing]:
                    energy.regen-=passive.quantity/120
            for passive in [passive for passive in pokemon.passive if passive.type == "addstats"]:
                cls.corestats.modifiers["Party additive"][passive.thing]-=passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type == "mulstats"]:
                cls.corestats.modifiers["Party multiplicative"][passive.thing] -= passive.quantity
            for passive in [passive for passive in pokemon.passive if passive.type == "longimprove"]:
                cls.corestats.improvedactions[passive.thing] -= passive.quantity



    @classmethod
    def frameaction(cls):
        cls.framecounter+=1
        cls.updatebuttons()
        cls.regenenergies()
        cls.regenitems()
        cls.longactionprogress()
        cls.checkflags()
        cls.reorderreserve()
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
            hit = pygame.mixer.Sound('Sounds/button.mp3')
            hit.set_volume(Gamelogic.volume)
            pygame.mixer.Sound.play(hit)
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
            hit = pygame.mixer.Sound('Sounds/button.mp3')
            hit.set_volume(Gamelogic.volume)
            pygame.mixer.Sound.play(hit)
            for key in cls.quests[cls.subtab]:
                for i in cls.quests[cls.subtab][key]:
                    if i.name == cls.quest:
                        i.docost()
