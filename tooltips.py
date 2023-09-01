description={'Get motivated':['test1','test2','test3']}

def actionTooltip(name,cost,complete):
    finaltooltip=[]
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    if cost[0][1]!=0:
        finaltooltip.append('<<cost>>')
        for i in cost:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    if complete[0][1]!=0:
        finaltooltip.append('[complete effect]')
        for i in complete:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    return finaltooltip
def upgradeTooltip(name,cost,complete,requirements):
    finaltooltip=[]
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    if requirements[0][1]!=0:
        finaltooltip.append('requirements')
        for i in requirements:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    if cost[0][1]!=0:
        finaltooltip.append('<<cost>>')
        for i in cost:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    if complete[0][1]!=0:
        finaltooltip.append('[complete effect]')
        for i in complete:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    return finaltooltip

def loopTooltip(name,cost,complete,progresscost,progresseffect):
    finaltooltip=[]
    if name in description.keys():
        for i in description[name]:
            finaltooltip.append(i)
    if cost[0][1]!=0:
        finaltooltip.append('<<cost>>')
        for i in cost:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    if progresscost[0][1]!=0:
        finaltooltip.append('<<progress cost>>')
        for i in progresscost:
            finaltooltip.append(f'{i[0]}:{round(i[1],3)} ({i[2]}/{i[3]})')
    if progresseffect[0][1]!=0:
        finaltooltip.append('[progress effect]')
        for i in progresseffect:
            finaltooltip.append(f'{i[0]}:{round(i[1],3)} ({i[2]}/{i[3]})')
    if complete[0][1]!=0:
        finaltooltip.append('[complete effect]')
        for i in complete:
            finaltooltip.append(f'{i[0]}:{i[1]} ({i[2]}/{i[3]})')
    return finaltooltip
