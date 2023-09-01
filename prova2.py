import pygame
from random import randint

pygame.init()

# color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 100, 0)
grey = (105, 105, 105)
teal = (173, 216, 230)
brown = (139, 69, 19)

# impostazioni schermo
screen = pygame.display.set_mode([1500, 900])
pygame.display.set_caption('Prova')
background = black
framerate = 60
font = pygame.font.Font('freesansbold.ttf', 15)
font2 = pygame.font.Font('freesansbold.ttf',11)
timer = pygame.time.Clock()

# variabili grafiche
tab = 0
subtab = 0
delay = 0
upgradeactions = {}
dungeonactions={}
currentdungeon=None



# loops
loopactions = {}
loopactions['rest'] = {'isvisible': 1, 'buttonpos': None, 'time': 6}
loopactions['recoverstamina'] = {'isvisible': 1, 'buttonpos': None, 'time': 7}
loopactions['pray'] = {'isvisible': 1, 'buttonpos': None, 'time': 2,'improvement':1}
currentloopaction = 0
previousloopaction = 0
looptimer = 0
previoustab = 0
previoussubtab = 0

# progression
woodquest = 0
story_progression = 3
dungeonprogress=0.1

# risorse
squaremenu = {}
redsquaremenu = {}
destiny = 60
destinymax = 100
energies = {'Action': {'max': 5, 'current': 0, 'regen': 0 / 60, 'color': red},
            'Stamina': {'max': 1, 'current': 0, 'regen': 0 / 60, 'color': green},
            'Water': {'max': 1, 'current': 0, 'regen': 1 / 60, 'color': blue},
            'Fire': {'max': 1, 'current': 0, 'regen': 1 / 60, 'color': orange},
            'Wind': {'max': 1, 'current': 0, 'regen': 1 / 60, 'color': teal},
            'Earth': {'max': 1, 'current': 0, 'regen': 1 / 60, 'color': brown}}

everyitem = {'pizza': 0, 'pasta': 0, 'wood': 0, 'hairclip': 0, 'firewood': 0, 'gold': 400}
everyitemmax = {'pizza': 10, 'pasta': 20, 'wood': 20, 'hairclip': 20, 'firewood': 80, 'gold': 400}
unlocked_resources = {'inspiration': [], 'etc': ['gold'], 'accessories': [], 'plants': [], 'wood': [],
                      'materials': [], 'seeds': [], 'food': [], 'cuisine': []}
resourcetypes = {'inspiration': 1, 'etc': 1, 'accessories': 1, 'plants': 1, 'wood': 1, 'materials': 1,
                 'seeds': 1, 'food': 1, 'cuisine': 1}
prayimprovement = 1
maxlengthparty=7


# class definition
class Dungeon:
    def __init__(self,name,pokemonlist):
        self.name=name
        self.pokemonlist=pokemonlist
        self.Generatedpokemon=[]
    def spawnpokemon(self):
        Enemyparty=[]
        i=randint(3,5)
        for l in range(i):
            a=randint(0,len(self.pokemonlist)-1)
            Enemyparty.append(self.pokemonlist[a])
        self.Generatedpokemon=Enemyparty
        return self.Generatedpokemon
    def containspokemon(self):
        return len(self.Generatedpokemon)



class Skill:
    def __init__(self,name,skilltype,power,cooldown):
        self.name = name
        self.power = power
        self.type = skilltype
        self.cooldown=cooldown
    def useskill(self,pokemon,enemy):
        enemy.hp -= pokemon.atk+self.power


class Pokemon:
    def __init__(self,pokemontype, hp, atk, dif, satk, sdif, unlocked=0,maxlvl=1000,lvl=0,phys=0,magic=0,special=0,skill=0):
        self.atk = atk
        self.dif = dif
        self.satk = satk
        self.sdif = sdif
        self.currenthp = hp
        self.hp = hp
        self.unlocked = unlocked
        self.type = pokemontype
        self.lvl = lvl
        self.maxlvl = maxlvl
        self.phys = phys
        self.magic = magic
        self.special = special
        self.buttonup = None
        self.buttondown = None
        self.remove= None
        self.add=None
        self.summon=None
        self.physbutt=None
        self.magicbutt=None
        self.specialbutton=None
        self.skill=Skill('Tackle','phys',10,2)
        self.timer=0
    def useskill(self,enemy):
        self.skill.useskill(self,enemy)
        self.timer=0
    def checkcooldown(self):
        self.timer+=1
        return self.timer>self.skill.cooldown

