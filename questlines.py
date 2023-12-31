import importlib
def createquests(parent):
    import os
    path = "automaticquests"
    dir_list = os.listdir(path)
    for dir in dir_list:
        if not dir.startswith("__"):
            dir=dir[:-3]
            my_module = importlib.import_module(f"automaticquests.{dir}")
            my_module.quest(parent)
    #fatherquestline(parent)
    #motherquestline(parent)
    #brotherquestline(parent)
    #billythekidquestline(parent)
    #zenmasterquestline(parent)
    #butchershopquestline(parent)
    #testquest(parent)
    #shopquestline(parent)


def shopquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Enter the sleazy shop',
           location=['Village', 'Shop'],
           unlockflags={'Mother': 5}, closingflags={'Shop': 1}, changeflags={'Shop': 1},
           cost=[['Fate', -20, 0, 0]])
def butchershopquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Butcher shop 1/6',
           location=['Village', 'Village'],
           unlockflags={'Mother': 1}, closingflags={'Butcher': 1}, changeflags={'Butcher': 1},
           cost=[['Frog legs', -5, 0, 0]], complete=[['max', 'Frog legs', 5, 0, 0]]
           )
    Quests(parent=parent, name='Butcher shop 2/6',
           location=['Village', 'Village'],
           unlockflags={'Butcher': 1}, closingflags={'Butcher': 2}, changeflags={'Butcher': 1},
           cost=[['Frog legs', -10, 0, 0]], complete=[['max', 'Frog legs', 5, 0, 0]]
           )
    Quests(parent=parent, name='Butcher shop 3/6',
           location=['Village', 'Village'],
           unlockflags={'Butcher': 2}, closingflags={'Butcher': 3}, changeflags={'Butcher': 1},
           cost=[['Frog legs', -10, 0, 0]],
           complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                     ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
           )
    Quests(parent=parent, name='Butcher shop 4/6',
           location=['Village', 'Village'],
           unlockflags={'Butcher': 3, 'Brother': 1}, closingflags={'Butcher': 4}, changeflags={'Butcher': 1},
           cost=[['Cow hide', -5, 0, 0]],
           complete=[['max', 'Cow hide', 5, 0, 0]]
           )
    Quests(parent=parent, name='Butcher shop 5/6',
           location=['Village', 'Village'],
           unlockflags={'Butcher': 4}, closingflags={'Butcher': 5}, changeflags={'Butcher': 1},
           cost=[['Cow hide', -10, 0, 0]],
           complete=[['max', 'Cow hide', 5, 0, 0]]
           )
    Quests(parent=parent, name='Butcher shop 6/6',
           location=['Village', 'Village'],
           unlockflags={'Butcher': 5}, closingflags={'Butcher': 6}, changeflags={'Butcher': 1},
           cost=[['Cow hide', -10, 0, 0]],
           complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                     ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
           )
def zenmasterquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Talk to the zen master 1/5',
           location=['Village', 'Village'],
           unlockflags={'Mother': 5}, closingflags={'Zen': 1}, changeflags={'Zen': 1},
           cost=[['Gold', -20, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
           )
    Quests(parent=parent, name='Talk to the zen master 2/5',
           location=['Village', 'Village'],
           unlockflags={'Zen': 1}, closingflags={'Zen': 2}, changeflags={'Zen': 1},
           cost=[['Gold', -30, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
           )
    Quests(parent=parent, name='Talk to the zen master 3/5',
           location=['Village', 'Village'],
           unlockflags={'Zen': 2}, closingflags={'Zen': 3}, changeflags={'Zen': 1},
           cost=[['Gold', -40, 0, 0]],
           complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                     ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
           )
    Quests(parent=parent, name='Talk to the zen master 4/5',
           location=['Village', 'Village'],
           unlockflags={'Zen': 3}, closingflags={'Zen': 4}, changeflags={'Zen': 1},
           cost=[['Gold', -50, 0, 0]],
           complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                     ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]]
           )
    Quests(parent=parent, name='Talk to the zen master 5/5',
           location=['Village', 'Village'],
           unlockflags={'Zen': 4}, closingflags={'Zen': 5}, changeflags={'Zen': 1},
           cost=[['Gold', -60, 0, 0]],
           complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                     ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]])
def billythekidquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Talk with Billy the kid 1/3',
           location=['Village', 'Village'],
           unlockflags={'Mother': 1}, closingflags={'Billy': 1}, changeflags={'Billy': 1},
           cost=[['Butterfly wings', -5, 0, 0]], complete=[['max', 'Butterfly wings', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk with Billy the kid 2/3',
           location=['Village', 'Village'],
           unlockflags={'Billy': 1}, closingflags={'Billy': 2}, changeflags={'Billy': 1},
           cost=[['Butterfly wings', -10, 0, 0]], complete=[['max', 'Butterfly wings', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk with Billy the kid 3/3',
           location=['Village', 'Village'],
           unlockflags={'Billy': 2}, closingflags={'Billy': 3}, changeflags={'Billy': 1},
           cost=[['Butterfly wings', -20, 0, 0]],
           complete=[['stat', 'hp', 0.5, 0, 0], ['stat', 'patk', 0.5, 0, 0], ['stat', 'pdef', 0.5, 0, 0],
                     ['stat', 'matk', 0.5, 0, 0], ['stat', 'mdef', 0.5, 0, 0]],
           )
def brotherquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Talk to Brother 1/3',
           location=['Village', 'Home'],
           unlockflags={'Brother': 1}, closingflags={'Brother': 2}, changeflags={'Brother': 1},
           cost=[['Fate', -80, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Brother 2/3',
           location=['Village', 'Home'],
           unlockflags={'Brother': 2}, closingflags={'Brother': 3}, changeflags={'Brother': 1},
           cost=[['Fate', -90, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]]
           )
    Quests(parent=parent, name='Talk to Brother 3/3',
           location=['Village', 'Home'],
           unlockflags={'Brother': 3}, closingflags={'Brother': 4}, changeflags={'Brother': 1},
           cost=[['Fate', -100, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]]
           )
def motherquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Talk to Mother 1/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 1}, closingflags={'Mother': 2}, changeflags={'Mother': 1},
           cost=[['Fate', -45, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 2/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 2}, closingflags={'Mother': 3}, changeflags={'Mother': 1},
           cost=[['Fate', -20, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 3/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 3}, closingflags={'Mother': 4}, changeflags={'Mother': 1},
           cost=[['Fate', -25, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 4/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 4}, closingflags={'Mother': 5}, changeflags={'Mother': 1,'Enter the village':1},
           cost=[['Fate', -30, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 5/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 5}, closingflags={'Mother': 6}, changeflags={'Mother': 1},
           cost=[['Weeds', -5, 0, 0]], complete=[['max', 'Weeds', 10, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 6/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 6}, closingflags={'Mother': 7}, changeflags={'Mother': 1},
           cost=[['Herbs', -1, 0, 0]], complete=[['max', 'Herbs', 3, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 7/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 7}, closingflags={'Mother': 8}, changeflags={'Mother': 1},
           cost=[['Herbs', -4, 0, 0]], complete=[['max', 'Herbs', 3, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 8/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 8}, closingflags={'Mother': 9}, changeflags={'Mother': 1},
           cost=[['Herbs', -7, 0, 0]], complete=[['max', 'Herbs', 3, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 9/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 9}, closingflags={'Mother': 10}, changeflags={'Mother': 1},
           cost=[['Herbs', -10, 0, 0]],
           complete=[['stat', 'hp', 5, 0, 0], ['stat', 'patk', 5, 0, 0], ['stat', 'pdef', 5, 0, 0],
                     ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Mother 10/10',
           location=['Village', 'Home'],
           unlockflags={'Mother': 10}, closingflags={'Mother': 11}, changeflags={'Mother': 1},
           cost=[['Fate', -40, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
           )
def fatherquestline(parent):
    from initialization_elements import Quests
    Quests(parent=parent, name='Talk to Father 1/12',isvisible=True,
           location=['Village', 'Home'],
           unlockflags={'Father': 0}, closingflags={'Father': 1}, changeflags={'Father': 1, 'Popup': 2},
           cost=[['Fate', -5, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]]
           )
    Quests(parent=parent, name='Talk to Father 2/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 1}, closingflags={'Father': 2}, changeflags={'Father': 1, 'Popup': 3},
           cost=[['Fate', -10, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]]
           )
    Quests(parent=parent, name='Talk to Father 3/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 2}, closingflags={'Father': 3}, changeflags={'Father': 1},
           cost=[['Wood', -1, 0, 0]], complete=[['max', 'Wood', 2, 0, 0]]
           )
    Quests(parent=parent, name='Talk to Father 4/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 3}, closingflags={'Father': 4}, changeflags={'Father': 1},
           cost=[['Wood', -3, 0, 0]], complete=[['max', 'Wood', 2, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 5/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 4}, closingflags={'Father': 5}, changeflags={'Father': 1},
           cost=[['Wood', -5, 0, 0]], complete=[['max', 'Wood', 2, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 6/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 5}, closingflags={'Father': 6}, changeflags={'Father': 1},
           cost=[['Wood', -7, 0, 0]], complete=[['max', 'Wood', 3, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 7/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 6}, closingflags={'Father': 7}, changeflags={'Father': 1, 'Popup': 4},
           cost=[['Wood', -10, 0, 0]], complete=[['max', 'Fate', 5, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 8/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 7}, closingflags={'Father': 8}, changeflags={'Father': 1, 'Popup': 5},
           cost=[['Strength gems', -1, 0, 0]], complete=[['max', 'Strength gems', 19, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 9/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 8}, closingflags={'Father': 9}, changeflags={'Father': 1},
           cost=[['Magic gems', -1, 0, 0]], complete=[['max', 'Magical gems', 19, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 10/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 9}, closingflags={'Father': 10}, changeflags={'Father': 1},
           cost=[['Special gems', -1, 0, 0]], complete=[['max', 'Special gems', 19, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 11/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 10}, closingflags={'Father': 11}, changeflags={'Father': 1},
           cost=[['Fate', -20, 0, 0]], complete=[['max', 'Fate', 10, 0, 0]],
           )
    Quests(parent=parent, name='Talk to Father 12/12',
           location=['Village', 'Home'],
           unlockflags={'Father': 11}, closingflags={'Father': 12}, changeflags={'Father': 1,'Popup':6},
           cost=[['Fate', -35, 0, 0]],
           complete=[['max', 'Fate', 10, 0, 0], ['stat', 'hp', 5, 0, 0], ['stat', 'patk', 5, 0, 0],
                     ['stat', 'pdef', 5, 0, 0],
                     ['stat', 'matk', 5, 0, 0], ['stat', 'mdef', 5, 0, 0]],
           )

def testquest(parent):
    from initialization_elements import Quests
    pass