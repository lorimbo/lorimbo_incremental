import json


class Corestats:
    def __init__(self):
        self.basestats = {'hp': 10, 'patk': 10, 'pdef': 10, 'matk': 10, 'mdef': 10}
        self.element = []
        # 0 for adding 1 for multiplication
        self.modifiers = {'Upgradeactions': {'type': 'add', 'hp': 1, 'patk': 0, 'pdef': 0, 'matk': 0, 'mdef': 0}}

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
    def __init__(self, parent, name, quantity, max, unlockflags, regen=0, effect=None,isvisible=True):
        self.parent = parent
        self.name = name
        self.quantity = quantity
        self.max = max
        self.unlockflags = unlockflags
        self.regen = regen
        self.effect = effect
        self.isvisible = isvisible
        parent.energies.append(self)


class Resource:
    def __init__(self, parent, name, quantity, max, unlockflags, category, regen=0, effect=None, resources=None,
                 isvisible=True):
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


class Upgradeactions(menuelement):
    def __init__(self, cost=[['Wood', 0, 0, 0]],
                 complete=[['Wood', 0, 0, 0]], requirements=[['Wood', 0, 0, 0]], *args, **kwargs):
        menuelement.__init__(self, *args, **kwargs)
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
                if costname in self.parent.energies.keys():
                    if self.parent.energies[costname]['current'] >= -i[1]:
                        self.parent.energies[costname]['current'] += i[1]
                        self.docomplete()
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        if resource.quantity > -i[1]:
                            resource.quantity += i[1]
                            self.docomplete()
        self.parent.upgradeaction = None

    def docomplete(self):
        for i in self.complete:
            completename = i[0]
            if completename in self.parent.energies.keys():
                if self.parent.energies[completename]['max'] - self.parent.energies[completename]['current'] > -i[1]:
                    self.parent.energies[completename]['current'] += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == completename]:
                    resource.quantity += i[1]
                    if resource.quantity > resource.max:
                        resource.quantity = resource.max
            if self.changeflags is not None:
                for key in self.changeflags:
                    self.parent.flags[key] += self.changeflags[key]

    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            if costname in self.parent.energies.keys():
                i[2] = round(self.parent.energies[costname]['current'], 2)
                i[3] = self.parent.energies[costname]['max']
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
            costname = i[0]
            if costname in self.parent.energies.keys():
                i[2] = self.parent.energies[costname]['current']
                i[3] = self.parent.energies[costname]['max']
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    continue

        for i in self.requirements:
            costname = i[0]
            if costname in self.parent.energies.keys():
                i[2] = self.parent.energies[costname]['current']
                i[3] = self.parent.energies[costname]['max']
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


