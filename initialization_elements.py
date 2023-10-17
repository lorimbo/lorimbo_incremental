import json
import random
from random import randint
import copy
import pygame
import pokemonlist
import questlines
import tooltips
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

Weak={'Fire':['Water','Ground'],'Grass':['Fire'],'Water':['Electric','Grass'],'Ground':['Water','Grass'],'Electric':['Ground']}
Strong={'Fire':['Grass'],'Grass':['Water','Ground'],'Water':['Fire','Ground'],'Ground':['Fire','Electric'],'Electric':['Water'],'Dark':['Light'],'Light':['Dark']}


class Passive:
    def __init__(self,thing,type,maxpower,percentage):
        self.thing=thing
        self.type=type
        self.quantity=maxpower/2+(maxpower/2)*percentage
        self.maxpower=maxpower
        self.percentage=percentage


class Skill:
    def __init__(self, name, power, interval, category, cost=False, type='Normal', effect=False, unlockflags=False):
        self.name = name
        self.power = power
        self.interval = interval
        self.category = category
        self.cost = cost
        self.type = type
        self.effect = effect
        self.unlockflags = unlockflags
    def copy(self):
        return copy.deepcopy(self)

    def useskill(self, user, target):
        if self.effect is not False and "heal" in self.effect:
            multiplier = 1 + self.power / 10
            baseheal = multiplier * user.actualmatk/4
            randomheal = random.uniform(-((baseheal) ** 0.5) / 2, ((baseheal) ** 0.5 / 2))
            damage = max(baseheal + randomheal, baseheal / 2.5)
            if target.currenthp > 0:
                target.currenthp += damage
            if target.currenthp > target.actualhp:
                target.currenthp = target.actualhp
            return damage


        else:
            multiplier = 1 + self.power / 10
            if self.category == 'Phys':
                attack = multiplier * user.actualpatk
                basedamage = attack / 2 - target.actualpdef / 4
            else:
                attack = multiplier * user.actualmatk
                basedamage = attack / 2 - target.actualmdef / 4
            if basedamage < 0:
                basedamage = 0
            if self.type in Strong and target.type in Strong[self.type]:
                basedamage*=2
            elif target.type in Weak and self.type in Weak[target.type]:
                basedamage /= 2

            randomdamage = random.uniform(-((basedamage) ** 0.5) / 2, ((basedamage) ** 0.5 / 2))
            damage = max(basedamage + randomdamage, attack / 10)
            target.currenthp -= damage

            if target.currenthp < 0:
                target.currenthp = 0
                target.cd = 0
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
        self.len = len(self.log)
        self.previouslen= self.len
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
        for pokemon in self.party:
            pokemon.cd=round(random.random()/4,1)
        if self.boss is None:
            for i in range(5):
                k = randint(0, 4)
                n = [3, 3, 4, 4, 5][k]
                self.currentlayout.append([])
                for j in range(n):
                    k = randint(0, len(self.monsterlist) - 1)
                    self.currentlayout[i].append(self.monsterlist[k].copy())
                    self.currentlayout[i][-1].cd=round(random.random()/4,1)
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
                    for character in [e for e in self.parent.party if e.name ==self.parent.mainname]:
                        character.maxlvl += quantity
            self.cleared = True
            self.parent.cleareddungeons.append(self.name)

    def update(self):
        pass


class Corestats:
    def __init__(self, parent):
        self.parent = parent
        self.basestats = {'hp': 10, 'patk': 10, 'pdef': 10, 'matk': 10, 'mdef': 10}
        self.modifiers = {'Quests': {'type': 'add', 'hp': 1, 'patk': 0, 'pdef': 0, 'matk': 0, 'mdef': 0},
                          'Party additive':{'type': 'add', 'hp': 0, 'patk': 0, 'pdef': 0, 'matk': 0, 'mdef': 0},
                          'Party multiplicative':{'type': 'mul', 'hp': 0, 'patk': 0, 'pdef': 0, 'matk': 0, 'mdef': 0}}
        self.improvedactions=[]
        self.baseexp=2000
        self.rank=0
        self.exprequiredtorank = 500
        self.expdropbonus=0
        self.skillpoints=0

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
        for flagdict in [self.unlockflags,self.closingflags,self.changeflags]:
            if flagdict is not None:
                for flagname in flagdict:
                    if flagname not in parent.flags:
                        parent.flags[flagname]=0
        self.isdisabled = isdisabled
        if elementlist is not None:
            elementlist.append(self)

