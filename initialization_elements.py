import json
import random
from random import randint
import copy
import pygame
import pokemonlist

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


class Skill:
    def __init__(self, name, power, interval, category, cost=None, type=None, effect=None, unlockflags=None):
        self.name = name
        self.power = power
        self.interval = interval
        self.category = category
        self.cost = cost
        self.type = type
        self.effect = effect
        self.unlockflags = unlockflags

    def useskill(self, user, target):
        multiplier = 1 + self.power / 10
        if self.category == 'Phys':
            attack = multiplier * user.actualpatk
            basedamage = attack / 2 - target.actualpdef / 4
        else:
            attack = multiplier * user.actualmatk
            basedamage = attack / 2 - target.actualmdef / 4
        if basedamage < 0:
            basedamage = 0
        randomdamage = random.uniform(-((basedamage) ** 0.5) / 2, ((basedamage) ** 0.5 / 2))
        damage = max(basedamage + randomdamage, attack / 10)
        target.currenthp -= damage

        if target.currenthp < 0:
            target.currenthp = 0
            target.cd = target.skill.interval * 240
        return damage


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


class Dungeon:
    def __init__(self, parent, name, location, unlockflags, closingflags, changeflags, monsterlist, isvisible=True,
                 isdisabled=False, boss=None, rare=None, usualreward=None, cleared=False, firsttime=None):
        self.parent = parent
        self.name = name
        self.unlockflags = unlockflags
        self.closingflags = closingflags
        self.changeflags = changeflags
        self.monsterlist = monsterlist
        self.isvisible = isvisible
        self.isdisabled = isdisabled
        self.boss = boss
        self.rare = rare
        self.location = location
        self.currentlayout = []
        self.floor = 0
        self.log = []
        self.party = []
        self.usualrewards = usualreward
        self.cleared = cleared
        self.firsttime = firsttime
        for pokemon in self.parent.party[0:min(5, len(self.parent.party))]:
            self.party.append(pokemon.copy())
        if location[0] not in self.parent.dungeons.keys():
            self.parent.dungeons[location[0]] = {}
        if location[1] not in self.parent.dungeons[location[0]].keys():
            self.parent.dungeons[location[0]][location[1]] = []
        self.parent.dungeons[location[0]][location[1]].append(self)

    def generate(self):
        self.floor = 0
        self.log = []
        self.currentlayout = []
        self.party = []
        for pokemon in self.parent.party[0:min(5, len(self.parent.party))]:
            self.party.append(pokemon.copy())
        if self.boss is None:
            for i in range(5):
                k = randint(0, 4)
                n = [3, 3, 4, 4, 5][k]
                self.currentlayout.append([])
                for j in range(n):
                    k = randint(0, len(self.monsterlist) - 1)
                    self.currentlayout[i].append(self.monsterlist[k].copy())
        else:
            self.currentlayout.append([])
            self.currentlayout[0].append(self.boss.copy())

    def docomplete(self):
        if self.usualrewards is not None:
            for i in self.usualrewards:
                if i[0] == 'resource':
                    name = i[1]
                    for energy in [e for e in self.parent.energies if e.name == name]:
                        if energy.max - energy.quantity > -i[2]:
                            energy.quantity += i[2]
                        continue
                    for x in self.parent.resources.keys():
                        for resource in [e for e in self.parent.resources[x] if e.name == name]:
                            resource.quantity += i[2]
                            if resource.quantity > resource.max:
                                resource.quantity = resource.max
                elif i[0] == 'max':
                    name = i[1]
                    for energy in [e for e in self.parent.energies if e.name == name]:
                        energy.max += i[2]
                        continue
                    for x in self.parent.resources.keys():
                        for resource in [e for e in self.parent.resources[x] if e.name == name]:
                            resource.max += i[2]
        if not self.cleared:
            for i in self.firsttime:
                if i[0] == 'resource':
                    name = i[1]
                    for energy in [e for e in self.parent.energies if e.name == name]:
                        if energy.max - energy.quantity > -i[2]:
                            energy.quantity += i[2]
                        continue
                    for x in self.parent.resources.keys():
                        for resource in [e for e in self.parent.resources[x] if e.name == name]:
                            resource.quantity += i[2]
                            if resource.quantity > resource.max:
                                resource.quantity = resource.max
                elif i[0] == 'max':
                    name = i[1]
                    for energy in [e for e in self.parent.energies if e.name == name]:
                        energy.max += i[2]
                        continue
                    for x in self.parent.resources.keys():
                        for resource in [e for e in self.parent.resources[x] if e.name == name]:
                            resource.max += i[2]
                elif i[0] == 'maxlvl':
                    quantity = i[1]
                    for character in [e for e in self.parent.party if e.name == 'You']:
                        character.maxlvl += quantity
            self.cleared = True

    def update(self):
        pass