#pokemon data
AllPokemons = [ Pokemon('You',5, 1, 1, 1, 1, 2),
                Pokemon('Robot',5,2,1,2,1),
                Pokemon('Scarlett Dragon',10,2,2,2,2,2),
                Pokemon('Scarlett Dragon2',10,2,2,2,2,2),
                Pokemon('Scarlett Dragon3',10,2,2,2,2,2),
                Pokemon('Scarlett Dragon4',10,2,2,2,2,2),
                Pokemon('Scarlett Dragon5',10,2,2,2,2,2),
                Pokemon('Scarlett Dragon6',10,2,2,2,2,2),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon7',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon8',10,2,2,2,2,1),
                Pokemon('Scarlett Dragon9',10,2,2,2,2,1)]
Alldungeons={"coco's lair":Dungeon("coco's lair",AllPokemons[1:])}
Reserve=[pokemon for pokemon in AllPokemons if pokemon.unlocked == 1]
Party = [pokemon for pokemon in AllPokemons if pokemon.unlocked == 2]
Leveluppable=[e for e in AllPokemons if e.unlocked]
startvisiblelist=0
startvisiblelist2=0
startvisiblelistlevelup=0


if len(Leveluppable)>15:
    endvisiblelistlevelup=15
else:
    endvisiblelistlevelup=len(Leveluppable)

if len(Party)>5:
    endvisiblelist=5
else:
    endvisiblelist=len(Party)
if len(Reserve)>10:
    endvisiblelist2=10
else:
    endvisiblelist2=len(Reserve)




# auxiliary functions
def loopeffect(name):
    global currentloopaction
    global previousloopaction
    global looptimer
    global prayimprovement
    if name == 'rest':
        energies['Action']['regen'] = 1 / 60
        energies['Stamina']['regen'] = 0
        if previousloopaction != 0 and (abs(energies['Action']['current'] - energies['Action']['max'])) < 1 / 10:
            currentloopaction = previousloopaction
            previousloopaction = 0
            looptimer = 1
    elif name == 'recoverstamina':
        if energies['Action']['current'] > 1 / 120:
            energies['Action']['current'] -= 1 / 120
            energies['Stamina']['regen'] = 1 / 120
        else:
            currentloopaction = 'rest'
            previousloopaction = 'recoverstamina'

            looptimer = 1
        energies['Action']['regen'] = 0
    elif name == 'pray':
        if energies['Action']['current'] > 1 / 120:
            energies['Action']['current'] -= 1 / 120
        else:
            currentloopaction = 'rest'
            previousloopaction = 'pray'

            looptimer = 1
        energies['Action']['regen'] = 0
        energies['Stamina']['regen'] = 0

    else:
        energies['Action']['regen'] = 0


def loopfinish(name):
    global destiny
    if name == 'pray':
        if destiny < destinymax:
            destiny += loopactions['prey']['improvement']
    if name == 'rest':
        print('ok')


def regen():
    for key in energies:
        if energies[key]['current'] < energies[key]['max']:
            energies[key]['current'] += energies[key]['regen']


def draw_energy():
    resources_text = font.render('Energies', True, black)
    screen.blit(resources_text, (1400, 45))
    for keynumber, key in enumerate(energies):
        if energies[key]['max']:
            pygame.draw.rect(screen, energies[key]['color'],
                             [1380, 60 + keynumber * 20, energies[key]['current'] / energies[key]['max'] * 110, 20])
        action_text = font.render(key, True, black)
        screen.blit(action_text, (1385, 65 + 20 * keynumber))
        action_text2 = font.render(str(round(energies[key]['current'], 1)) + '/' + str(round(energies[key]['max'], 1)),
                                   True, black)
        screen.blit(action_text2, (1450, 65 + 20 * keynumber))


def pastetext(text,positionx,positiony,antialias=True,color=black):
    testo = font.render(text,antialias, color)
    screen.blit(testo,(positionx,positiony))
def createaPokemontext(text,number,positionx,position):
    positiony=255+number*35+position
    pastetext(str(text),positionx,positiony,True,black)
