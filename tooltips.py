def autospacer(text):
    list = text.split(" ")
    output = ""
    n = 0
    for num, i in enumerate(list):
        if len(" ".join(list[n:num])) > 30:
            output += "\n"
            output += " ".join(list[n:num - 1])
            n = num - 1
        if num == len(list) - 1:
            output += "\n"
            output += " ".join(list[n:num + 1])
    return [output[1:]]


description = {
    'Ponder the future': 'Reflect upon your actions and make a wish for a successful life',
    'Rest': 'Take a breather from the weight of the world',
    'Exercise': 'Time to get moving!',
    'Cutting wood': 'Embrace your masculine self',
    'Get weeds': 'What do we even need them for?',
    'Parse through weeds': 'Maybe we can find something useful in these',
    'Enter your home': 'Welcome gamer!You can use the instant action "Ponder the future" to gain fate',
    'Talk with father 1/11': 'Fate is used as the main resource of this adventure,to proceed with the story and unlock new resources',
    'Talk with father 2/11': 'You have now unlocked wood!To gain stamina you can use the loop action "Exercise"',
    'Talk with father 3/11': 'Quests, such as the one you are seeing right now, can have a variety of effects',
    'Talk with father 4/11': 'For example, right now you are raising the maximum cap for your wood resource',
    'Talk with father 5/11': "There are many other possible effects that you will discover with time",
    'Talk with father 6/11': "Let's now talk about dungeons: this will be another way of proceeding in the story",
    'Talk with father 7/11': 'You have unlocked your first dungeon, you can find it in the "Dungeons" section',
    'Talk with father 8/11': 'Dungeons drop gems , that you can use to make your party more powerful in the party tab',
    'Talk with father 9/11': 'Physical gems improve hp,atk and def, magical gems improve matk and mdef, and special gems currently do nothing',
    'Talk with father 10/11': 'I will now proceed to get in character for this whole charade',
    'Talk with father 11/11': 'Little soldier!"Would you mind fetching your mom?She is in the garden',
    'Talk with mother 1/10': 'Ehy sweetie, how did you get here?The garden is dangerous',
    'Talk with mother 2/10': 'Oh you want to help me with the garden?How nice!',
    'Talk with mother 3/10': 'Well you are old enough to go around in the village',
    'Talk with mother 4/10': 'So i guess you can help me too',
    'Talk with mother 5/10': "Let's start by getting some weeds from the garden",
    'Talk with mother 6/10': 'Next step is to parse through the weeds to find something useful',
    'Talk with mother 7/10': 'These herbs were used by people to connect with their inner self',
    'Talk with mother 8/10': "Or at least that's the old folks at the village like to say",
    'Talk with mother 9/10': "I wouldn't know, after all i've never used them myself eheh",
    'Talk with mother 10/10': "Anyway it's time for dinner, go fetch your brother in the fields",

}
storydescription=description.copy()
itemsdescription = {'Wood': 'Suitable wood for making firewood'}
pokemondescription = {'You': 'You are beautiful'}
skilldescription={}
for key in description:
    description[key] = autospacer(description[key])
for key in skilldescription:
    skilldescription[key] = autospacer(skilldescription[key])
for key in itemsdescription:
    itemsdescription[key] = autospacer(itemsdescription[key])
for key in pokemondescription:
    pokemondescription[key] = autospacer(pokemondescription[key])


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
def dungeontooltip(dungeon):
    finaltooltip = [f'{dungeon.name}']
    if dungeon.cleared:
        finaltooltip[0]+='(Cleared)'
    mainenemieslist=''
    for num,pokemon in enumerate(dungeon.monsterlist):
        mainenemieslist+=f'{pokemon.name}'
        if num!= len(dungeon.monsterlist)-1:
            mainenemieslist+=','
    if len(mainenemieslist):
        finaltooltip.append(f"Main enemies: {mainenemieslist}")
    if dungeon.boss is not None:
        finaltooltip.append(f"Boss:{dungeon.boss.name}")
    if dungeon.usualrewards is not None:
        rewardlist=''
        for num,reward in enumerate(dungeon.usualrewards):
            rewardlist += f'{reward[1]}:{reward[2]}'
            if num != len(dungeon.usualrewards) - 1:
                rewardlist += ','
        finaltooltip.append(f"[Rewards]:")
        finaltooltip.append(rewardlist)
    if dungeon.firsttime is not None:
        rewardlist=''
        for num,reward in enumerate(dungeon.firsttime):
            if reward[0]=='maxlvl':
                rewardlist+=f'Your max level +{reward[1]}'
            elif reward[0]=='resource':
                rewardlist += f'{reward[1]}:{reward[2]}'
            if num != len(dungeon.firsttime) - 1:
                rewardlist += ','
        finaltooltip.append(f"[First time clear]:")
        finaltooltip.append(rewardlist)


    return finaltooltip
def templatetooltip(partytemplate):
    finaltooltip = []
    finaltooltip.append(f'Party')
    for pokemon in partytemplate:
        finaltooltip.append(pokemon.name)
        finaltooltip.append(f'-{pokemon.skill.name}')
    return finaltooltip