class Corestats:
    def __init__(self, parent):
        self.parent = parent
        self.basestats = {'hp': 10, 'patk': 10, 'pdef': 10, 'matk': 10, 'mdef': 10}
        self.modifiers = {'Quests': {'type': 'add', 'hp': 1, 'patk': 0, 'pdef': 0, 'matk': 0, 'mdef': 0}}

    def updatepokemons(self):
        for pokemon in self.parent.party:
            pokemon.updatestats()
        for pokemon in self.parent.reserve:
            pokemon.updatestats()

    def finalstats(self):
        final = {}
        for key in self.basestats:
            final[key] = self.basestats[key]
            for modifier in self.modifiers:
                if self.modifiers[modifier]['type'] == 'mul':
                    final[key] *= self.modifiers[modifier][key]
                elif self.modifiers[modifier]['type'] == 'add':
                    final[key] += self.modifiers[modifier][key]
        return final


class Energy:
    def __init__(self, parent, name, quantity, max, unlockflags, color, regen=0, effect=None, isvisible=True):
        self.parent = parent
        self.name = name
        self.quantity = quantity
        self.max = max
        self.unlockflags = unlockflags
        self.regen = regen
        self.effect = effect
        self.isvisible = isvisible
        self.color = color
        parent.energies.append(self)


class Resource:
    def __init__(self, parent, name, quantity, max, unlockflags, category, regen=0, effect=None, resources=None,
                 isvisible=False):
        self.parent = parent
        self.name = name
        self.quantity = quantity
        self.max = max
        self.unlockflags = unlockflags
        self.regen = regen
        self.effect = effect
        self.category = category
        self.isvisible = isvisible
        if resources is not None:
            if category in resources.keys():
                resources[category].append(self)
            else:
                resources[category] = [self]


class menuelement:
    def __init__(self, parent, name, isvisible=False, isdisabled=False, elementlist=None, unlockflags=None,
                 closingflags=None,
                 changeflags=None):
        self.name = name
        self.isvisible = isvisible
        self.parent = parent
        self.unlockflags = unlockflags
        self.closingflags = closingflags
        self.changeflags = changeflags
        self.isdisabled = isdisabled
        if elementlist is not None:
            elementlist.append(self)


class Quests(menuelement):
    def __init__(self, cost=[['Wood', 0, 0, 0]],
                 complete=[['resource', 'Wood', 0, 0, 0]], location=None, requirements=[['Wood', 0, 0, 0]], *args,
                 **kwargs):
        menuelement.__init__(self, elementlist=None, *args, **kwargs)
        if location is not None:
            if location[0] not in self.parent.quests.keys():
                self.parent.quests[location[0]] = {}
            if location[1] not in self.parent.quests[location[0]].keys():
                self.parent.quests[location[0]][location[1]] = []
            self.parent.quests[location[0]][location[1]].append(self)
        self.cost = cost
        self.complete = complete
        self.requirements = requirements

    def docost(self):
        temp = 0
        for i in self.requirements:
            costname = i[0]
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity < i[1]:
                        temp = 1
        if not temp:
            for i in self.cost:
                costname = i[0]
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    if energy.quantity + i[1] > -1 / 240:
                        energy.quantity += i[1]
                    if not energy.quantity:
                        energy.quantity = 0
                        self.docomplete()
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        if resource.quantity >= -i[1]:
                            resource.quantity += i[1]
                            self.docomplete()
        self.parent.quest = None

    def docomplete(self):
        for i in self.complete:
            if i[0] == 'resource':
                name = i[1]
                for energy in [e for e in self.parent.energies if e.name == name]:
                    if energy.max - energy.quantity > -i[2]:
                        energy.quantity += i[2]
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == name]:
                        resource.quantity += i[2]
                        if resource.quantity > resource.max:
                            resource.quantity = resource.max
            elif i[0] == 'max':
                name = i[1]
                for energy in [e for e in self.parent.energies if e.name == name]:
                    energy.max += i[2]
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == name]:
                        resource.max += i[2]
            elif i[0] == 'stat':
                name = i[1]
                self.parent.corestats.modifiers['Quests'][name] += i[2]
                self.parent.corestats.updatepokemons()

        if self.changeflags is not None:
            for key in self.changeflags:
                self.parent.flags[key] += self.changeflags[key]

    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                if i[2] < -i[1]:
                    self.isdisabled = True
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[2] < -i[1]:
                        self.isdisabled = True
                    continue
        for i in self.complete:
            costname = i[1]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[3] = energy.quantity
                i[4] = energy.max
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[3] = resource.quantity
                    i[4] = resource.max
                    continue

        for i in self.requirements:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = energy.quantity
                i[3] = energy.max
                if i[2] < i[1]:
                    self.isdisabled = True
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[2] < i[1]:
                        self.isdisabled = True
                    continue
