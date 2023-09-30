def createpokemonlist(parent):
    from initialization_elements import Pokemon
    pokemonlist = [
        Pokemon(
            10, 0, 0, 0, 0, 10, 0, 10, 10, 10, 10,
            drop={"exp": 1, "resources": [["Physical gems", 1, 10], ["Magical gems", 1, 10], ["Special gems", 1, 10]]},
            skill=["Silently judge", 0, 2, "Phys"], name="Training dummy", parent=parent, elementlist=parent.pokemonlist
        ),

        Pokemon(
            80, 80, 80, 80, 80, 10, 0, 10, 10, 10, 10,
            drop={"exp": 2, "resources": [["Butterfly wings", 1, 30], ["Physical gems", 1, 10], ["Magical gems", 1, 10],
                                          ["Special gems", 1, 10]]},
            name="Butterfly", parent=parent, elementlist=parent.pokemonlist
        ),
        Pokemon(
            91.2, 100.8, 91.2, 96, 100.8, 12, 0, 12, 12, 12, 12,
            drop={"exp": 2, "resources": [["Frog legs", 1, 10], ["Physical gems", 1, 10], ["Magical gems", 1, 10]
                , ["Special gems", 1, 10]]},
            name="Frog", parent=parent, elementlist=parent.pokemonlist, skill=["Jump attack", 6, 2.3, "Phys"]
        ),
        Pokemon(
            150, 105, 126, 105, 114, 15, 0, 15, 15, 15, 15,
            drop={"exp": 3, "resources": [["Physical gems", 1, 10], ["Magical gems", 1, 10], ["Special gems", 1, 10]]},
            name="Worm", parent=parent, elementlist=parent.pokemonlist, skill=["Roll over", 8, 2.4, "Phys"]
        ),
        Pokemon(
            133, 171, 144.4, 152, 159.6, 19, 0, 19, 19, 19, 19,
            drop={"exp": 3,
                  "resources": [["Cow hide", 1, 10], ["Beef", 1, 10], ["Physical gems", 1, 10], ["Magical gems", 1, 10],
                                ["Special gems", 1, 10]]},
            name="Cow", parent=parent, elementlist=parent.pokemonlist, skill=["Rear kick", 5, 2, "Phys"]
        ),
        Pokemon(
            187.2, 211.2, 172.8, 201.6, 187.2, 24, 0, 24, 24, 24, 24,
            drop={"exp": 4, "resources": [["Snake skin", 1, 10], ["Physical gems", 1, 10], ["Magical gems", 1, 10],
                                          ["Special gems", 1, 10]]},
            name="Snake", parent=parent, elementlist=parent.pokemonlist, skill=["Squeeze", 9, 2.8, "Phys"]
        ),
        Pokemon(
            1200, 200, 200, 200, 200, 30, 0, 30, 30, 30, 30,
            drop={"exp": 5, "resources": [["Physical gems", 1, 10], ["Magical gems", 1, 10], ["Special gems", 1, 10]]},
            name="Snake", parent=parent, elementlist=parent.pokemonlist, skill=["Azura blow", 13, 3.5, "Phys"]
        )
    ]

    return pokemonlist