class Instantactions(menuelement):
    def __init__(self,
                 cost=[['Wood', 0, 0, 0]],
                 complete=[['Wood', 0, 0, 0]], *args, **kwargs):
        menuelement.__init__(self, *args, **kwargs)
        self.cost = cost
        self.complete = complete
        self.resourcetype = []
        self.update()

    def docost(self):
        temp = 0
        for i in self.cost:
            costname = i[0]
            if costname in self.parent.energies.keys():
                if self.parent.energies[costname]['current'] < -i[1]:
                    temp = 1
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity <= -i[1]:
                        temp = 1
        if not temp:
            for i in self.cost:
                costname = i[0]
                if costname in self.parent.energies.keys():
                    self.parent.energies[costname]['current'] += i[1]
                    continue
                for x in self.parent.resources.keys():
                    for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                        resource.quantity += i[1]
            self.docomplete()
        self.parent.action = None

    def docomplete(self):
        for i in self.complete:
            completename = i[0]
            if completename in self.parent.energies.keys():
                if self.parent.energies[completename]['max'] - self.parent.energies[completename]['current'] > -i[1]:
                    self.parent.energies[completename]['current'] += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == completename]:
                    resource.quantity += i[1]
                    if resource.quantity > resource.max:
                        resource.quantity = resource.max

    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            if costname in self.parent.energies.keys():
                i[2] = round(self.parent.energies[costname]['current'], 2)
                i[3] = self.parent.energies[costname]['max']
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
            if costname in self.parent.energies.keys():
                i[2] = self.parent.energies[costname]['current']
                i[3] = self.parent.energies[costname]['max']
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
    def __init__(self, progress=0, speed=1 / 1200, isactive=False,
                 cost=[['Wood', 0, 0, 0]], progresscost=[['Wood', 0, 0, 0]],
                 progresseffect=[['Wood', 0, 0, 0]], complete=[['Wood', 0, 0, 0]], *args, **kwargs):
        menuelement.__init__(self, *args, **kwargs)
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
            if costname in self.parent.energies.keys():
                i[2] = round(self.parent.energies[costname]['current'], 2)
                i[3] = self.parent.energies[costname]['max']
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
            if costname in self.parent.energies.keys():
                i[2] = round(self.parent.energies[costname]['current'], 2)
                i[3] = self.parent.energies[costname]['max']
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    continue
        for i in self.progresseffect:
            costname = i[0]
            if costname in self.parent.energies.keys():
                i[2] = round(self.parent.energies[costname]['current'], 2)
                i[3] = self.parent.energies[costname]['max']
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    i[2] = resource.quantity
                    i[3] = resource.max
                    continue
        temp = 1
        for i in self.complete:
            costname = i[0]
            if costname in self.parent.energies.keys():
                i[2] = self.parent.energies[costname]['current']
                i[3] = self.parent.energies[costname]['max']
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
        for i in self.cost:
            costname = i[0]
            if costname in self.parent.energies.keys():
                if self.parent.energies[costname]['current'] >= -i[1]:
                    self.parent.energies[costname]['current'] += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]:
                        resource.quantity += i[1]

    def dopassiveeffect(self):
        for i in self.progresseffect:
            costname = i[0]
            if costname in self.parent.energies.keys():
                if self.parent.energies[costname]['current'] >= -i[1] and self.parent.energies[costname]['current'] + i[
                    1] < self.parent.energies[costname]['max']:
                    self.parent.energies[costname]['current'] += i[1]
                elif costname == 'Action':
                    for key in self.parent.loopactions:
                        for e in self.parent.loopactions[key]:
                            if e.previouslyactive:
                                e.activation()
                                e.previouslyactive = False

                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1] and resource.quantity + i[1] < resource.max:
                        self.parent.resources[x][costname]['quantity'] += i[1]

    def dopassiveaction(self):
        for i in self.progresscost:
            costname = i[0]
            if costname in self.parent.energies.keys():
                if self.parent.energies[costname]['current'] >= -i[1]:
                    self.parent.energies[costname]['current'] += i[1]
                    self.dopassiveeffect()
                elif costname == 'Action':
                    self.previouslyactive = True
                    self.parent.loopactions['Common loopactions'][0].activation()
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]:
                        resource.quantity += i[1]

                        self.dopassiveeffect()

    def dofinishaction(self):
        for i in self.complete:
            costname = i[0]
            if costname in self.parent.energies.keys():
                if self.parent.energies[costname]['current'] >= -i[1]:
                    self.parent.energies[costname]['current'] += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]:
                        resource.quantity += i[1]


class Pokemon(menuelement):
    def __init__(self, hp, atk, dif, satk, sdif, maxlvl=1000, unlocked=0, lvl=0, phys=0, magic=0,
                 special=0,
                 skill=0, *args, **kwargs):
        menuelement.__init__(self, *args, **kwargs)
        self.atk = atk
        self.dif = dif
        self.satk = satk
        self.sdif = sdif
        self.currenthp = hp
        self.hp = hp
        self.lvl = lvl
        self.unlocked = unlocked
        self.maxlvl = maxlvl
        self.phys = phys
        self.magic = magic
        self.special = special
        # self.skill=Skill('Tackle','phys',10,2)
        self.timer = 0
    # def useskill(self,enemy):
    # self.skill.useskill(self,enemy)
    # self.timer=0
    # def checkcooldown(self):
    # self.timer+=1
    # return self.timer>self.skill.cooldown


def getgamestate():
    f = open("gamestate.json")
    Information = json.load(f)
    return Information


def createinstantactions(parent):
    Instantactions(parent=parent, name='Get motivated', isvisible=True,
                   elementlist=parent.instantactions['Common actions'], cost=[['Action', -1, 0, 0]],
                   complete=[['Destiny', +1, 0, 0]])
    Instantactions(parent=parent, name='Test1', isvisible=True, elementlist=parent.instantactions['Common actions'],
                   unlockflags={'Dubious home': 1}, cost=[['Action', -1, 0, 0], ['Wood', -1, 0, 0]],
                   complete=[['Destiny', +1, 0, 0], ['Wood', 10, 0, 0]])
    Instantactions(parent=parent, name='Test2', isvisible=True, elementlist=parent.instantactions['Common actions'])
    Instantactions(parent=parent, name='Test3', isvisible=True, elementlist=parent.instantactions['Common actions 2'])
    Instantactions(parent=parent, name='Test4', isvisible=True, elementlist=parent.instantactions['Common actions 2'])