class Nextaction(menuelement):
    def __init__(self,
                 cost=[['Wood', 0, 0, 0]],complete=[['Wood', 0, 0, 0]],location=None,*args, **kwargs):
        menuelement.__init__(self, elementlist=None, *args, **kwargs)
        if location is not None:
            if location not in self.parent.proceedactions.keys():
                self.parent.proceedactions[location]=[]
            self.parent.proceedactions[location].append(self)
        self.cost = cost
        self.complete = complete
        self.update()

    def docost(self):
        temp = 0
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity + i[1] <= -1 / 240:
                    temp = 1
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity < -i[1]:
                        temp = 1
        if not temp:
            for i in self.cost:
                costname = i[0]
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    energy.quantity += i[1]
                    if energy.quantity < 0:
                        energy.quantity = 0
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        resource.quantity += i[1]
            self.docomplete()
            if self.changeflags is not None:
                for key in self.changeflags:
                    self.parent.flags[key] += self.changeflags[key]

        self.parent.action = None

    def docomplete(self):
        for i in self.complete:
            name = i[0]
            for energy in [e for e in self.parent.energies if e.name == name]:
                if energy.max - energy.quantity > -i[1]:
                    energy.quantity += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == name]:
                    resource.quantity += i[1]
                    if resource.quantity > resource.max:
                        resource.quantity = resource.max


    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                if i[2] < -i[1]:
                    self.isdisabled = True
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[2] < -i[1]:
                        self.isdisabled = True
                    continue
        temp = 1
        for i in self.complete:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                if i[3] > i[2]:
                    temp = 0
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[3] > i[2]:
                        temp = 0
                    continue
        if self.complete[0][1] != 0 and temp:
            self.isdisabled = True

class Instantactions(menuelement):
    def __init__(self,
                 cost=[['Wood', 0, 0, 0]],
                 complete=[['Wood', 0, 0, 0]], location=None, area=False, *args, **kwargs):
        menuelement.__init__(self, elementlist=None, *args, **kwargs)
        if location is not None:
            if not area:
                if location not in self.parent.instantactions.keys():
                    self.parent.instantactions[location] = []
                self.parent.instantactions[location].append(self)
            else:
                if location not in self.parent.areainstants.keys():
                    self.parent.areainstants[location] = []
                self.parent.areainstants[location].append(self)

        self.cost = cost
        self.complete = complete
        self.resourcetype = []
        self.update()


    def docost(self):
        temp = 0
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity + i[1] <= -1 / 240:
                    temp = 1
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity <= -i[1]:
                        temp = 1
        if not temp:
            for i in self.cost:
                costname = i[0]
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    energy.quantity += i[1]
                    if energy.quantity < 0:
                        energy.quantity = 0
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        resource.quantity += i[1]
            self.docomplete()
        self.parent.action = None

    def docomplete(self):
        for i in self.complete:
            name = i[0]
            for energy in [e for e in self.parent.energies if e.name == name]:
                if energy.max - energy.quantity > -i[1]:
                    energy.quantity += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == name]:
                    resource.quantity += i[1]
                    if resource.quantity > resource.max:
                        resource.quantity = resource.max

    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                if i[2] < -i[1]:
                    self.isdisabled = True
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[2] < -i[1]:
                        self.isdisabled = True
                    continue
        temp = 1
        for i in self.complete:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                if i[3] > i[2]:
                    temp = 0
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[3] > i[2]:
                        temp = 0
                    continue
        if self.complete[0][1] != 0 and temp:
            self.isdisabled = True