def createaPokemon(screen,pokemon,number,position):
    pygame.draw.rect(screen, black, [135, 245 + number * 35+position, 150, 40])
    pygame.draw.rect(screen, white, [140, 250 + number * 35+position, 140, 30])
    if pokemon.unlocked == 2:
        pokemon.switchup = pygame.draw.rect(screen, white, [510, 250 + number * 35+position, 30, 30])
        pokemon.switchdown = pygame.draw.rect(screen, white, [550, 250 + number * 35+position, 30, 30])
        pygame.draw.polygon(screen, green, ((555,255 + number * 35+position),(575,255 + number * 35+position) , (565,275 + number * 35+position)))
        pygame.draw.polygon(screen, green, ((515, 275 + number * 35 + position), (535, 275 + number * 35 + position), (525, 255 + number * 35 + position)))
        if len(Party)!=1:
            pokemon.remove = pygame.draw.rect(screen,white,[600,250+number*35+position,60,30])
        else:
            pokemon.remove = pygame.draw.rect(screen, red, [600, 250 + number * 35 + position, 60, 30])
        pastetext('Remove', 600, 255 + 35 * number + position)
    elif pokemon.unlocked == 1:
        if len(Party)<maxlengthparty:
            pokemon.add = pygame.draw.rect(screen,white,[600,250+number*35+position,60,30])
        else:
            pokemon.add = pygame.draw.rect(screen, red, [600, 250 + number * 35 + position, 60, 30])
        pastetext('Add',600,255+35*number+position)
    createaPokemontext(pokemon.type,number,145,position)
    createaPokemontext(pokemon.hp, number,350, position)
    createaPokemontext(pokemon.atk, number,380, position)
    createaPokemontext(pokemon.dif, number,410, position)
    createaPokemontext(pokemon.satk, number,440, position)
    createaPokemontext(pokemon.sdif, number,470, position)
    isjo=font2.render(str(pokemon.lvl)+'/'+str(pokemon.maxlvl),True,black)
    screen.blit(isjo, (290,255+ number * 35 + position))
def draw_resources():
    pygame.draw.rect(screen, black, [1379, 199, 112, 24])
    pygame.draw.rect(screen, white, [1380, 200, 110, 22])
    destinynumber = font2.render(str(destiny) + '/' + str(destinymax), True, grey)
    screen.blit(destinynumber, (1450, 205))
    destinywriting = font2.render('Destiny', True, grey)
    screen.blit(destinywriting, (1382, 205))

    j3 = 0
    for j1, j2 in enumerate(resourcetypes):
        typeofres = font.render(j2, True, black)
        screen.blit(typeofres, (1380, 200 + 22 * (j1 + 1 + j3)))
        if resourcetypes[j2]:
            closesquare = pygame.draw.rect(screen, red, [1350, 199 + 22 * (j1 + 1 + j3), 20, 20])
            redsquaremenu[j2] = closesquare
            for k in unlocked_resources[j2]:
                itemname2 = font2.render(str(k), True, grey)
                j3 += 1
                pygame.draw.rect(screen, black, [1379, 199 + 22 * (j1 + 1 + j3), 112, 24])
                pygame.draw.rect(screen, white, [1380, 200 + 22 * (j1 + 1 + j3), 110, 22])
                screen.blit(itemname2, (1384, 205 + 22 * (j1 + 1 + j3)))
                itemquantity = font2.render(str(everyitem[k]) + '/' + str(everyitemmax[k]), True, grey)
                screen.blit(itemquantity, (1450, 205 + 22 * (j1 + 1 + j3)))
        else:
            opensquare = pygame.draw.rect(screen, grey, [1350, 199 + 22 * (j1 + 1 + j3), 20, 20])
            squaremenu[j2] = opensquare




