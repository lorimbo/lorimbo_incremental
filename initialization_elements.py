import json

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
    if n > 10000000:
        return f'{round(n / 1000000, 1)}M'
    elif n > 1000000:
        return f'{round(n / 1000000, 2)}M'
    elif n > 100000:
        return f'{round(n / 1000, 0)}K'
    elif n > 10000:
        return f'{round(n / 1000, 1)}K'
    elif n > 1000:
        return f'{round(n / 1000, 2)}K'
    return str(round(n, 1))


class Corestats:
    def __init__(self,parent):
        self.parent=parent
        self.basestats = {'hp': 10, 'patk': 10, 'pdef': 10, 'matk': 10, 'mdef': 10}
        self.modifiers = {'Upgradeactions': {'type': 'add', 'hp': 1, 'patk': 0, 'pdef': 0, 'matk': 0, 'mdef': 0}}
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
                 complete=[['resource', 'Wood', 0, 0, 0]], requirements=[['Wood', 0, 0, 0]], *args, **kwargs):
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
                for energy in [e for e in self.parent.energies if e.name == costname]:
                    if energy.current >= -i[1]:
                        energy.current += i[1]
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
                self.parent.corestats.modifiers['Upgradeactions'][name] += i[2]
                self.parent.corestats.updatepokemons()

            if self.changeflags is not None:
                for key in self.changeflags:
                    self.parent.flags[key] += self.changeflags[key]

    def update(self):
        self.isdisabled = False
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                i[2] = round(energy.current, 2)
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
                i[2] = energy.current
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
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity < -i[1]:
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
                i[2] = energy.current
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
        for i in self.cost:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1]:
                    energy.quantity += i[1]
                continue
            for x in self.parent.resources.keys():
                for resource in [e for e in self.parent.resources[x] if e.name == costname]:
                    if resource.quantity > -i[1]:
                        resource.quantity += i[1]

    def dopassiveeffect(self):
        for i in self.progresseffect:
            costname = i[0]
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1] and energy.quantity + i[
                    1] < energy.max:
                    energy.quantity += i[1]
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
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1]:
                    energy.quantity += i[1]
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
            for energy in [e for e in self.parent.energies if e.name == costname]:
                if energy.quantity >= -i[1]:
                    energy.quantity += i[1]
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
        self.updatestats()

    def updatestats(self):
        if self.name == 'You':
            if self.lvl<=10:
                scaling1=1/10+self.phys*9/100
                scaling2=1/10+self.magic*9/100
            else:
                scaling1=1+self.lvl*8/100
                scaling2 = 1 + self.magic * 8 / 100

            self.actualhp = scaling1 * self.parent.corestats.finalstats()['hp']
            self.actualpatk = scaling1 * self.parent.corestats.finalstats()['patk']
            self.actualpdef = scaling1 * self.parent.corestats.finalstats()['pdef']
            self.actualmatk = scaling2 * self.parent.corestats.finalstats()['matk']
            self.actualmdef = scaling2 * self.parent.corestats.finalstats()['mdef']





        else:
            self.actualhp = round(
                self.parent.corestats.finalstats()['hp'] * (self.phys + 1 / self.maxlvl) * (self.hp / 100), 1)
            self.actualpatk = round(
                self.parent.corestats.finalstats()['patk'] * (self.phys + 1 / self.maxlvl) * (self.patk / 100), 1)
            self.actualpdef = round(
                self.parent.corestats.finalstats()['pdef'] * (self.phys + 1 / self.maxlvl) * (self.pdef / 100), 1)
            self.actualmatk = round(
                self.parent.corestats.finalstats()['matk'] * (self.magic + 1 / self.maxlvl) * (self.matk / 100), 1)
            self.actualmdef = round(
                self.parent.corestats.finalstats()['mdef'] * (self.magic + 1 / self.maxlvl) * (self.mdef / 100), 1)

            self.currenthp = self.actualhp


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
                   cost=[['Wood', -10, 0, 0]], complete=[['max', 'Wood', 20, 0, 0]],
                   requirements=[['Destiny', 5, 0, 0]])
    Upgradeactions(parent=parent, name='Wood quest2', isvisible=True,
                   elementlist=parent.upgradeactions['Village']['old house'],
                   cost=[['Wood', -10, 0, 0]], complete=[['resource', 'Wood', 20, 0, 0]],
                   unlockflags={'Dubious home': 1, }, closingflags={'Dubious home': 2}, changeflags={'Dubious home': 1})
    Upgradeactions(parent=parent, name='Wood quest3', isvisible=True,
                   complete=[['stat', 'hp', 20, 0, 0], ['stat', 'patk', 1000, 0, 0], ['stat', 'pdef', 70, 0, 0],
                             ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 10, 0, 0]],
                   elementlist=parent.upgradeactions['Village']['old house 2'],
                   unlockflags={'Dubious home': 2, }, closingflags={'Dubious home': 3}, changeflags={'Dubious home': 1})


def createresources(parent):
    parent.destiny=Resource(parent, 'Destiny', 0, 100, {'Dubious home': 0}, 'Destiny', 0, resources=parent.resources)
    Resource(parent, 'Wood', 50, 10000000, {'Dubious home': 1}, 'Wood', 0, resources=parent.resources)
    Resource(parent, 'Wooden statue', 0, 100, {'Dubious home': 2}, 'Accessories', 0, resources=parent.resources)
    Resource(parent, 'Stone', 0, 100, {'Dubious home': 0}, 'Minerals', 0, resources=parent.resources)
    Resource(parent, 'Firewood', 0, 100, {'Dubious home': 0}, 'Wood', 0, resources=parent.resources)
    Resource(parent, 'Pelt', 0, 100, {'Dubious home': 0}, 'Materials', 0, resources=parent.resources)
    parent.physseeds=Resource(parent, 'Physical seeds', 10, 10000, {'Dubious home': 0}, 'Seeds', 0, resources=parent.resources)
    parent.magicseeds=Resource(parent, 'Magical seeds', 100, 10000, {'Dubious home': 0}, 'Seeds', 0, resources=parent.resources)
    parent.specialseeds=Resource(parent, 'Special seeds', 100, 10000, {'Dubious home': 0}, 'Seeds', 0, resources=parent.resources)


def createenergies(parent):
    Energy(parent=parent, name='Action', quantity=0, max=5, unlockflags={'Dubious home': 0}, color=red, regen=0)
    Energy(parent=parent, name='Stamina', quantity=0, max=1, unlockflags={'Dubious home': 0}, color=green,
           regen=0)
    Energy(parent=parent, name='Mana', quantity=0, max=1, unlockflags={'Dubious home': 0}, color=blue,
           regen=1 / 240)
    Energy(parent=parent, name='Fire', quantity=0, max=1, unlockflags={'Dubious home': 0}, color=orange,
           regen=1 / 240)