class Loopaction(menuelement):
    def __init__(self, progress=0, speed=1 / 1200, isactive=False, location=None,
                 cost=[['Wood', 0, 0, 0]], progresscost=[['Wood', 0, 0, 0]],
                 progresseffect=[['Wood', 0, 0, 0]], complete=[['Wood', 0, 0, 0]], area=False, *args, **kwargs):
        menuelement.__init__(self, elementlist=None, *args, **kwargs)
        if location is not None:
            if not area:
                if location not in self.parent.loopactions.keys():
                    self.parent.loopactions[location] = []
                self.parent.loopactions[location].append(self)
            else:
                if location not in self.parent.arealoops.keys():
                    self.parent.arealoops[location] = []
                self.parent.arealoops[location].append(self)
        self.progress = progress
        self.isactive = isactive
        self.speed = speed
        self.previouslyactive = False
        self.cost = cost
        self.progresscost = progresscost
        self.progresseffect = progresseffect
        self.complete = complete

    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                if i[2] < -i[1]:
                    self.isdisabled = True
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[2] < -i[1]:
                        self.isdisabled = True
                    continue
        for i in self.progresscost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    continue
        for i in self.progresseffect:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.quantity, 2)
                i[3] = energy.max
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    continue
        temp = 1
        for i in self.complete:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = energy.quantity
                i[3] = energy.max
                if i[3] > i[2]:
                    temp = 0
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    if i[3] > i[2]:
                        temp = 0
                    continue
        if self.complete[0][1] != 0 and temp:
            self.isdisabled = True

    def activation(self):
        self.parent.deactivateloopactions()
        self.isactive = True

    def docost(self):
        costpaid = True
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1]:
                    energy.quantity += i[1]
                else:
                    costpaid = False
                if not energy.quantity:
                    energy.quantity = 0
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity >= -i[1]:
                        resource.quantity += i[1]
                    else:
                        costpaid = False
        return costpaid

    def dopassiveeffect(self):
        for i in self.progresseffect:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1] and energy.quantity + i[
                    1] < energy.max:
                    energy.quantity += i[1]
                elif costname == 'Energy':
                    for key in self.parent.loopactions:
                        for e in self.parent.loopactions[key]:
                            if e.previouslyactive:
                                e.activation()
                                e.previouslyactive = False

                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1] and resource.quantity + i[1] < resource.max:
                        self.parent.resources[x][costname].quantity += i[1]

    def dopassiveaction(self):
        for i in self.progresscost:
            if i[1] != 0:
                costname = i[0]
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    if energy.quantity >= -i[1]:
                        energy.quantity += i[1]
                        self.dopassiveeffect()
                    elif costname == 'Energy':
                        self.previouslyactive = True
                        self.parent.loopactions['Common loopactions'][0].activation()
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        if resource.quantity > -i[1]:
                            resource.quantity += i[1]

                            self.dopassiveeffect()
            else:
                self.dopassiveeffect()

    def dofinishaction(self):
        for i in self.complete:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1]:
                    energy.quantity += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]:
                        resource.quantity += i[1]
                        if resource.quantity > resource.max:
                            resource.quantity = resource.max


class Pokemon(menuelement):
    def __init__(self, hp, atk, dif, satk, sdif, maxlvl=1000, unlocked=0, lvl=0, phys=0, magic=0,
                 special=0, drop=None,
                 skill=None, wild=True,
                 *args, **kwargs):

        menuelement.__init__(self, *args, **kwargs)
        self.patk = atk
        self.pdef = dif
        self.matk = satk
        self.mdef = sdif
        self.hp = hp
        self.lvl = lvl
        self.unlocked = unlocked
        self.maxlvl = maxlvl
        self.phys = phys
        self.magic = magic
        self.special = special
        self.wild = wild
        if drop == None:
            self.drop = {'exp': 1, 'resources': [['Physical gems', 1, 10], ['Magical gems', 1, 10],
                                                 ['Special gems', 1, 10]]}
        else:
            self.drop = drop

        self.updatestats()
        if skill is not None:
            self.skill = Skill(*skill)
            self.cd = self.skill.interval * 240
        else:
            self.skill = Skill('Tackle', 7, 2.8, 'Phys', None, None, None, None)
            self.cd = self.skill.interval * 240

    def copy(self):
        return copy.deepcopy(self)

    def updatestats(self):
        if self.name == 'You':
            if self.lvl <= 10:
                self.scaling1 = 1 / 10 + self.phys * 9 / 100
                self.scaling2 = 1 / 10 + self.magic * 9 / 100
            else:
                self.scaling1 = 1 + self.phys * 8 / 100
                self.scaling2 = 1 + self.magic * 8 / 100

            self.actualhp = self.scaling1 * self.parent.corestats.finalstats()['hp']
            self.actualpatk = self.scaling1 * self.parent.corestats.finalstats()['patk']
            self.actualpdef = self.scaling1 * self.parent.corestats.finalstats()['pdef']
            self.actualmatk = self.scaling2 * self.parent.corestats.finalstats()['matk']
            self.actualmdef = self.scaling2 * self.parent.corestats.finalstats()['mdef']
            self.currenthp = self.actualhp


        elif not self.wild:
            self.scaling1 = ((self.phys) / self.maxlvl) * (self.hp / 100)
            self.scaling2 = ((self.magic) / self.maxlvl) * (self.matk / 100)
            self.actualhp = round(
                self.parent.corestats.finalstats()['hp'] * self.scaling1, 1)
            self.actualpatk = round(
                self.parent.corestats.finalstats()['patk'] * self.scaling1, 1)
            self.actualpdef = round(
                self.parent.corestats.finalstats()['pdef'] * self.scaling1, 1)
            self.actualmatk = round(
                self.parent.corestats.finalstats()['matk'] * self.scaling2, 1)
            self.actualmdef = round(
                self.parent.corestats.finalstats()['mdef'] * self.scaling2, 1)

            self.currenthp = self.actualhp
        else:
            self.scaling1 = ((self.phys) / self.maxlvl) * (self.hp / 100)
            self.scaling2 = ((self.magic) / self.maxlvl) * (self.matk / 100)
            self.actualhp = round(
                10 * self.scaling1, 1)
            self.actualpatk = round(
                10 * self.scaling1, 1)
            self.actualpdef = round(
                10 * self.scaling1, 1)
            self.actualmatk = round(
                10 * self.scaling2, 1)
            self.actualmdef = round(
                10 * self.scaling2, 1)

            self.currenthp = self.actualhp