def pokemontooltip(pokemon, status, soul=None):
    finaltooltip = []
    if pokemon.name in pokemondescription.keys():
        for i in pokemondescription[pokemon.name]:
            finaltooltip.append(i)
    finaltooltip.append(f'Condition:{status}')
    finaltooltip.append(f'Hp :{numcon(pokemon.actualhp)}({numcon(pokemon.scaling1 * 100)}%)')
    finaltooltip.append(f'Patk :{numcon(pokemon.actualpatk)}({numcon(pokemon.scaling1 * 100)}%)')
    finaltooltip.append(f'Pdef :{numcon(pokemon.actualpdef)}({numcon(pokemon.scaling1 * 100)}%)')
    finaltooltip.append(f'Matk :{numcon(pokemon.actualmatk)}({numcon(pokemon.scaling2 * 100)}%)')
    finaltooltip.append(f'Mdef :{numcon(pokemon.actualmdef)}({numcon(pokemon.scaling2 * 100)}%)')
    if len(pokemon.passive):
        finaltooltip.append('[Effect when in party]')
        for passive in pokemon.passive:
            dict={'patk':'Phisical attack','pdef':'Phisical defense','hp':'Healt','matk':'Magic attack','mdef':'Magic defense'}
            if passive.type=='resourcemax' or passive.type=='energymax':
                finaltooltip.append(f'{passive.thing} max: +{numcon(passive.quantity)}')
            if passive.type=='resourceregen'or passive.type=='energyregen':
                finaltooltip.append(f'{passive.thing} regen: +{numcon(passive.quantity)}/s')
            if passive.type=='addstats':
                finaltooltip.append(f'{dict[passive.thing]} :+{numcon(passive.quantity)}')
            if passive.type == 'mulstats':
                finaltooltip.append(f'{dict[passive.thing]} :+{numcon(passive.quantity*100)}%')
            if passive.type == 'longimprove':
                finaltooltip.append(f'{passive.thing} effect: +{numcon(passive.quantity*100)}%')
    if soul is not None:
        finaltooltip.append(f'<<summon cost>>')
        finaltooltip.append(soul)
    return finaltooltip

def skilltooltip(skill,cost):
    finaltooltip = []
    finaltooltip.append(f'{skill.name}')
    if skill.name in skilldescription:
        for i in skilldescription[skill.name]:
            finaltooltip.append(i)
    finaltooltip.append(f'Cost:{cost} gold')
    finaltooltip.append(f'Power:{skill.power}')
    finaltooltip.append(f'Countdown:{skill.interval}')
    finaltooltip.append(f'Category:{skill.category}')
    if skill.type is not False:
        finaltooltip.append(f'Type:{skill.type}')
    else:
        finaltooltip.append(f'Type: Neutral')
    return finaltooltip




def resourceTooltip(name, quantity, max, effect=None):
    finaltooltip = []
    if name in itemsdescription.keys():
        for i in itemsdescription[name]:
            finaltooltip.append(i)
    finaltooltip.append(f'{numcon(quantity)}/{numcon(max)}')
    return finaltooltip


def energyTooltip(name, quantity, max, regen, effect=None):
    finaltooltip = []
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    finaltooltip.append(f'{round(quantity, 1)}/{round(max, 1)}')
    finaltooltip.append(f'Regeneration    {regen * 120}/s')
    return finaltooltip


def actionTooltip(name, cost, complete):
    finaltooltip = []
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    if cost[0][1] != 0:
        finaltooltip.append('<<cost>>')
        for i in cost:
            finaltooltip.append(f'{i[0]}:{i[1]} ({numcon(i[2])}/{numcon(i[3])})')
    if complete[0][1] != 0:
        finaltooltip.append('[complete effect]')
        for i in complete:
            finaltooltip.append(f'{i[0]}:{i[1]} ({numcon(i[2])}/{numcon(i[3])})')
    return finaltooltip


def questTooltip(name, cost, complete, requirements):
    finaltooltip = []
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    if requirements[0][1] != 0:
        finaltooltip.append('requirements')
        for i in requirements:
            finaltooltip.append(f'{i[0]}:{i[1]} ({numcon(i[2])}/{numcon(i[3])})')
    if cost[0][1] != 0:
        finaltooltip.append('<<cost>>')
        for i in cost:
            finaltooltip.append(f'{i[0]}:{i[1]} ({numcon(i[2])}/{numcon(i[3])})')
    if complete[0][2] != 0:
        statdict = {'hp': 'Max hp', 'patk': 'Physical Attack', 'pdef': 'Physical Defense', 'matk': 'Magical Attack',
                    'mdef': 'Magical Defense'}
        finaltooltip.append('[complete effect]')
        for i in complete:
            if i[0] == 'resource':
                finaltooltip.append(f'{i[1]} : {i[2]} ({numcon(i[3])}/{numcon(i[4])})')
            elif i[0] == 'max':
                finaltooltip.append(f'{i[1]} {i[0]} : +{i[2]}')
            elif i[0] == 'stats':
                finaltooltip.append(f'{statdict[i[1]]} : {i[2]}')
    return finaltooltip


def loopTooltip(name, cost, complete, progresscost, progresseffect):
    finaltooltip = []
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    if cost[0][1] != 0:
        finaltooltip.append('<<cost>>')
        for i in cost:
            finaltooltip.append(f'{i[0]}:{i[1]} ({numcon(i[2])}/{numcon(i[3])})')
    if progresscost[0][1] != 0:
        finaltooltip.append('<<progress cost>>')
        for i in progresscost:
            finaltooltip.append(f'{i[0]}:{round(i[1], 3)} ({numcon(i[2])}/{numcon(i[3])})')
    if progresseffect[0][1] != 0:
        finaltooltip.append('[progress effect]')
        for i in progresseffect:
            finaltooltip.append(f'{i[0]}:{round(i[1], 3)} ({numcon(i[2])}/{numcon(i[3])})')
    if complete[0][1] != 0:
        finaltooltip.append('[complete effect]')
        for i in complete:
            finaltooltip.append(f'{i[0]}:{i[1]} ({numcon(i[2])}/{numcon(i[3])})')
    return finaltooltip
