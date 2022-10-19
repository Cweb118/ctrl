from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict as bk
#[user_snowflake (must be a registered player), starting_loc, alleigance, inventory_kit]
#TODO: Needs to be updated for game 0 balance

g0_character_kits = {
    #Ginger_Walnut, Military
    161520114657656832:[161520114657656832, 1, 'The Core', 'Barheim',
     {'resources':{'Food':10,'Water':10,'Vessel':1},
      'stats':{'Influence':3},
      'units':[['Barheim','Guardian'],['Barheim','Guardian'],['Barheim','Guardian'],['Barheim','Guardian']],
      'buildings':[]}],

    #Cart, Econ (ALERGIC TO ROBOTS)
    160020690051792898:[160020690051792898, 2, 'The Core', 'Barheim',
     {'resources':{'Food':10,'Water':10,'Vessel':1},
      'stats':{'Influence':3},
      'units':[['Barheim','Engineer'],['Barheim','Engineer']],
      'buildings':[bk['kardiahorologist'],bk['mechanized_excavator'],bk['metal_refinery']]}],
}




g0_casting_components = {
            'intro':"You find yourselves at a crossroads, a pivotal moment in Aporia's history. Two factions, traditionally isolationists, seek each other out in times of need.",
            'locations':{
                'Yavar':'Your home is in the Dominion of Yavar, a tranquil place on the western coast where the Yavari people have lived for centuries.',
                'The Core':'Your home is in the City of Baraheim, a thriving refuge for your people and the global capital of industry and innovation.',
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

"""
Unit Actions:
Survey (Architect): Submits a request for a building type to control. Unit ought to have non-zero endurance. Unit ought to have at least half of that buildings working requirements as certs. Requests are processed during the night phase.
Overclock (Automata): Unit consumes 3 steam for a boost in Endurance equal to their cap.
Harmonize (Yavari): Pass your current effects to another unit (consumes all End)
Explore (Pathfinder): Submits a directional exploration request to control.
Scout (Scout): Scouts a location, requires 2 End
Inspire (Barheim): Charges Industrialist unit (not relevant to this playtest)
Transport (Various): Links two buildings together, routing the output of one into the input of the other.

Unit Passives:
Sentry (Sentry): Gets a report on adj districts (needs full End)
Recon (Recon Units): Provides access to chat if units are present
Overtime (Barheim): Works two slots in a building instead of one
Inorganic (Automata): Does not have upkeep
Harmony (Harmonist): Protects unit from defense loss at upkeep (known bug: triggers twice)
"""


character_kits_dict = g0_character_kits
character_briefs_dict = g0_casting_components
