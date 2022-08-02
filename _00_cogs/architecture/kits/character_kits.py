from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict as bk
#[user_snowflake (must be a registered player), starting_loc, alleigance, inventory_kit]
#TODO: Needs to be updated for game 0 balance

g0 = {
    #The Cartographer (me)
    160020690051792898:[160020690051792898, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'units':[['Yavari','Worker'],['Yavari','Worker']],
      'buildings':[bk['harmonist_scout_guild'],bk['mother_tree']]}],

    'snowflake2':['snowflake', 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'units':[['Loyavasi','Scout'],['Loyavasi','Scout']],
      'buildings':[]}],

    'snowflake3':['snowflake', 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'units':[['Xinn','Scout'],['Xinn','Scout']],
      'buildings':[]}],

    'snowflake4':['snowflake', 'Barheim', 'Barheim',
     {'resources':{'Food':10,'Water':10},
      'units':[['Barheim','Worker'],['Barheim','Worker']],
      'buildings':[]}],

    'snowflake5':['snowflake', 'Barheim', 'Barheim',
     {'resources':{'Food':10,'Water':10},
      'units':[['Automata','Worker'],['Automata','Scout']],
      'buildings':[]}],

    'snowflake6':['snowflake', 'Barheim', 'Barheim',
     {'resources':{'Food':10,'Water':10},
      'units':[['Eelaki','Worker'],['Eelaki','Engineer']],
      'buildings':[]}],
}




character_kits_dict = g0