class Shopitem(menuelement):
    def __init__(self,cost,*args,**kwargs):
        menuelement.__init__(self, *args, **kwargs)
        self.cost=cost
    def buy(self):
        gold = [e for e in self.parent.resources['Gold'] if e.name == 'Gold'][0]
        item=None
        for category in self.parent.resources:
            for object in self.parent.resources[category]:
                if object.name==self.name:
                    item=object
        if item is not None:
            if gold.quantity<self.cost or item.quantity>= item.max:
                toopoor = pygame.mixer.Sound('Sounds/toopoor.mp3')
                toopoor.set_volume(self.parent.volume)
                pygame.mixer.Sound.play(toopoor)
            else:
                gold.quantity-=self.cost
                item.quantity+=1
                purchase = pygame.mixer.Sound('Sounds/purchase.mp3')
                purchase.set_volume(self.parent.volume)
                pygame.mixer.Sound.play(purchase)


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
            temp2=0
            for i in self.cost:
                costname = i[0]
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    if energy.quantity + i[1] > -1 / 120:
                        energy.quantity += i[1]
                    else:
                        temp2=1
                    if not energy.quantity:
                        energy.quantity = 0
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        if resource.quantity >= -i[1]:
                            resource.quantity += i[1]
                        else:
                            temp2=1
            if not temp2:
                self.docomplete = self.docomplete()
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
            elif i[0] == 'stats':
                name = i[1]
                self.parent.corestats.modifiers['Quests'][name] += i[2]
                self.parent.corestats.updatepokemons()
        if self.name in tooltips.description:
            now = (datetime.datetime.now())
            self.parent.storylog.append([str(now)[0:19],tooltips.storydescription[self.name],self.name])


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
                if energy.quantity + i[1] <= -1 / 120:
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
                if energy.quantity + i[1] <= -1 / 120:
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


class Longaction(menuelement):
    def __init__(self, progress=0, speed=1 / 1200, isactive=False, location=None,
                 cost=[['Wood', 0, 0, 0]], progresscost=[['Wood', 0, 0, 0]],
                 progresseffect=[['Wood', 0, 0, 0]], complete=[['Wood', 0, 0, 0]], area=False, *args, **kwargs):
        menuelement.__init__(self, elementlist=None, *args, **kwargs)
        if location is not None:
            if not area:
                if location not in self.parent.longactions.keys():
                    self.parent.longactions[location] = []
                self.parent.longactions[location].append(self)
            else:
                if location not in self.parent.arealongs.keys():
                    self.parent.arealongs[location] = []
                self.parent.arealongs[location].append(self)
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
        self.parent.deactivatelongactions()
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
        self.costpaid = costpaid
        return self.costpaid

    def dopassiveeffect(self):
        m=1
        if self.name in self.parent.corestats.improvedactions:
            m+=self.parent.corestats.improvedactions[self.name]
        for i in self.progresseffect:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1] and energy.quantity + i[1]*m < energy.max:
                    energy.quantity += (i[1]*m)
                elif costname == 'Energy':
                    energy.quantity=energy.max
                    for key in self.parent.longactions:
                        for e in self.parent.longactions[key]:
                            if e.previouslyactive:
                                e.activation()
                                e.previouslyactive = False
                    for key in self.parent.arealongs:
                        for e in self.parent.arealongs[key]:
                            if e.previouslyactive:
                                e.activation()
                                e.previouslyactive = False

                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]*m:
                        if resource.quantity + i[1]*m < resource.max:
                            self.parent.resources[x][costname].quantity += i[1]*m
                        else:
                            self.parent.resources[x][costname].quantity=self.parent.resources[x][costname].max


    def dopassiveaction(self):
        for i in self.progresscost:
            if i[1] != 0:
                temp=1
                costname = i[0]
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    if energy.quantity >= -i[1]:
                        energy.quantity += i[1]
                    elif costname == 'Energy':
                        temp=0
                        self.previouslyactive = True
                        self.parent.longactions['Common longactions'][0].activation()
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        if resource.quantity > -i[1]:
                            resource.quantity += i[1]
                        else:
                            temp=0
                if temp:
                    self.dopassiveeffect()
            else:
                self.dopassiveeffect()

    def dofinishaction(self):
        m = 1
        if self.name in self.parent.corestats.improvedactions:
            m += self.parent.corestats.improvedactions[self.name]
        for i in self.complete:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1]*m:
                    energy.quantity += i[1]*m
                    if energy.quantity>energy.max:
                        energy.quantity=energy.max
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]*m:
                        resource.quantity += i[1]*m
                        if resource.quantity > resource.max:
                            resource.quantity = resource.max


