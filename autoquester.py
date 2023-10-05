
import xml.etree.ElementTree as ET
import autopep8


tree = ET.parse('Autoquests.drawio')

def convertcost(string):
    finalproduct='['
    n=0
    for e in string:

        if e=='[':
            n=0
            finalproduct+=(e+"'")
        elif e==']':
            n=1
            finalproduct+=(',0,0]')
        elif e==',' and n==0:
            n=1
            finalproduct+="',-"
        else:
            finalproduct+=e
    finalproduct += ']'
    return(finalproduct)
def convertcomplete(string):
    finalproduct='['
    n=2
    for e in string:

        if e=='[':
            n=2
            finalproduct+=(e+"'")
        elif e==']':
            n=0
            finalproduct+=(',0,0]')
        elif e==',' and n>0:
            n-=1
            if n==1:
                finalproduct+="','"
            else:
                finalproduct += "',"
        else:
            finalproduct+=e
    finalproduct += ']'
    return(finalproduct)
def convertlocation(string):
    finalproduct=''
    for e in string:
        if e=='[':
            finalproduct += (e + "'")
        elif e == ',':
            finalproduct += "','"
        elif e==']':
            finalproduct+=("']")
        else:
            finalproduct+=e
    return finalproduct

def idfinder(root,idlist):
    for child in root:
        if 'id' in child.attrib and len(child.attrib['id'])>4:
            idlist.append(child)
        idfinder(child,idlist)
    return idlist
filecontent='''
def quest(parent):
    from initialization_elements import Quests\n'''

for diagram in tree.getroot():
    idlist=[]
    idfinder(diagram,idlist)
    lines=[]

    for line in [e for e in idlist if 'target' in e.attrib]:
        lines.append([line.attrib['source'],line.attrib['target'],'fillColor=#f8cecc' not in line.attrib['style']])
        redlines=[line for line in lines if not line[2]]
    objects=[e for e in idlist if 'target' not in e.attrib and len(e.attrib['label'])>=3]
    def getquestleng(quest,num=0):
        num+=1
        for targetid in  [e[1] for e in lines if e[0]==quest.attrib['id']]:
            target=[e for e in objects if e.attrib['id']==targetid][0]
            num=getquestleng(target,num)
        return num

    numberofmerges=0

    def createquest(quest,questlineflag,questlineflagamount,listofidscreated=[]):
        global filecontent
        isitamerge=len([e[0] for e in lines if e[1]==quest.attrib['id'] and e[2]])>1
        childrenid=[e[1] for e in lines if e[0] == quest.attrib['id'] and e[2]]
        locksid=[e[1] for e in redlines if e[0] == quest.attrib['id']]
        childrenlocks=[]
        children=[]
        for id in locksid:
            childrenlocks.append([e for e in objects if e.attrib['id']==id][0])
        for id in childrenid:
            children.append([e for e in objects if e.attrib['id']==id][0])
        numberofchildren=len(children)
        if isitamerge:
            questlineflag=quest.attrib['label']
        finalstring=("Quests(parent=parent,")
        finalstring+=f"name='{quest.attrib['label']}'"
        finalstring+=f',cost={convertcost(quest.attrib["cost"])},'
        finalstring+=f'complete={convertcomplete(quest.attrib["complete"])},'
        finalstring += f'location={convertlocation(quest.attrib["location"])},'
        finalstring += 'unlockflags={'+f"'{questlineflag}':{questlineflagamount}"+'},'
        finalstring += 'closingflags={' + f"'{questlineflag}':{questlineflagamount+max(1,len([e[0] for e in lines if e[1]==quest.attrib['id'] and e[2]]))}" + '},'
        finalstring += 'changeflags={'
        for i in range(len(childrenlocks)):
            finalstring += f"'{childrenlocks[i].attrib['label']}':{len([e[0] for e in lines if e[1]==childrenlocks[i].attrib['id'] and e[2]])+99},"
        finalstring += f"'{questlineflag}':{max(1,len([e[0] for e in lines if e[1]==quest.attrib['id'] and e[2]]))},"
        for i in range(numberofchildren):
            finalstring+=f"'{children[i].attrib['label']}':1"
            if i!=numberofchildren-1:
                finalstring+=','

        finalstring+='})'
        filecontent+=f'    {finalstring}\n'
        listofidscreated.append(quest.attrib['id'])
        for num,targetid in  enumerate([e[1] for e in lines if e[0]==quest.attrib['id'] ]):
            target=[e for e in objects if e.attrib['id']==targetid][0]
            if targetid not in listofidscreated:
                createquest(target, target.attrib['label'],  1,listofidscreated)
    targetlist=[e[1] for e in lines]
    for element in objects:
        if element.attrib['id'] not in targetlist and 'target' not in element.attrib:
            createquest(element,element.attrib['label'],1)
with open('automaticquests/villagequest.py', "w") as file1:
    file1.write(filecontent)
print(filecontent)



'''def function(parent):
    from initialization_elements import Quests 
    Quests(parent=parent, name='Talk to Father 1/12',isvisible=True,location=['Village', 'Home'],unlockflags={
    'Father': 0}, closingflags={'Father': 1}, changeflags={'Father': 1, 'Popup': 2},cost=[['Fate', -5, 0, 0]], 
    complete=[['max', 'Fate', 5, 0, 0]])'''