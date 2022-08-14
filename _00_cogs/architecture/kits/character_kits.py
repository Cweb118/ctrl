from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict as bk
#[user_snowflake (must be a registered player), starting_loc, alleigance, inventory_kit]
#TODO: Needs to be updated for game 0 balance

g0_character_kits = {
    #The Cartographer (me)
    160020690051792898:[160020690051792898, 0, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10,'Wood':10,'Metal':10},
      'units':[['Yavari','Laborer'],['Yavari','Laborer'],['Yavari','Laborer'],['Yavari','Laborer']],
      'buildings':[bk['mother_tree'],bk['bountiful_field'],bk['kinetika_trolly']]}],

    #Cody, Uranu
    155172173089210368:[155172173089210368, 0, 'Yavar', 'Uranu',
     {'resources':{'Food':10,'Water':10,'Wood':10},
      'units':[['Yavari','Pathfinder'],['Yavari','Laborer'],['Yavari','Laborer'],['Yavari','Laborer'],['Yavari','Courier']],
      'buildings':[bk['mother_tree'],bk['bountiful_field'],bk['harmonist_scout_guild']]}],

    #Dan, Xinn
    90231355677364224:[90231355677364224, 0, 'Yavar', 'Xinn',
     {'resources':{'Food':10,'Water':10,'Wood':10},
      'units':[['Yavari','Pathfinder'],['Yavari','Laborer'],['Yavari','Laborer'],['Yavari','Laborer'],['Yavari','Courier']],
      'buildings':[bk['mother_tree'],bk['bountiful_field'],bk['harmonist_scout_guild']]}],




    #Ginger_Walnut, Military
    161520114657656832:[161520114657656832, 1, 'The Core', 'Barheim',
     {'resources':{'Food':10,'Water':10,'Vessel':1},
      'stats':{'Influence':3},
      'units':[['Barheim','Guardian'],['Barheim','Guardian'],['Barheim','Guardian'],['Barheim','Guardian']],
      'buildings':[]}],

    #Tiat, Econ (ALERGIC TO ROBOTS)
    162034951615676416:[162034951615676416, 2, 'The Core', 'Barheim',
     {'resources':{'Food':10,'Water':10,'Vessel':1},
      'stats':{'Influence':3},
      'units':[['Barheim','Engineer'],['Barheim','Engineer']],
      'buildings':[bk['kardiahorologist'],bk['mechanized_excavator'],bk['metal_refinery']]}],
    #Bam, Econ 2
    644696938901405696:[644696938901405696, 3, 'The Core', 'Barheim',
     {'resources':{'Metal':10,'Water':10,'Vessel':1},
      'stats':{'Influence':4},
      'units':[['Automata','Engineer'],['Automata','Worker'],['Automata','Worker'],['Automata','Worker']],
      'buildings':[bk['kinetika_trolly'],bk['kinetika_trolly'],bk['kinetika_trolly']]}],

    #Tong, Recon
    163310421132967936:[163310421132967936, 4, 'The Core', 'Barheim',
     {'resources':{'Steam':6,'Metal':5,'Water':10,'Vessel':1},
      'stats':{'Influence':2},
      'units':[['Automata','Pathfinder'],['Automata','Scout']],
      'buildings':[bk['steam_boiler'],bk['steam_boiler']]}],



    #Pairjax, Econ
    169961433625264128:[169961433625264128, 5, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'stats':{'Influence':4},
      'units':[['Yavari','Courier'],['Yavari','Worker'],['Yavari','Laborer'],['Yavari','Laborer']],
      'buildings':[bk['mother_tree'],bk['bountiful_field']]}],

    #jamspinnle, Military
    143574434874130432:[143574434874130432, 6, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'stats':{'Influence':3},
      'units':[['Yavari','Ranger'],['Yavari','Ranger'],['Xinn','Laborer']],
      'buildings':[bk['living_briar']]}],

    #Orlando, Recon
    143467854358904832:[143467854358904832, 7, 'Yavar', 'Yavari',
     {'resources':{'Food':10,'Water':10},
      'stats':{'Influence':2},
      'units':[['Loyavasi','Pathfinder'],['Loyavasi','Scout'],['Loyavasi','Engineer']],
      'buildings':[]}],
}




g0_casting_components = {
            'intro':"You find yourselves at a crossroads, a pivotal moment in Aporia's history. Two factions, traditionally isolationists, seek each other out in times of need.",
            'locations':{
                'Yavar':'Your home is in the Dominion of Yavar, a tranquil place on the western coast where the Yavari people have lived for centuries.',
                'Barheim':'Your home is in the City of Baraheim, a thriving refuge for your people and the global capital of industry and innovation.',
            },
            'factions':{
                'Yavari':'You have heard tales of great inovation in the City of Baraheim, the likes of which will change the world. You have decided it most prudent to reach out to the northern historically known isolationists to attempt to reach a trade deal for some of their breakthroughs.',
                'Baraheim':'Your breakthrough has catapulted your civilization into a new age, but has come at a cost. Your means of collecting water have dried up, resulting in a deadly drought. You decide it best to set out to the south to find the Yavari people who have such resources in plenty.',
            },
            'characters':{
                1:'You are a military leader of the city, provided with resources that have primarily been used to defend your mountain. In these desparate times you may need to send them out into the wilds to defend your exploration attempts.',
                2:'You are an engineering expert of the city, working towards a refined production line. In these recent times there has been a push to use Automata. While you persionally find this abhorrent, as nothing could beat natural Baraheimian intellect and precision, you are trying to bring yourself into the new age.',
                3:'You are an engineering expert of the city, working towards a refined production line. You have with you resources designed to refine your automation process, including several Automata which do not need food or water. These will prove invaluable in these desperate times.',
                4:'You are a reconnaissance leader of the city, responsible for finding a trade route to Yavar. They are located to the south of you at the western shores, and you should try to make contact as soon as possible.',

                5:'You are a military leader of the dominion. Your small troop of Rangers have historically been for defence, but you may find it prudent to escort scouts traveling north.',
                6:'You are a commerce director of the dominion. You are responsible for overseeing the production of food and water in the city.',
                7:'You are a reconnaissance leader of the dominion, responsible for finding a trade route to Baraheim. Theya re located to the north of you in the eponymous mountain of Baraheim, and you should try to make contact as soon as possible. '
            },
            'outro':'Good luck!',
}

character_kits_dict = g0_character_kits
character_briefs_dict = g0_casting_components