class Pokemon(menuelement):
    def __init__(self, hp, atk, dif, satk, sdif, maxlvl=1000, unlocked=0, lvl=0, phys=0, magic=0,
                 special=0, drop=None,
                 skill=None,num=0, wild=True,originalskill=None,passive=[],velocity=1,type='Normal',
                 *args, **kwargs):

        menuelement.__init__(self, *args, **kwargs)
        self.number=num
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
        self.passive=passive
        self.velocity=velocity
        self.cd=0
        self.type=type
        for passive in self.passive:
            passive.percentage = (self.special / self.maxlvl)
            passive.quantity = passive.maxpower / 2 + (passive.maxpower / 2) * passive.percentage

        if drop == None:
            self.drop = {'exp': 1, 'resources': [['Strength gems', 1, 10], ['Magic gems', 1, 10],
                                                 ['Special gems', 1, 10]]}
        else:
            self.drop = drop

        self.updatestats()
        if skill is not None:
            self.skill = []
            for ski in skill:
                self.skill.append(Skill(*ski))
            if originalskill is None:
                self.originalskill = self.skill[0].copy
            else:
                self.originalskill = Skill(*originalskill)
        else:
            self.skill = [Skill('Tackle', 7, 2.8, 'Phys', False, False, False, False)]

            if originalskill is None:
                self.originalskill=Skill('Tackle', 7, 2.8, 'Phys', False, False, False, False)
            else:
                self.originalskill = Skill(*originalskill)

    def copy(self):
        return copy.deepcopy(self)

    def updatestats(self):
        for passive in self.passive:
            passive.percentage = (self.special / self.maxlvl)
            passive.quantity = passive.maxpower / 2 + (passive.maxpower / 2) * passive.percentage
        if self.name == self.parent.mainname:
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

def createshopitems(parent):
    Shopitem(parent=parent,name='Frog legs',elementlist=parent.buyablematerials,cost=50)
    Shopitem(parent=parent, name='Butterfly wings', elementlist=parent.buyablematerials, cost=50)
    Shopitem(parent=parent, name='Cow hide', elementlist=parent.buyablematerials, cost=50,unlockflags={'Mother':11})


def createmenu(parent):
    menuelement(parent=parent, name='Main', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Party', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Rank', isvisible=False, elementlist=parent.mainelements,
                unlockflags={'Talk with father 7/11': 1})
    menuelement(parent=parent, name='Training', isvisible=False, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Shop', isvisible=False, elementlist=parent.mainelements,
                unlockflags={'Enter the sleazy shop':2})
    menuelement(parent=parent, name='Story', isvisible=False, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Dungeon', isvisible=False, elementlist=parent.mainelements,
                unlockflags={'Talk with father 7/11': 1})
    menuelement(parent=parent, name='Settings', isvisible=True, elementlist=parent.mainelements)


def createmainsubmenu(parent):
    menuelement(parent=parent, name='Village', isvisible=True, elementlist=parent.mainsubelements)
    menuelement(parent=parent, name='Forest', elementlist=parent.mainsubelements,
                unlockflags={'Main': 2})
    menuelement(parent=parent, name='City', elementlist=parent.mainsubelements, unlockflags={'Main': 2})
    menuelement(parent=parent, name='Coast', elementlist=parent.mainsubelements,
                unlockflags={'Main': 2})
    menuelement(parent=parent, name='Jungle', elementlist=parent.mainsubelements,
                unlockflags={'Main': 2})
    menuelement(parent=parent, name='Astral plane', elementlist=parent.mainsubelements,
                unlockflags={'Main': 2})


def createpartytabs(parent):
    menuelement(parent=parent, name='Party selection', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Level up', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Bestiary', isvisible=True, elementlist=parent.partyelements,
                unlockflags={'Main': 0})
    menuelement(parent=parent, name='Skill', isvisible=True, elementlist=parent.partyelements, unlockflags={'Main': 0})
    menuelement(parent=parent, name='Dojo', isvisible=True, elementlist=parent.partyelements)#unlockflags={'Talk with zen master 4/4': 2}