# main loop
running = True
while running:
    timer.tick(framerate)
    screen.fill(white)
    if delay > 0:
        delay -= 1
    if currentloopaction != 0:
        if looptimer < loopactions[currentloopaction]['time']*60:
            looptimer += 1
        else:
            looptimer = 0
            loopfinish(currentloopaction)
    loopeffect(currentloopaction)
    instantactions = {}
    dungeonactions = {}

    regen()
    # energy graphics
    draw_energy()

    # resources graphics
    draw_resources()

    # grafica delle tab principali a sinistra
    tab_background = pygame.draw.rect(screen, black, [5, 45, 110, 215])
    tab0_button = pygame.draw.rect(screen, grey, [10, 50, 100, 30])
    tab0_text = font.render('Main', True, black)
    screen.blit(tab0_text, (40, 55))
    tab1_button = pygame.draw.rect(screen, grey, [10, 85, 100, 30])
    tab1_text = font.render('Party', True, black)
    screen.blit(tab1_text, (35, 90))
    tab2_button = pygame.draw.rect(screen, grey, [10, 120, 100, 30])
    tab2_text = font.render('Ritual', True, black)
    screen.blit(tab2_text, (33, 125))
    tab3_button = pygame.draw.rect(screen, grey, [10, 155, 100, 30])
    tab3_text = font.render('Routine', True, black)
    screen.blit(tab3_text, (30, 160))
    tab4_button = pygame.draw.rect(screen, grey, [10, 190, 100, 30])
    tab4_text = font.render('Story', True, black)
    screen.blit(tab4_text, (40, 195))
    tab5_button = pygame.draw.rect(screen, grey, [10, 225, 100, 30])
    tab5_text = font.render('Dungeon', True, black)
    screen.blit(tab5_text, (25, 230))
    ####

    # main tab
    hover = (0, 0)
    tooltipname=None


    if tab == 0:
        # grafica delle subtab
        subtab_background = pygame.draw.rect(screen, black, [120, 45, 110, 75 + story_progression * 35])
        subtab0_button = pygame.draw.rect(screen, grey, [125, 50, 100, 30])
        subtab0_text = font.render('Astral plane', True, black)
        screen.blit(subtab0_text, (128, 55))
        subtab1_button = pygame.draw.rect(screen, grey, [125, 85, 100, 30])
        subtab1_text = font.render('Village', True, black)
        screen.blit(subtab1_text, (150, 90))
        if story_progression > 0:
            subtab2_button = pygame.draw.rect(screen, grey, [125, 120, 100, 30])
            subtab2_text = font.render('City', True, black)
            screen.blit(subtab2_text, (155, 125))
            if story_progression > 1:
                subtab3_button = pygame.draw.rect(screen, grey, [125, 155, 100, 30])
                subtab3_text = font.render('Coast', True, black)
                screen.blit(subtab3_text, (150, 160))
                if story_progression > 2:
                    subtab4_button = pygame.draw.rect(screen, grey, [125, 190, 100, 30])
                    subtab4_text = font.render('Jungle', True, black)
                    screen.blit(subtab4_text, (145, 195))

        if subtab == 1:

            # definisco quali instantaction ci sono
            instantactions['Get motivated'] = {'isvisible': 1, 'buttonpos': 0}
            if woodquest >= 0.1:
                instantactions['Get wood'] = {'isvisible': 1, 'buttonpos': 0}
                instantactions['Split wood'] = {'isvisible': 1, 'buttonpos': 0}

            # disegno le instantaction
            n_ofvisible = 0

            for keynumber, key in enumerate(instantactions):
                if instantactions[key]['isvisible']:
                    action0_background = pygame.draw.rect(screen, black, [235, 45 + 30 * n_ofvisible, 150, 40])
                    action0_button = pygame.draw.rect(screen, white, [240, 50 + 30 * n_ofvisible, 140, 30])
                    action0_text = font.render(key, True, black)
                    screen.blit(action0_text, (240, 55 + 30 * n_ofvisible))
                    instantactions[key]['buttonpos'] = action0_button
                    n_ofvisible += 1
                    if action0_button.collidepoint(pygame.mouse.get_pos()):
                        hover=pygame.mouse.get_pos()
                        tooltipname=key

            # definisco quali upgradeaction ci sono
            if woodquest == 0:
                upgradeactions['Visit the lumbermill'] = {'isvisible': 1, 'buttonpos': 0}
            if 0.1 <= woodquest < 0.2:
                upgradeactions['expand storage'] = {'isvisible': 1, 'buttonpos': 0}

            # disegno le upgradeaction
            n_ofvisible3 = 0
            for keynumber, key in enumerate(upgradeactions):
                if upgradeactions[key]['isvisible']:
                    action0_background = pygame.draw.rect(screen, black, [615, 45 + 30 * n_ofvisible3, 150, 40])
                    action0_button = pygame.draw.rect(screen, white, [620, 50 + 30 * n_ofvisible3, 140, 30])
                    action0_text = font.render(key, True, black)
                    screen.blit(action0_text, (620, 55 + 30 * n_ofvisible3))
                    upgradeactions[key]['buttonpos'] = action0_button
                    n_ofvisible3 += 1
                    if action0_button.collidepoint(pygame.mouse.get_pos()):
                        hover=pygame.mouse.get_pos()
                        tooltipname=key

            # definisco quali loopaction ci sono

            # disegno le loopaction
            n_ofvisible2 = 0
            for keynumber, key in enumerate(loopactions):
                if loopactions[key]['isvisible']:
                    action0_background = pygame.draw.rect(screen, black, [425, 45 + 30 * n_ofvisible2, 150, 40])
                    action0_button = pygame.draw.rect(screen, white, [430, 50 + 30 * n_ofvisible2, 140, 30])
                    if key == currentloopaction:
                        action0_progress = pygame.draw.rect(screen, grey, [430, 50 + 30 * n_ofvisible2,looptimer / (loopactions[currentloopaction]['time'] * 60) * 140, 30])
                    action0_text = font.render(key, True, black)
                    screen.blit(action0_text, (430, 55 + 30 * n_ofvisible2))
                    loopactions[key]['buttonpos'] = action0_button
                    n_ofvisible2 += 1
                    if action0_button.collidepoint(pygame.mouse.get_pos()):
                        hover=pygame.mouse.get_pos()
                        tooltipname=key
            #definisco quali dungeon ci sono
            dungeonactions['rat cellar']={'isvisible':1,'buttonpos':0}
            if dungeonprogress>=0.1:
                dungeonactions["coco's lair"] = {'isvisible': 1, 'buttonpos': 0}


            #disegno i dungeon
            n_ofvisible4 = 0
            for keynumber, key in enumerate(dungeonactions):
                if dungeonactions[key]['isvisible']:
                    action0_background = pygame.draw.rect(screen, black, [995, 45 + 30 * n_ofvisible4, 150, 40])
                    dungeonactions[key]['buttonpos'] = pygame.draw.rect(screen, white, [1000, 50 + 30 * n_ofvisible4, 140, 30])
                    action0_text = font.render(key, True, black)
                    screen.blit(action0_text, (1005, 55 + 30 * n_ofvisible4))
                    n_ofvisible4+=1
                    if dungeonactions[key]['buttonpos'].collidepoint(pygame.mouse.get_pos()):
                        hover=pygame.mouse.get_pos()
                        tooltipname=key

            #hover and tooltip

            if hover!=(0,0):
                pygame.draw.rect(screen,black,[hover[0],hover[1],140,140])
                if tooltipname == 'Get motivated':
                    pastetext('Test1',hover[0]+20,hover[1]+20,True,white)


    elif tab == 1:
        pygame.draw.rect(screen, black, [325, 45, 480, 40])
        partysubtab0=pygame.draw.rect(screen, grey, [330, 50, 90, 30])
        pastetext('Main',355,55)
        partysubtab1 = pygame.draw.rect(screen, grey, [425, 50, 90, 30])
        pastetext('Level up', 430, 55)
        partysubtab2 = pygame.draw.rect(screen, grey, [520, 50, 90, 30])
        pastetext('Quest', 530, 55)
        partysubtab3 = pygame.draw.rect(screen, grey, [615, 50, 90, 30])
        pastetext('Bestiary', 630, 55)
        partysubtab4 = pygame.draw.rect(screen, grey, [710, 50, 90, 30])
        pastetext('Skill', 730, 55)
        partysubtabs=[partysubtab0,partysubtab1,partysubtab2,partysubtab3,partysubtab4]
        if subtab == 0:
            grey_background = pygame.draw.rect(screen,grey,[130,240,600,190])
            grey_background2 = pygame.draw.rect(screen, grey, [130, 440, 600, 365])
            for number,pokemon in enumerate(Party[startvisiblelist:endvisiblelist]):
                createaPokemon(screen,pokemon,number,0)
            blackbar1 = pygame.draw.rect(screen, black, [705, 245, 15, 180])
            lengthwhitebar1=5/max(5,len(Party))
            whitebar1 = pygame.draw.rect(screen, white, [706, 246+185*startvisiblelist/len(Party), 13, 178*lengthwhitebar1])
            for number,pokemon in enumerate(Reserve[startvisiblelist2:endvisiblelist2]):
                createaPokemon(screen, pokemon, number, 200)
            blackbar2 = pygame.draw.rect(screen, black, [705, 445, 15, 350])
            lengthwhitebar2 = 10 / max(10, len(Reserve))
            whitebar2 = pygame.draw.rect(screen, white,[706, 446 + 350 * startvisiblelist2 / len(Reserve), 13, 348 * lengthwhitebar2])

        elif subtab == 1:
            grey_background = pygame.draw.rect(screen, grey, [130, 240, 600, 540])
            Leveluppable=[e for e in AllPokemons if e.unlocked]
            blackbar3 = pygame.draw.rect(screen, black, [705, 245, 15, 530])
            lengthwhitebar3 = 15 / max(15, len(Leveluppable))
            whitebar3 = pygame.draw.rect(screen, white,[706, 246 + 530 * startvisiblelistlevelup / len(Leveluppable), 13, 528 * lengthwhitebar3])
            for number,pokemon in enumerate(Leveluppable[startvisiblelistlevelup:endvisiblelistlevelup]):
                pygame.draw.rect(screen, black, [135, 245 + number * 35, 150, 40])
                pygame.draw.rect(screen, white, [140, 250 + number * 35, 140, 30])
                pastetext(pokemon.type,145,260 + number * 35)
                pygame.draw.rect(screen, black, [438, 248 + number * 35, 54, 13])
                pokemon.summon=pygame.draw.rect(screen, white, [440, 250 + number * 35, 50, 9])
                summon_text = font2.render('Summon', True, black)
                screen.blit(summon_text, (443, 250+number*35))
                level_text = font2.render(str(pokemon.lvl)+'/'+str(pokemon.maxlvl), True, black)
                screen.blit(level_text, (443, 263 + number * 35))
                pygame.draw.rect(screen, black, [498, 248 + number * 35, 54, 13])
                pokemon.physbutt=pygame.draw.rect(screen, white, [500, 250 + number * 35, 50, 9])
                phys_text = font2.render('Phys', True, black)
                screen.blit(phys_text, (503, 250 + number * 35))
                physlvl_text = font2.render(str(pokemon.phys) + '/' + str(pokemon.lvl), True, black)
                screen.blit(physlvl_text, (503, 263 + number * 35))
                pygame.draw.rect(screen, black, [558, 248 + number * 35, 54, 13])
                pokemon.magicbutt=pygame.draw.rect(screen, white, [560, 250 + number * 35, 50, 9])
                magic_text = font2.render('Magic', True, black)
                screen.blit(magic_text, (563, 250 + number * 35))
                magiclvl_text = font2.render(str(pokemon.magic) + '/' + str(pokemon.lvl), True, black)
                screen.blit(magiclvl_text, (563, 263 + number * 35))
                pygame.draw.rect(screen, black, [618, 248 + number * 35, 54, 13])
                pokemon.specialbutt=pygame.draw.rect(screen, white, [620, 250 + number * 35, 50, 9])
                special_text = font2.render('Special', True, black)
                screen.blit(special_text, (623, 250 + number * 35))
                speciallvl_text = font2.render(str(pokemon.special) + '/' + str(pokemon.lvl), True, black)
                screen.blit(speciallvl_text, (623, 263 + number * 35))
    elif tab == 5:
        test_background = pygame.draw.rect(screen, black, [1000, 45, 150, 40])
        test_button = pygame.draw.rect(screen, white, [1005, 50, 140, 30])
        pastetext('Back',1010,55,True,black)
        for num,pokemon in enumerate(Party[0:5]):
            pygame.draw.rect(screen, black, [198, 148+num*100, 144, 34])
            pygame.draw.rect(screen, red, [200, 150+num*100, pokemon.currenthp/pokemon.hp*140, 30])
            pygame.draw.rect(screen, black, [198, 178 + num * 100, 144, 24])
            pygame.draw.rect(screen, grey, [200, 180 + num * 100,140, 20])
            pastetext(pokemon.type,200,130+num*100)
        if currentdungeon is not None:
            if currentdungeon.containspokemon():
                for num,pokemon in enumerate(currentdungeon.Generatedpokemon):
                    pygame.draw.rect(screen, black, [498, 148 + num * 100, 144, 34])
                    pygame.draw.rect(screen, red, [500, 150 + num * 100, pokemon.currenthp / pokemon.hp * 140, 30])
                    pygame.draw.rect(screen, black, [498, 178 + num * 100, 144, 24])
                    pygame.draw.rect(screen, grey, [500, 180 + num * 100, 140, 20])
                    pastetext(pokemon.type, 500, 130 + num * 100)

    events=pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if tab == 1:
                if subtab == 0:
                    if grey_background.collidepoint(pygame.mouse.get_pos()) and not delay:
                        if event.y == 1 and startvisiblelist:
                            startvisiblelist -= 1
                            endvisiblelist -= 1

                        elif event.y == -1 and endvisiblelist < len(Party):
                            startvisiblelist += 1
                            endvisiblelist += 1
                    if grey_background2.collidepoint(pygame.mouse.get_pos()) and not delay:
                        if event.y == 1 and startvisiblelist2:
                            startvisiblelist2 -= 1
                            endvisiblelist2 -= 1

                        elif event.y == -1 and endvisiblelist2 < len(Reserve):
                            startvisiblelist2 += 1
                            endvisiblelist2 += 1
                if subtab == 1:
                    if grey_background.collidepoint(pygame.mouse.get_pos()) and not delay:
                        if event.y == 1 and startvisiblelistlevelup:
                            startvisiblelistlevelup -= 1
                            endvisiblelistlevelup -= 1

                        elif event.y == -1 and endvisiblelistlevelup < len(Leveluppable):
                            startvisiblelistlevelup += 1
                            endvisiblelistlevelup += 1
                delay = 15

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if [e for e in events if e.type == pygame.MOUSEWHEEL]:
                continue
            if tab == 0:
                positions = [subtab0_button, subtab1_button, subtab2_button, subtab3_button, subtab4_button]
                for x, y in enumerate(positions):
                    if y.collidepoint(event.pos):
                        subtab = x
                for square in squaremenu:
                    if squaremenu[square].collidepoint(event.pos):
                        resourcetypes[square] = 1
                for square in redsquaremenu:
                    if redsquaremenu[square].collidepoint(event.pos):
                        resourcetypes[square] = 0
                if subtab == 1:
                    # cosa succede se clicco su una instantaction
                    for key in instantactions:
                        if instantactions[key]['buttonpos'].collidepoint(event.pos):
                            if (key == 'Get motivated'
                                    and energies['Action']['current'] >= 1
                                    and destiny < destinymax
                                    and not delay):
                                energies['Action']['current'] -= 1
                                destiny += 1
                                delay = 15
                            elif (key == 'Get wood'
                                  and energies['Stamina']['current'] >= 1
                                  and everyitem['wood'] < everyitemmax['wood']
                                  and not delay):
                                energies['Stamina']['current'] -= 1
                                everyitem['wood'] += 1
                                delay = 15
                            elif (key == 'Split wood'
                                  and everyitem['wood'] >= 1
                                  and everyitem['firewood'] < everyitemmax['firewood']
                                  and not delay):
                                everyitem['wood'] -= 1
                                everyitem['firewood'] += 8
                                delay = 15
                    # cosa succede se clicco su una upgradeaction
                    for key in upgradeactions:
                        if upgradeactions[key]['buttonpos'].collidepoint(event.pos):
                            if (key == 'Visit the lumbermill'
                                    and destiny >= 40
                                    and not delay):
                                woodquest = 0.1
                                destiny -= 40
                                upgradeactions['Visit the lumbermill']['isvisible'] = 0
                                unlocked_resources['wood'].append('wood')
                                unlocked_resources['wood'].append('firewood')
                                delay = 15
                            if (key == 'expand storage'
                                    and everyitem['gold'] >= 80
                                    and not delay):
                                woodquest += 0.01
                                everyitem['gold'] -= 80
                                upgradeactions['expand storage']['isvisible'] = 0
                                everyitemmax['firewood'] += 8
                                delay = 15

                    # cosa succede se clicco su una loopaction
                    for key in loopactions:
                        if loopactions[key]['buttonpos'] is not None and loopactions[key]['buttonpos'].collidepoint(event.pos):
                            if not looptimer or currentloopaction != key:
                                looptimer = 1
                            currentloopaction = key

                            if key == 'rest':
                                previousloopaction = 0

                    #cosa succede se clicco un dungeoun
                    for key in dungeonactions:
                        if dungeonactions[key]['buttonpos'].collidepoint(event.pos):
                            tab = 5
                            previoussubtab = 1
                            previoustab = 0
                            currentdungeon =Alldungeons[key]
                            if not currentdungeon.containspokemon():
                                currentdungeon.spawnpokemon()


            elif tab== 1:
                for x, y in enumerate(partysubtabs):
                    if y.collidepoint(event.pos):
                        subtab = x
                if subtab ==0:
                    temp=None
                    temp2=None
                    temp3=None
                    temp4=None
                    temp5=None
                    for x,y in enumerate(Reserve[startvisiblelist2:endvisiblelist2]):
                        if y.add.collidepoint(event.pos) and len(Party)<maxlengthparty:
                            y.unlocked = 2
                            temp4 = y
                            y.remove = None
                            temp5 = x

                    for x,y in enumerate(Party[startvisiblelist:endvisiblelist]):
                        if y.switchup.collidepoint(event.pos) and x:
                            temp=x
                        if y.switchdown.collidepoint(event.pos):
                            temp2=x
                        if y.remove.collidepoint(event.pos) and len(Party)!=1:
                            y.unlocked = 1
                            temp3=x
                    Reserve = [pokemon for pokemon in AllPokemons if pokemon.unlocked == 1]
                    if temp3 is not None:
                        a=0
                        if endvisiblelist == len(Party):
                            a=1
                        Party.pop(startvisiblelist+temp3)
                        if a == 1:
                            if startvisiblelist!=0:
                                startvisiblelist-=1
                            endvisiblelist-=1
                    if temp:
                        Party.insert(startvisiblelist+temp-1,Party.pop(startvisiblelist+temp))
                    if temp2 is not None:
                        Party.insert(startvisiblelist + temp2 + 1, Party.pop(startvisiblelist + temp2))
                    if temp4 is not None:
                        Party.append(temp4)
                        if endvisiblelist<5:
                            endvisiblelist+=1
                        if temp5 == endvisiblelist2-startvisiblelist2-1 and endvisiblelist2 == len(Reserve)+1:
                            if startvisiblelist2!=0:
                                startvisiblelist2-=1
                            endvisiblelist2-=1

                elif subtab == 1:
                    for pokemon in Leveluppable:
                        #mettere condizione con i semi
                        if pokemon.summon is not None:
                            if  pokemon.summon.collidepoint(event.pos) and pokemon.lvl<pokemon.maxlvl:
                                pokemon.lvl+=1
                            if pokemon.physbutt.collidepoint(event.pos) and pokemon.phys<pokemon.lvl:
                                pokemon.phys+=1
                                pokemon.atk+=1
                                pokemon.dif+=1
                            elif pokemon.magicbutt.collidepoint(event.pos) and pokemon.magic<pokemon.lvl:
                                pokemon.magic+=1
                                pokemon.satk+=1
                                pokemon.sdif+=1
                            elif pokemon.specialbutt.collidepoint(event.pos) and pokemon.special<pokemon.lvl:
                                pokemon.special+=1

            elif tab == 5 :
                if test_background.collidepoint(event.pos):
                    tab = previoustab
                    subtab = previoussubtab
            positions = [tab0_button, tab1_button, tab2_button, tab3_button, tab4_button, tab5_button]

            for x, y in enumerate(positions):
                if y.collidepoint(event.pos):
                    if y == tab5_button and tab != 5:
                        previoustab = tab
                        previoussubtab = subtab
                    tab = x
                    subtab = 0

            for square in squaremenu:
                if squaremenu[square].collidepoint(event.pos):
                    resourcetypes[square] = 1
            for square in redsquaremenu:
                if redsquaremenu[square].collidepoint(event.pos):
                    resourcetypes[square] = 0
    squaremenu = {}
    redsquaremenu = {}

    pygame.display.flip()

pygame.quit()