def getgamestate():
    f = open("gamestate.json")
    Information = json.load(f)
    return Information


def createmenu(parent):
    menuelement(parent=parent, name='Main', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Party', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Training', isvisible=False, elementlist=parent.mainelements,
                unlockflags={'Main': 1})
    menuelement(parent=parent, name='Routine', isvisible=False, elementlist=parent.mainelements,
                unlockflags={'Main': 2})
    menuelement(parent=parent, name='Story', isvisible=False, elementlist=parent.mainelements, unlockflags={'Main': 2})
    menuelement(parent=parent, name='Dungeon', isvisible=False, elementlist=parent.mainelements,
                unlockflags={'Father': 7})
    menuelement(parent=parent, name='Settings', isvisible=True, elementlist=parent.mainelements)


def createmainsubmenu(parent):
    menuelement(parent=parent, name='Village', isvisible=True, elementlist=parent.mainsubelements)
    menuelement(parent=parent, name='Forest', elementlist=parent.mainsubelements,
                unlockflags={'Main': 1})
    menuelement(parent=parent, name='City', elementlist=parent.mainsubelements, unlockflags={'Main': 2})
    menuelement(parent=parent, name='Coast', elementlist=parent.mainsubelements,
                unlockflags={'Main': 1})
    menuelement(parent=parent, name='Jungle', elementlist=parent.mainsubelements,
                unlockflags={'Main': 1})
    menuelement(parent=parent, name='Astral plane', elementlist=parent.mainsubelements,
                unlockflags={'Main': 1})


def createpartytabs(parent):
    menuelement(parent=parent, name='Party selection', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Level up', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Quest', isvisible=False, elementlist=parent.partyelements, unlockflags={'Main': 2})
    menuelement(parent=parent, name='Bestiary', isvisible=False, elementlist=parent.partyelements,
                unlockflags={'Main': 2})
    menuelement(parent=parent, name='SKill', isvisible=False, elementlist=parent.partyelements, unlockflags={'Main': 2})


def createpokemon(parent):
    Information = getgamestate()
    pokemonlist.createpokemonlist(parent)
    for pokemonkey in Information['party']:
        Pokemon(parent=parent, wild=False, elementlist=parent.party, **pokemonkey)
    for pokemonkey in Information['reserve']:
        Pokemon(parent=parent, wild=False, elementlist=parent.reserve, **pokemonkey)

def createtemplates(parent):
    Information = getgamestate()
    for num,template in enumerate(Information['templates']):
        if template==[]:
            parent.templates.append([])
        else:
            late=[[],[]]
            for partypok in Information['templates'][num][0]:
                Pokemon(parent=parent, wild=False, elementlist=late[0], **partypok)
            for reservepok in Information['templates'][num][1]:
                Pokemon(parent=parent, wild=False, elementlist=late[1], **reservepok)
            parent.templates.append(late)


def createinstantactions(parent):
    Instantactions(parent=parent, name='Ponder the future', isvisible=True,
                   location='Common actions', cost=[['Energy', -1, 0, 0]],
                   complete=[['Fate', +1, 0, 0]])
    Instantactions(parent=parent, name='Cut wood', isvisible=True, location='Woodcutting',
                   unlockflags={'Father': 2}, cost=[['Endurance', -1, 0, 0]],
                   complete=[['Wood', 1, 0, 0]])
    Instantactions(parent=parent, name='"Eat" herbs', isvisible=True, location='Garden activities',
                   unlockflags={'Mother': 7}, cost=[['Herbs', -1, 0, 0]],
                   complete=[['Fate', 5, 0, 0]])


def createareainstant(parent):
    Instantactions(parent=parent, name='Look for weeds', isvisible=True, location='Village',
                   unlockflags={'Mother': 5}, cost=[['Energy', -0.4, 0, 0]], area=True,
                   complete=[['Weeds', 1, 0, 0], ['Gold', 2, 0, 0]])