def createsouls(parent):
    Information = getgamestate()
    parent.souls=Information['souls']


def createpokemon(parent):
    Information = getgamestate()
    pokemonlist.createpokemonlist(parent)
    parent.mainname=Information['mainname']
    for pokemonkey in Information['unlockablepokemons']:
        Pokemon(type=pokemonkey['type'],velocity=pokemonkey['velocity'],skill=pokemonkey['Skill'],originalskill=pokemonkey['Original skill'],parent=parent, wild=False, elementlist=parent.unlockablepokemons, hp=pokemonkey['hp'],name=pokemonkey['name'],atk=pokemonkey['atk'],
                dif=pokemonkey['dif'],satk=pokemonkey['satk'],sdif=pokemonkey['sdif'],maxlvl=pokemonkey['maxlvl'],unlocked=pokemonkey['unlocked'],lvl=pokemonkey['lvl'],phys=pokemonkey['phys'],
                magic=pokemonkey['magic'],special=pokemonkey['special'],drop=pokemonkey['drop'],num=pokemonkey['num'],passive=parent.pokemonlist[pokemonkey['num']-1].passive)
    for pokemonkey in Information['party']:
        Pokemon(type=pokemonkey['type'],velocity=pokemonkey['velocity'],skill=pokemonkey['Skill'],originalskill=pokemonkey['Original skill'],parent=parent, wild=False, elementlist=parent.party, hp=pokemonkey['hp'],name=pokemonkey['name'],atk=pokemonkey['atk'],
                dif=pokemonkey['dif'],satk=pokemonkey['satk'],sdif=pokemonkey['sdif'],maxlvl=pokemonkey['maxlvl'],unlocked=pokemonkey['unlocked'],lvl=pokemonkey['lvl'],phys=pokemonkey['phys'],
                magic=pokemonkey['magic'],special=pokemonkey['special'],drop=pokemonkey['drop'],num=pokemonkey['num'],passive=parent.pokemonlist[pokemonkey['num']-1].passive)
    for pokemonkey in Information['reserve']:

        Pokemon(type=pokemonkey['type'],velocity=pokemonkey['velocity'],skill=pokemonkey['Skill'], originalskill=pokemonkey['Original skill'], parent=parent, wild=False, elementlist=parent.reserve,
                hp=pokemonkey['hp'], name=pokemonkey['name'], atk=pokemonkey['atk'],
                dif=pokemonkey['dif'], satk=pokemonkey['satk'], sdif=pokemonkey['sdif'], maxlvl=pokemonkey['maxlvl'],
                unlocked=pokemonkey['unlocked'], lvl=pokemonkey['lvl'], phys=pokemonkey['phys'],
                magic=pokemonkey['magic'], special=pokemonkey['special'], drop=pokemonkey['drop'],
                num=pokemonkey['num'],passive=parent.pokemonlist[pokemonkey['num']-1].passive)

def createtemplates(parent):
    Information = getgamestate()
    for num,template in enumerate(Information['templates']):
        if template==[]:
            parent.templates.append([])
        else:
            late=[[],[]]
            for partypok in Information['templates'][num][0]:
                Pokemon(skill=partypok['Skill'], originalskill=partypok['Original skill'], parent=parent, wild=False, elementlist=late[0],
                        hp=partypok['hp'], name=partypok['name'], atk=partypok['atk'],
                        dif=partypok['dif'], satk=partypok['satk'], sdif=partypok['sdif'],
                        maxlvl=partypok['maxlvl'], unlocked=partypok['unlocked'], lvl=partypok['lvl'],
                        phys=partypok['phys'],
                        magic=partypok['magic'], special=partypok['special'], drop=partypok['drop'],
                        num=partypok['num'],passive=parent.pokemonlist[partypok['num']-1].passive)
            for reservepok in Information['templates'][num][1]:
                Pokemon(skill=reservepok['Skill'], originalskill=reservepok['Original skill'], parent=parent, wild=False, elementlist=late[1],
                        hp=reservepok['hp'], name=reservepok['name'], atk=reservepok['atk'],
                        dif=reservepok['dif'], satk=reservepok['satk'], sdif=reservepok['sdif'],
                        maxlvl=reservepok['maxlvl'], unlocked=reservepok['unlocked'], lvl=reservepok['lvl'],
                        phys=reservepok['phys'],
                        magic=reservepok['magic'], special=reservepok['special'], drop=reservepok['drop'],
                        num=reservepok['num'],passive=parent.pokemonlist[reservepok['num']-1].passive)
            parent.templates.append(late)


