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
    return [output]


description = {
    'Ponder the future': 'Reflect upon your actions and make a wish for a successful life',
    'Rest': 'Take a breather from the weight of the world',
    'Exercise': 'Time to get moving!',
    'Cutting wood': 'Embrace your masculine self',
    'Get weeds': 'What do we even need them for?',
    'Parse through weeds': 'Maybe we can find something useful in these',
    'Talk to Father 1/12': 'Welcome gamer!You can use the instant action "Ponder the future" to gain fate',
    'Talk to Father 2/12': 'Fate is used as the main resource of this adventure,to proceed with the story and unlock new resources',
    'Talk to Father 3/12': 'You have now unlocked wood!To gain stamina you can use the loop action "Exercise"',
    'Talk to Father 4/12': 'Upgrade actions, such as the one you are seeing right now, can have a variety of effects',
    'Talk to Father 5/12': 'For example, right now you are raising the maximum cap for your wood resource',
    'Talk to Father 6/12': "There are many other possible effects that you will discover with time",
    'Talk to Father 7/12': "Let's now talk about dungeons: this will be another way of proceeding in the story",
    'Talk to Father 8/12': 'You have unlocked your first dungeon, you can find it in the "Dungeons" section',
    'Talk to Father 9/12': 'Dungeons drop gems , that you can use to make your party more powerful in the party tab',
    'Talk to Father 10/12': 'Physical gems improve hp,atk and def, magical gems improve matk and mdef, and special gems currently do nothing',
    'Talk to Father 11/12': 'I will now proceed to get in character for this whole charade',
    'Talk to Father 12/12': 'Little soldier!"Would you mind fetching your mom?She is in the garden',
    'Talk to Mother 1/10': 'Ehy sweetie, how did you get here?The garden is dangerous',
    'Talk to Mother 2/10': 'Oh you want to help me with the garden?How nice!',
    'Talk to Mother 3/10': 'Well you are old enough to go around in the village',
    'Talk to Mother 4/10': 'So i guess you can help me too',
    'Talk to Mother 5/10': "Let's start by getting some weeds from the garden",
    'Talk to Mother 6/10': 'Next step is to parse through the weeds to find something useful',
    'Talk to Mother 7/10': 'These herbs were used by people to connect with their inner self',
    'Talk to Mother 8/10': "Or at least that's the old folks at the village like to say",
    'Talk to Mother 9/10': "I wouldn't know, after all i've never used them myself eheh",
    'Talk to Mother 10/10': "Anyway it's time for dinner, go fetch your brother in the fields",

}
itemsdescription = {'Wood': 'Suitable wood for making firewood'}
pokemondescription = {'You': 'You are beautiful'}
for key in description:
    description[key] = autospacer(description[key])
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


def pokemontooltip(pokemon, status, soul=None, cost=None):
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
    if soul is not None:
        finaltooltip.append(f'<<summon cost>>')
        finaltooltip.append(soul)
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
    finaltooltip.append(f'Regeneration    {regen * 240}/s')
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


def upgradeTooltip(name, cost, complete, requirements):
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
            elif i[0] == 'stat':
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
