description = {'Get motivated': ['test1', 'test2', 'test3'],'Wood': ['Suitable wood for','making firewood.']}

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


def resourceTooltip(name,quantity,max,effect=None):
    finaltooltip = []
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    finaltooltip.append(f'{numcon(quantity)}/{numcon(max)}')
    return finaltooltip

def energyTooltip(name,quantity,max,regen,effect=None):
    finaltooltip = []
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    finaltooltip.append(f'{round(quantity,1)}/{round(max,1)}')
    finaltooltip.append(f'Regeneration    {regen*240}/s')
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
    if complete[0][1] != 0:
        statdict = {'hp': 'Max hp', 'patk': 'Physical Attack', 'pdef': 'Physical Defense', 'matk': 'Magical Attack',
                    'mdef': 'Magical Defense'}
        finaltooltip.append('[complete effect]')
        for i in complete:
            if i[0] == 'resource':
                finaltooltip.append(f'{i[1]} : {i[2]} ({numcon(i[3])}/{numcon(i[4])})')
            elif i[0] == 'max':
                finaltooltip.append(f'{i[1]} {i[0]} : {i[2]}')
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