def createinstantactions(parent):
    Instantactions(parent=parent, name='Ponder the future', isvisible=True,
                   location='Common actions', cost=[['Energy', -1, 0, 0]],
                   complete=[['Fate', +1, 0, 0]])
    Instantactions(parent=parent, name='Cut wood', location='Woodcutting',
                   unlockflags={'Talk with father 2/11': 1}, cost=[['Endurance', -1, 0, 0]],
                   complete=[['Wood', 1, 0, 0]])
    Instantactions(parent=parent, name='"Eat" herbs', location='Garden activities',
                   unlockflags={'Talk with mother 8/10': 1}, cost=[['Herbs', -1, 0, 0]],
                   complete=[['Fate', 5, 0, 0]])


def createareainstant(parent):
    Instantactions(parent=parent, name='Look for weeds', isvisible=True, location='Village',
                   unlockflags={'Talk with mother 6/10': 1}, cost=[['Energy', -0.4, 0, 0]], area=True,
                   complete=[['Weeds', 1, 0, 0], ['Gold', 2, 0, 0]])


def createlongactions(parent):
    Longaction(parent=parent, name='Rest', isvisible=True,
               location='Common longactions', speed=1 / 600,
               progresseffect=[['Energy', 1 / 120, 0, 0]])
    Longaction(parent=parent, name='Parse through weeds', isvisible=True,
               location='Garden', speed=1 / 120, cost=[['Weeds', -5, 0, 0]],
               progresscost=[['Energy', -1 / 120, 0, 0]], complete=[['Herbs', 1, 0, 0]],
               unlockflags={'Talk with mother 6/10': 1})
    Longaction(parent=parent, name='Meditate', isvisible=True,
               location='Your room', speed=1 / 120,
               progresscost=[['Energy', -1 / 120, 0, 0]], complete=[['Fate', 1, 0, 0]],
               unlockflags={'Zen': 1})


def createarealongs(parent):
    Longaction(parent=parent, name='Exercise', isvisible=True,
               location='Village', speed=1 / 300, area=True,
               progresscost=[['Energy', -1 / 120, 0, 0]], progresseffect=[['Endurance', 1 / 120, 0, 0]],
               unlockflags={'Talk with father 2/11': 1})



def createquests(parent):
    questlines.createquests(parent)

    '''Quests(parent=parent, name='Wood quest2', isvisible=True,
                   location=['Village', 'old house'],
                   cost=[['Wood', -10, 0, 0]], complete=[['resource', 'Wood', 20, 0, 0]],
                   unlockflags={'Dubious home': 0, }, closingflags={'Dubious home': 2}, changeflags={'Dubious home': 1})
    Quests(parent=parent, name='Wood quest3', isvisible=True,
                   complete=[['stat', 'hp', 20, 0, 0], ['stat', 'patk', 1000, 0, 0], ['stat', 'pdef', 70, 0, 0],
                             ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 10, 0, 0]],
                   location=['Village', 'old house 2'],
                   unlockflags={'Dubious home': 0, }, closingflags={'Dubious home': 3}, changeflags={'Dubious home': 1})'''
def createskilllists(parent):
    Information = getgamestate()
    for skill in Information["availableskill"]:
        parent.availableskills.append(Skill(*skill))
    for skill in Information["learnableskills"]:
        parent.learnableskills.append([Skill(*skill[0]),skill[1]])

def createproceedactions(parent):
    Nextaction(parent=parent,name='Unlock the world',location='Village',unlockflags={'Main': 1}, closingflags={'Main':2}, changeflags={'Main': 1},cost=[['Fate', -10, 0, 0]])