def createmenu(parent):
    menuelement(parent=parent, name='Main', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Party', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Ritual', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Routine', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Story', isvisible=True, elementlist=parent.mainelements)
    menuelement(parent=parent, name='Dungeon', isvisible=True, elementlist=parent.mainelements)


def createmainsubmenu(parent):
    menuelement(parent=parent, name='Village', isvisible=True, elementlist=parent.mainsubelements)
    menuelement(parent=parent, name='Forest', isvisible=True, elementlist=parent.mainsubelements)
    menuelement(parent=parent, name='City', isvisible=True, elementlist=parent.mainsubelements, unlockflags={'Main': 1})
    menuelement(parent=parent, name='Coast', isvisible=True, elementlist=parent.mainsubelements)
    menuelement(parent=parent, name='Jungle', isvisible=True, elementlist=parent.mainsubelements)
    menuelement(parent=parent, name='Astral plane', isvisible=True, elementlist=parent.mainsubelements)


def createpartytabs(parent):
    menuelement(parent=parent, name='Main', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Level up', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Quest', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='Bestiary', isvisible=True, elementlist=parent.partyelements)
    menuelement(parent=parent, name='SKill', isvisible=True, elementlist=parent.partyelements)


def createloopactions(parent):
    Information = getgamestate()
    loopactionvisibility = Information['loopactionvisibility']
    Loopaction(parent=parent, name='Rest', isvisible=loopactionvisibility[0],
               elementlist=parent.loopactions['Common loopactions'], speed=1 / 1200,
               progresseffect=[['Action', 1 / 240, 0, 0]])
    Loopaction(parent=parent, name='Exercise', isvisible=loopactionvisibility[1],
               elementlist=parent.loopactions['Common loopactions 2'], speed=1 / 600,
               progresscost=[['Action', -1 / 240, 0, 0]], progresseffect=[['Stamina', 1 / 240, 0, 0]])


def createpokemon(parent):
    Information = getgamestate()
    for pokemonkey in Information['basepokemons']:
        Pokemon(parent=parent, elementlist=parent.pokemonlist, **pokemonkey)
    for pokemonkey in Information['party']:
        Pokemon(parent=parent, elementlist=parent.party, **pokemonkey)
    for pokemonkey in Information['reserve']:
        Pokemon(parent=parent, elementlist=parent.reserve, **pokemonkey)


def createupgradeactions(parent):
    Upgradeactions(parent=parent, name='Wood quest', isvisible=True,
                   elementlist=parent.upgradeactions['Village']['old house'],
                   unlockflags={'Dubious home': 0, }, closingflags={'Dubious home': 1}, changeflags={'Dubious home': 1},
                   cost=[['Wood', -10, 0, 0]], complete=[['Wood', 20, 0, 0]], requirements=[['Destiny', 5, 0, 0]])
    Upgradeactions(parent=parent, name='Wood quest2', isvisible=True,
                   elementlist=parent.upgradeactions['Village']['old house'],
                   cost=[['Wood', -10, 0, 0]], complete=[['Wood', 20, 0, 0]],
                   unlockflags={'Dubious home': 1, }, closingflags={'Dubious home': 2}, changeflags={'Dubious home': 1})
    Upgradeactions(parent=parent, name='Wood quest3', isvisible=True,
                   elementlist=parent.upgradeactions['Village']['old house 2'],
                   unlockflags={'Dubious home': 2, }, closingflags={'Dubious home': 3}, changeflags={'Dubious home': 1})


def createresources(parent):
    Resource(parent, 'Destiny', 0, 100, {'Dubious home': 0}, 'Destiny', 0, resources=parent.resources)
    Resource(parent, 'Wood', 50, 100, {'Dubious home': 1}, 'Wood', 0, resources=parent.resources)
    Resource(parent, 'Wooden statue', 0, 100, {'Dubious home': 2}, 'Accessories', 0, resources=parent.resources)
    Resource(parent, 'Stone', 0, 100, {'Dubious home': 0}, 'Minerals', 0, resources=parent.resources)
    Resource(parent, 'Firewood', 0, 100, {'Dubious home': 0}, 'Wood', 0, resources=parent.resources)
    Resource(parent, 'Pelt', 0, 100, {'Dubious home': 0}, 'Materials', 0, resources=parent.resources)
