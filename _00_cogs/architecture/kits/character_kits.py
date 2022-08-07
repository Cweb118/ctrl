from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict as bk
#[user_snowflake (must be a registered player), starting_loc, alleigance, inventory_kit]
#TODO: Needs to be updated for game 0 balance

g0_character_kits = {
    #The Cartographer (me)
    160020690051792898:[160020690051792898, 1, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'units':[['Yavari','Worker'],['Yavari','Architect']],
      'buildings':[bk['harmonist_scout_guild'],bk['mother_tree']]}],

    #jamspinnle
    143574434874130432:[143574434874130432, 1, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'units':[['Loyavasi','Scout'],['Loyavasi','Scout']],
      'buildings':[]}],

    'snowflake3':['snowflake', 3, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'units':[['Xinn','Scout'],['Xinn','Scout']],
      'buildings':[]}],

    #Pairjax
    169961433625264128:[169961433625264128, 1, 'The Threshold', 'Barheim',
     {'resources':{'Food':10,'Water':10},
      'units':[['Barheim','Scout'],['Barheim','Scout']],
      'buildings':[]}],

    'snowflake5':['snowflake', 5, 'Barheim', 'Barheim',
     {'resources':{'Food':10,'Water':10},
      'units':[['Automata','Worker'],['Automata','Scout']],
      'buildings':[]}],

    'snowflake6':['snowflake', 6, 'Barheim', 'Barheim',
     {'resources':{'Food':10,'Water':10},
      'units':[['Eelaki','Worker'],['Eelaki','Engineer']],
      'buildings':[]}],
}

g0_casting_components = {
            'intro':'This is the part everyone gets to know',
            'locations':{
                'Yavar':'And ye who are in Yavar get to know this',
            },
            'factions':{
                'Yavari':'And ye who are part of the Yavari faction obtain the faction knowledge',
            },
            'characters':{
                1:'And finally, ye who are in the middle of all of this, get the secret wisdom'
            },
            'outro':'Good luck!',
}

character_kits_dict = g0_character_kits
character_briefs_dict = g0_casting_components