def createloopactions(parent):
    Loopaction(parent=parent, name='Rest', isvisible=True,
               location='Common loopactions', speed=1 / 1200,
               progresseffect=[['Energy', 1 / 240, 0, 0]])
    Loopaction(parent=parent, name='Parse through weeds', isvisible=True,
               location='Garden', speed=1 / 240, cost=[['Weeds', -5, 0, 0]],
               progresscost=[['Energy', -1 / 240, 0, 0]], complete=[['Herbs', 1, 0, 0]],
               unlockflags={'Mother': 5})
    Loopaction(parent=parent, name='Meditate', isvisible=True,
               location='Your room', speed=1 / 240,
               progresscost=[['Energy', -1 / 240, 0, 0]], complete=[['Fate', 1, 0, 0]],
               unlockflags={'Zen': 1})


def createarealoops(parent):
    Loopaction(parent=parent, name='Exercise', isvisible=True,
               location='Village', speed=1 / 600, area=True,
               progresscost=[['Energy', -1 / 240, 0, 0]], progresseffect=[['Endurance', 1 / 240, 0, 0]],
               unlockflags={'Father': 2})


def createquests(parent):
    Quests(parent=parent, name='Talk to Father 1/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 0}, closingflags={'Father': 1}, changeflags={'Father': 1,'Popup':2},
                   cost=[['Fate', -5, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]]
                   )
    Quests(parent=parent, name='Talk to Father 2/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 1}, closingflags={'Father': 2}, changeflags={'Father': 1,'Popup':3},
                   cost=[['Fate', -10, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]]
                   )
    Quests(parent=parent, name='Talk to Father 3/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 2}, closingflags={'Father': 3}, changeflags={'Father': 1},
                   cost=[['Wood', -1, 0, 0]], complete=[['max', 'Wood', 2, 0, 0]]
                   )
    Quests(parent=parent, name='Talk to Father 4/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 3}, closingflags={'Father': 4}, changeflags={'Father': 1},
                   cost=[['Wood', -3, 0, 0]], complete=[['max', 'Wood', 2, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 5/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 4}, closingflags={'Father': 5}, changeflags={'Father': 1},
                   cost=[['Wood', -5, 0, 0]], complete=[['max', 'Wood', 2, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 6/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 5}, closingflags={'Father': 6}, changeflags={'Father': 1},
                   cost=[['Wood', -7, 0, 0]], complete=[['max', 'Wood', 3, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 7/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 6}, closingflags={'Father': 7}, changeflags={'Father': 1,'Popup':4},
                   cost=[['Wood', -10, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 8/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 7}, closingflags={'Father': 8}, changeflags={'Father': 1,'Popup':5},
                   cost=[['Physical gems', -1, 0, 0]], complete=[['max', 'Physical gems', 19, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 9/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 8}, closingflags={'Father': 9}, changeflags={'Father': 1},
                   cost=[['Magical gems', -1, 0, 0]], complete=[['max', 'Magical gems', 19, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 10/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 9}, closingflags={'Father': 10}, changeflags={'Father': 1},
                   cost=[['Special gems', -1, 0, 0]], complete=[['max', 'Special gems', 19, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 11/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 10}, closingflags={'Father': 11}, changeflags={'Father': 1},
                   cost=[['Fate', -20, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Father 12/12', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Father': 11}, closingflags={'Father': 12}, changeflags={'Father': 1},
                   cost=[['Fate', -35, 0, 0]],
                   complete=[['max', 'Fate', 10, 0, 0], ['stat', 'hp', 5, 0, 0], ['stat', 'patk', 5, 0, 0],
                             ['stat', 'pdef', 5, 0, 0],
                             ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 1/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 1}, closingflags={'Mother': 2}, changeflags={'Mother': 1},
                   cost=[['Fate', -45, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 2/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 2}, closingflags={'Mother': 3}, changeflags={'Mother': 1},
                   cost=[['Fate', -20, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 3/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 3}, closingflags={'Mother': 4}, changeflags={'Mother': 1},
                   cost=[['Fate', -25, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 4/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 4}, closingflags={'Mother': 5}, changeflags={'Mother': 1},
                   cost=[['Fate', -30, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 5/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 5}, closingflags={'Mother': 6}, changeflags={'Mother': 1},
                   cost=[['Weeds', -5, 0, 0]], complete=[['max', 'Weeds', 10, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 6/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 6}, closingflags={'Mother': 7}, changeflags={'Mother': 1},
                   cost=[['Herbs', -1, 0, 0]], complete=[['max', 'Herbs', 3, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 7/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 7}, closingflags={'Mother': 8}, changeflags={'Mother': 1},
                   cost=[['Herbs', -4, 0, 0]], complete=[['max', 'Herbs', 3, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 8/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 8}, closingflags={'Mother': 9}, changeflags={'Mother': 1},
                   cost=[['Herbs', -7, 0, 0]], complete=[['max', 'Herbs', 3, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 9/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 9}, closingflags={'Mother': 10}, changeflags={'Mother': 1},
                   cost=[['Herbs', -10, 0, 0]],
                   complete=[['stat', 'hp', 5, 0, 0], ['stat', 'patk', 5, 0, 0], ['stat', 'pdef', 5, 0, 0],
                             ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Mother 10/10', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 10}, closingflags={'Mother': 11}, changeflags={'Mother': 1},
                   cost=[['Fate', -40, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Brother 1/3', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Brother': 1}, closingflags={'Brother': 2}, changeflags={'Brother': 1},
                   cost=[['Fate', -80, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to Brother 2/3', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Brother': 2}, closingflags={'Brother': 3}, changeflags={'Brother': 1},
                   cost=[['Fate', -90, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]]
                   )
    Quests(parent=parent, name='Talk to Brother 3/3', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Brother': 3}, closingflags={'Brother': 4}, changeflags={'Brother': 1},
                   cost=[['Fate', -100, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]]
                   )
    Quests(parent=parent, name='Talk with Billy the kid 1/3', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Mother': 1}, closingflags={'Billy': 1}, changeflags={'Billy': 1},
                   cost=[['Butterfly wings', -5, 0, 0]], complete=[['max', 'Butterfly wings', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk with Billy the kid 2/3', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Billy': 1}, closingflags={'Billy': 2}, changeflags={'Billy': 1},
                   cost=[['Butterfly wings', -10, 0, 0]], complete=[['max', 'Butterfly wings', 5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk with Billy the kid 3/3', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Billy': 2}, closingflags={'Billy': 3}, changeflags={'Billy': 1},
                   cost=[['Butterfly wings', -20, 0, 0]],
                   complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                             ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to the zen master 1/5', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Mother': 5}, closingflags={'Zen': 1}, changeflags={'Zen': 1},
                   cost=[['Gold', -20, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to the zen master 2/5', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Zen': 1}, closingflags={'Zen': 2}, changeflags={'Zen': 1},
                   cost=[['Gold', -30, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
                   )
    Quests(parent=parent, name='Talk to the zen master 3/5', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Zen': 2}, closingflags={'Zen': 3}, changeflags={'Zen': 1},
                   cost=[['Gold', -40, 0, 0]],
                   complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                             ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
                   )
    Quests(parent=parent, name='Talk to the zen master 4/5', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Zen': 3}, closingflags={'Zen': 4}, changeflags={'Zen': 1},
                   cost=[['Gold', -50, 0, 0]],
                   complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                             ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
                   )
    Quests(parent=parent, name='Talk to the zen master 5/5', isvisible=True,
                   location=['Village', 'Village'],
                   unlockflags={'Zen': 4}, closingflags={'Zen': 5}, changeflags={'Zen': 1},
                   cost=[['Gold', -60, 0, 0]],
                   complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                             ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
                   )
    Quests(parent=parent, name='Butcher shop 1/6', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Mother': 11}, closingflags={'Butcher': 1}, changeflags={'Butcher': 1},
                   cost=[['Frog legs', -5, 0, 0]], complete=[['max', 'Frog legs', 5, 0, 0]]
                   )
    Quests(parent=parent, name='Butcher shop 2/6', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Butcher': 1}, closingflags={'Butcher': 2}, changeflags={'Butcher': 1},
                   cost=[['Frog legs', -10, 0, 0]], complete=[['max', 'Frog legs', 5, 0, 0]]
                   )
    Quests(parent=parent, name='Butcher shop 3/6', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Butcher': 2}, closingflags={'Butcher': 3}, changeflags={'Butcher': 1},
                   cost=[['Frog legs', -10, 0, 0]],
                   complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                             ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
                   )
    Quests(parent=parent, name='Butcher shop 4/6', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Butcher': 3, 'Brother': 1}, closingflags={'Butcher': 4}, changeflags={'Butcher': 1},
                   cost=[['Cow hide', -5, 0, 0]],
                   complete=[['max', 'Cow hide', 5, 0, 0]]
                   )
    Quests(parent=parent, name='Butcher shop 5/6', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Butcher': 4}, closingflags={'Butcher': 5}, changeflags={'Butcher': 1},
                   cost=[['Cow hide', -10, 0, 0]],
                   complete=[['max', 'Cow hide', 5, 0, 0]]
                   )
    Quests(parent=parent, name='Butcher shop 6/6', isvisible=True,
                   location=['Village', 'Home'],
                   unlockflags={'Butcher': 5}, closingflags={'Butcher': 6}, changeflags={'Butcher': 1},
                   cost=[['Cow hide', -10, 0, 0]],
                   complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                             ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
                   )

    '''Quests(parent=parent, name='Wood quest2', isvisible=True,
                   location=['Village', 'old house'],
                   cost=[['Wood', -10, 0, 0]], complete=[['resource', 'Wood', 20, 0, 0]],
                   unlockflags={'Dubious home': 0, }, closingflags={'Dubious home': 2}, changeflags={'Dubious home': 1})
    Quests(parent=parent, name='Wood quest3', isvisible=True,
                   complete=[['stat', 'hp', 20, 0, 0], ['stat', 'patk', 1000, 0, 0], ['stat', 'pdef', 70, 0, 0],
                             ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 10, 0, 0]],
                   location=['Village', 'old house 2'],
                   unlockflags={'Dubious home': 0, }, closingflags={'Dubious home': 3}, changeflags={'Dubious home': 1})'''

def createproceedactions(parent):
    Nextaction(parent=parent,name='Unlock the world',location='Village',unlockflags={'Main': 1}, closingflags={'Main':2}, changeflags={'Main': 1},cost=[['Fate', -10, 0, 0]])

def loadflags(parent):
    Information = getgamestate()
    for flag in Information['flags']:
        parent.flags[flag] = Information['flags'][flag]


def createresources(parent):
    Information = getgamestate()
    for resourcename in Information['resources']:
        if resourcename not in ['Fate', 'Physical gems', 'Magical gems', 'Special gems']:
            Resource(parent, resourcename, *Information['resources'][resourcename], resources=parent.resources)
    parent.fate = Resource(parent, 'Fate', *Information['resources']['Fate'], 0, resources=parent.resources)
    parent.physgems = Resource(parent, 'Physical gems', *Information['resources']['Physical gems'],
                               resources=parent.resources)
    parent.magicgems = Resource(parent, 'Magical gems', *Information['resources']['Magical gems'],
                                resources=parent.resources)
    parent.specialgems = Resource(parent, 'Special gems', *Information['resources']['Special gems'],
                                  resources=parent.resources)


def createenergies(parent):
    Energy(parent=parent, name='Energy', quantity=5, max=5, unlockflags={'Father': 0}, color=red, regen=0)
    Energy(parent=parent, name='Endurance', quantity=0, max=1, unlockflags={'Father': 2}, color=(255, 255, 0),
           regen=0)
    Energy(parent=parent, name='Mana', quantity=0, max=1, unlockflags={'Father': 14}, color=(0, 0, 205),
           isvisible=False,
           regen=1 / 240)
    Energy(parent=parent, name='Fire', quantity=0, max=1, unlockflags={'Father': 14}, color=orange, isvisible=False,
           regen=1 / 240)
    Energy(parent=parent, name='Wind', quantity=0, max=1, unlockflags={'Father': 14}, color=teal, isvisible=False,
           regen=1 / 240)
    Energy(parent=parent, name='Earth', quantity=0, max=1, unlockflags={'Father': 14}, color=brown, isvisible=False,
           regen=1 / 240)


def createdungeons(parent):
    Dungeon(parent=parent, name="Field", location=['Village', 'Surroundings'], changeflags={'Brother': 1},
            unlockflags={'Mother': 11}, closingflags={}, usualreward=[['resource', 'Special gems', 1, 0, 0]],
            firsttime=[['maxlvl', 7]],
            monsterlist=[parent.pokemonlist[i].copy() for i in range(3, 6)])
    Dungeon(parent=parent, name="Garden", location=['Village', 'Home'], changeflags={'Mother': 1},
            unlockflags={'Father': 12}, closingflags={}, usualreward=[['resource', 'Magical gems', 1, 0, 0]],
            firsttime=[['maxlvl', 6]],
            monsterlist=[parent.pokemonlist[i].copy() for i in range(1, 4)])
    Dungeon(parent=parent, name="Training hall", location=['Village', 'Home'], changeflags={'Main': 1,'Popup':5},
            unlockflags={'Father': 7}, closingflags={}, usualreward=[['resource', 'Physical gems', 1, 0, 0]],
            firsttime=[['maxlvl', 5]],
            monsterlist=[], boss=parent.pokemonlist[0].copy())
    Dungeon(parent=parent, name="Brother fight", location=['Village', 'Surroundings'], changeflags={},
            unlockflags={'Brother': 4}, closingflags={}, firsttime=[['maxlvl', 10]],
            monsterlist=[], boss=parent.pokemonlist[6].copy())