def createcorestats(parent):
    Information = getgamestate()
    parent.corestats = Corestats(parent)
    parent.corestats.basestats = Information['corestats']['basestats']
    parent.corestats.modifiers = Information['corestats']['modifiers']
    parent.corestats.baseexp = Information['corestats']['baseexp']
    parent.corestats.rank = Information['corestats']['rank']
    parent.corestats.improvedactions = Information['corestats']['improvedactions']
    parent.corestats.exprequiredtorank = Information['corestats']['exprequiredtorank']
    parent.corestats.expdropbonus = Information['corestats']['expdropbonus']

def loadflags(parent):
    Information = getgamestate()
    for flag in Information['flags']:
        parent.flags[flag] = Information['flags'][flag]
    parent.cleareddungeons=Information['cleareddungeons']
    parent.storylog=Information["storylog"]


def createresources(parent):
    Information = getgamestate()
    for resourcename in Information['resources']:
        if resourcename not in ['Fate', 'Strength gems', 'Magic gems', 'Special gems']:
            Resource(parent, resourcename, *Information['resources'][resourcename], resources=parent.resources)
    parent.fate = Resource(parent, 'Fate', *Information['resources']['Fate'], 0, resources=parent.resources)
    parent.physgems = Resource(parent, 'Strength gems', *Information['resources']['Strength gems'],
                               resources=parent.resources)
    parent.magicgems = Resource(parent, 'Magic gems', *Information['resources']['Magic gems'],
                                resources=parent.resources)
    parent.specialgems = Resource(parent, 'Special gems', *Information['resources']['Special gems'],
                                  resources=parent.resources)




def createenergies(parent):
    Energy(parent=parent, name='Energy', quantity=5, max=5, unlockflags={'Enter your home': 0}, color=red, regen=0)
    Energy(parent=parent, name='Endurance', quantity=0, max=1, unlockflags={'Talk with father 2/11': 1}, color=(255, 255, 0),
           regen=0)
    Energy(parent=parent, name='Mana', quantity=0, max=1, unlockflags={'Talk with father 7/11': 14}, color=(0, 0, 205),
           isvisible=False,
           regen=1 / 120)
    Energy(parent=parent, name='Fire', quantity=0, max=1, unlockflags={'Talk with father 7/11': 14}, color=orange, isvisible=False,
           regen=1 / 120)
    Energy(parent=parent, name='Wind', quantity=0, max=1, unlockflags={'Talk with father 7/11': 14}, color=teal, isvisible=False,
           regen=1 / 120)
    Energy(parent=parent, name='Earth', quantity=0, max=1, unlockflags={'Talk with father 7/11': 14}, color=brown, isvisible=False,
           regen=1 / 120)


def createdungeons(parent):
    Dungeon(parent=parent, name="Field", location=['Village', 'Surroundings'], changeflags={'Talk with Francesco 1/3': 1},
            unlockflags={'Talk with mother 10/10': 2}, closingflags={}, usualreward=[['resource', 'Special gems', 1, 0, 0]],
            firsttime=[['maxlvl', 7]],
            monsterlist=[parent.pokemonlist[i].copy() for i in range(3, 6)])
    Dungeon(parent=parent, name="Garden", location=['Village', 'Home'], changeflags={'Talk with mother 1/10': 1},
            unlockflags={'Talk with father 11/11': 2}, closingflags={}, usualreward=[['resource', 'Magic gems', 1, 0, 0]],
            firsttime=[['maxlvl', 6]],
            monsterlist=[parent.pokemonlist[i].copy() for i in range(1, 4)])
    Dungeon(parent=parent, name="Training hall", location=['Village', 'Home'], changeflags={'Main': 1},
            unlockflags={'Talk with father 7/11': 1}, closingflags={}, usualreward=[['resource', 'Physical gems', 1, 0, 0]],
            firsttime=[['maxlvl', 5],['resource', 'Strength gems', 1, 0, 0],['resource', 'Magic gems', 1, 0, 0],['resource', 'Special gems', 1, 0, 0]],
            monsterlist=[], boss=parent.pokemonlist[0].copy())
    Dungeon(parent=parent, name="Brother fight", location=['Village', 'Surroundings'], changeflags={},
            unlockflags={'Talk with Francesco 3/3': 2}, closingflags={}, firsttime=[['maxlvl', 10]],
            monsterlist=[], boss=parent.pokemonlist[6].copy())
    for location1 in parent.dungeons:
        for location2 in parent.dungeons[location1]:
            for dung in parent.dungeons[location1][location2]:
                if dung.name in parent.cleareddungeons:
                    dung.cleared= True
