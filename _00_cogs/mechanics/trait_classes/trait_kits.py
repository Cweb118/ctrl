from _00_cogs.mechanics.trait_classes.trait_classes import *

trait_kits_dict = {

    # 'TraitName':{
    #     'title':'TITLE',
    #     'description':'DESC',
    #     'type':'TYPE',
    #     'certs':'CERTS',
    #     'skillsets':'SKILLSET_LIST',
    #     'inv_args':'INV_ARGS_DICT',
    #     'play_cost':'PLAY_COST_DICT',
    #     'stats':'STATS_DICT',
    #     'upkeep':'UPKEEP_DICT',
    #     'die_set':'DIE_SET_LIST'
    # },


    # races

    'Aratori': {
        'title': 'Aratori',
        'description': 'A mighty race of great strength, the Aratori have built an empire to last the test of time.',
        'type': 'race',
        'certs': None,
        'skillsets': [Aratori()],
        'inv_args': {'cap': {'resource': 3}, 'cont': 1},
        'play_cost': None,
        'stats': {'Attack': 1, 'Fortitude': 2},
        'upkeep': {'Food': 1},
        'die_set': ['1d7']
    },

    'Barheim': {
        'title': 'Barheim',
        'description': 'A race of Engineers, their hearts are said to be as hard and cold as their flesh.',
        'type': 'race',
        'certs': ['Engineer'],
        'skillsets': [Barheim()],
        'inv_args': {'cont': 2},
        'play_cost': None,
        'stats': {'Defense': 2, 'Initiative': -1},
        'upkeep': None,
        'die_set': ['1d4']
    },

    'Automata': {
        'title': 'Automata',
        'description': 'A creation of the Barheim, the Automata can brave dangers no man should face.',
        'type': 'race',
        'certs': ['Inorganic'],
        'skillsets': [Automata()],
        'inv_args': {'cont': 1},
        'play_cost': None,
        'stats': {'Health': 1, 'Defense': 2},
        'upkeep': {'Food': -10, 'Water': -10},
        'die_set': ['2d4']
    },

    'Eelaki': {
        'title': 'Eelaki',
        'description': 'Natural engineers, the Eelaki are strong kin with the Tevaru, whose chitinous suits they designed.',
        'type': 'race',
        'certs': ['Engineer'],
        'skillsets': [Eelaki()],
        'inv_args': None,
        'play_cost': None,
        'stats': {'Endurance': -1, 'Initiative': -2, 'Taunt': -1},
        'upkeep': None,
        'die_set': ['2d3']
    },

    'Loyavasi': {
        'title': 'Loyavasi',
        'description': 'A hoofed people from the mountains, the Loyavasi never sit still for long.',
        'type': 'race',
        'certs': None,
        'skillsets': [Loyavasi(), Gatherer()],
        'inv_args': {'cap': {'resource': 2}},
        'play_cost': None,
        'stats': {'Initiative': -1},
        'upkeep': None,
        'die_set': ['1d6', '1d2']
    },

    'Otavan': {
        'title': 'Otavan',
        'description': 'Descendants of Aratori colonists, these who have made their lives in the countryside have learned to subvert strength with subterfuge.',
        'type': 'race',
        'certs': None,
        'skillsets': [Otavan(), Colonist()],
        'inv_args': None,
        'play_cost': None,
        'stats': {'Taunt': -2},
        'upkeep': None,
        'die_set': ['1d6']
    },
    'Prismari': {
        'title': 'Prismari',
        'description': 'A regal race of birds who move quite fast for their size.',
        'type': 'race',
        'certs': ['Transporter'],
        'skillsets': [Prismari(), Transport()],
        'inv_args': None,
        'play_cost': None,
        'stats': {'Health': 1, 'Endurance': 1},
        'upkeep': {'Water': 1},
        'die_set': ['1d5']
    },

    'Rivenborne': {
        'title': 'Rivenborne',
        'description': 'A mysterious race, the Rivenborne seek to claim their self-proclaimed birthright as rules of Aporia.',
        'type': 'race',
        'certs': ['Inorganic'],
        'skillsets': [Rivenborne()],
        'inv_args': None,
        'play_cost': None,
        'stats': {'Health': 1},
        'upkeep': None,
        'die_set': ['1d4', '1d8']
    },

    'Tevaru': {
        'title': 'Tevaru',
        'description': 'The Tevaru are aliens to the surface world, but despite the dangerous environment they feel more welcomed here.',
        'type': 'race',
        'certs': ['Aquatic'],
        'skillsets': [Tevaru()],
        'inv_args': {'cap': {'resource': 4, 'unit': 1}, 'cont': 2},
        'play_cost': None,
        'stats': {'Health': 2, 'Defense': 1, 'Fortitude': -1, 'Initiative': 1, 'Taunt': 1},
        'upkeep': {'Water': 3},
        'die_set': ['1d3']
    },

    'Xinn': {
        'title': 'Xinn',
        'description': 'An brutal race of bipedal bovines, what the Xinn lack in intellect they more than make up for in raw strength.',
        'type': 'race',
        'certs': ['Laborer'],
        'skillsets': [Xinn()],
        'inv_args': {'cap': {'resource': 4}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 3, 'Health': 1, 'Fortitude': 3, 'Taunt': 2},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d10']
    },

    'Yavari': {
        'title': 'Yavari',
        'description': 'A race hunters in tune with nature, the Yavari fight to preserve the natural order.',
        'type': 'race',
        'certs': ['Harmonist'],
        'skillsets': [Yavari()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': ['1d6']
    },


    # classes

    'Worker': {
        'title': 'Worker',
        'description': '*And let the works of a craftsman satiate their hunger. -The Book of The Patron 5:3*',
        'type': 'class',
        'certs': ['Worker'],
        'skillsets': None,
        'inv_args': {'cap': {'resource': 3}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 1, 'Defense': 6, 'Endurance': 1, 'Fortitude': 4, 'Initiative': 10, 'Taunt': -10},
        'upkeep': {'Food': 2, 'Water': 1},
        'die_set': ['1d6']
    },

    'Laborer': {
        'title': 'Laborer',
        'description': "*Let no man's bounty exceed the sweat of their brow -The Book of The Patron 5:2*",
        'type': 'class',
        'certs': ['Worker', 'Laborer'],
        'skillsets': None,
        'inv_args': {'cap': {'resource': 3}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 1, 'Defense': 6, 'Endurance': 1, 'Fortitude': 5, 'Initiative': 10, 'Taunt': -10},
        'upkeep': {'Food': 1, 'Water': 2},
        'die_set': ['1d7']
    },

    'Engineer': {
        'title': 'Engineer',
        'description': '*The dullest wit would put even the sharpest blade to shame. -Barheimian Proverb*',
        'type': 'class',
        'certs': ['Worker', 'Engineer'],
        'skillsets': None,
        'inv_args': {'cap': {'resource': 2}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 1, 'Defense': 6, 'Endurance': 1, 'Fortitude': 3, 'Initiative': 10, 'Taunt': -10},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d5']
    },

    'Courier': {
        'title': 'Courier',
        'description': '*May your feet be swift, and your loads light! - A parting adage among Couriers*',
        'type': 'class',
        'certs': ['Transporter'],
        'skillsets': [Transport()],
        'inv_args': {'cap': {'resource': 2}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 1, 'Defense': 6, 'Endurance': 2, 'Fortitude': 3, 'Initiative': 10, 'Taunt': -10},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d6']
    },

    'Caravan': {
        'title': 'Caravan',
        'description': '*Safety in numbers... - An old adage*',
        'type': 'class',
        'certs': ['Transporter'],
        'skillsets': [Transport()],
        'inv_args': {'cap': {'resource': 15}, 'cont': 6},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 2, 'Defense': 8, 'Endurance': 3, 'Fortitude': 3, 'Initiative': 10, 'Taunt': -10},
        'upkeep': {'Wood': 1, 'Stone': 1},
        'die_set': ['1d6']
    },

    'Architect': {
        'title': 'Architect',
        'description': '*We walk in the very footsteps of the gods. -Unknown Scribe (likely an Architect)*',
        'type': 'class',
        'certs': ['Architect'],
        'skillsets': [Architect()],
        'inv_args': {'cap': {'resource': 2, 'building':3}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 1, 'Defense': 6, 'Endurance': 1, 'Fortitude': 3, 'Initiative': 10, 'Taunt': -10},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d6']
    },

    'Pathfinder': {
        'title': 'Pathfinder',
        'description': '*Should you seek after Her own heart, given an eternity, you will find Her. - Unknown Scribe*',
        'type': 'class',
        'certs': ['Recon'],
        'skillsets': [Pathfinder(), Recon()],
        'inv_args': {'cap': {'resource': 6}, 'cont': 3},
        'play_cost': None,
        'stats': {'Attack': 1, 'Health': 2, 'Defense': 7, 'Endurance': 3, 'Fortitude': 5, 'Initiative': 3, 'Taunt': -4},
        'upkeep': {'Food': 2, 'Water': 1},
        'die_set': ['1d7']
    },

    'Scout': {
        'title': 'Scout',
        'description': '*Think of it this way, the more time we spend out roaming the wilds, the less we spend tilling fields. -Unknown Scout*',
        'type': 'class',
        'certs': ['Recon'],
        'skillsets': [Scout(), Recon()],
        'inv_args': {'cap': {'resource': 6}, 'cont': 3},
        'play_cost': None,
        'stats': {'Attack': 1, 'Health': 2, 'Defense': 8, 'Endurance': 3, 'Fortitude': 3, 'Initiative': 5, 'Taunt': -5},
        'upkeep': {'Food': 1, 'Water': 2},
        'die_set': ['1d6']
    },

    'Sentry': {
        'title': 'Sentry',
        'description': '*Nothing remains unseen under a watchful eye. -An adage among Sentries *',
        'type': 'class',
        'certs': ['Recon'],
        'skillsets': [Sentry(), Recon()],
        'inv_args': {'cap': {'resource': 5}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 1, 'Health': 3, 'Defense': 9, 'Endurance': 2, 'Fortitude': 2, 'Initiative': 2, 'Taunt': 1},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d5']
    },

    'Warrior': {
        'title': 'Warrior',
        'description': '*None shall remain. - A quote attributed to The Harbinger*',
        'type': 'class',
        'certs': ['Combat'],
        'skillsets': [Warrior()],
        'inv_args': {'cap': {'resource': 4}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 2, 'Health': 2, 'Defense': 10, 'Endurance': 2, 'Fortitude': 3, 'Initiative': 0, 'Taunt': 0},
        'upkeep': {'Food': 2, 'Water': 1},
        'die_set': ['1d6']
    },

    'Ranger': {
        'title': 'Ranger',
        'description': '*A sword should never touch they who are of nimble mind. - Yavari Proverb*',
        'type': 'class',
        'certs': ['Combat'],
        'skillsets': [Ranger()],
        'inv_args': {'cap': {'resource': 3}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 2, 'Health': 1, 'Defense': 8, 'Endurance': 2, 'Fortitude': 4, 'Initiative': -1, 'Taunt': -1},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d8']
    },

    'Guardian': {
        'title': 'Guardian',
        'description': '*As I have cared for you, so ought you care for one another. - The Matriarch*',
        'type': 'class',
        'certs': ['Combat'],
        'skillsets': [Guardian()],
        'inv_args': {'cap': {'resource': 6}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 1, 'Health': 3, 'Defense': 12, 'Endurance': 2, 'Fortitude': 1, 'Initiative': 2, 'Taunt': 3},
        'upkeep': {'Food': 3, 'Water': 1},
        'die_set': ['1d4']
    },

    'Witch': {
        'title': 'Witch',
        'description': '*[concerning, incoherent whispering] -???*',
        'type': 'class',
        'certs': ['Combat', 'Arkanist'],
        'skillsets': [Witch()],
        'inv_args': {'cap': {'resource': 2}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 2, 'Defense': 7, 'Endurance': 2, 'Fortitude': 1, 'Initiative': -2, 'Taunt': -2},
        'upkeep': {'Food': 1, 'Water': 1},
        'die_set': ['1d5']
    },

    'Knight': {
        'title': 'Knight',
        'description': '*Let the stalwart of us take up arms, that the weak may live as the brave. -Keive, Aratori Hero*',
        'type': 'class',
        'certs': ['Combat', 'Arkanist'],
        'skillsets': [Knight()],
        'inv_args': {'cap': {'resource': 4}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 3, 'Health': 3, 'Defense': 10, 'Endurance': 2, 'Fortitude': 4, 'Initiative': 0, 'Taunt': 1},
        'upkeep': {'Food': 2, 'Water': 2},
        'die_set': ['1d5', '1d7']
    },

    'Alchemist': {
        'title': 'Alchemist',
        'description': '*We stand on the cusp of a new magic- what a time to walk Aporia! - Jarrio, Great Aratori Engineer*',
        'type': 'class',
        'certs': ['Combat', 'Industrialist', 'Engineer'],
        'skillsets': [Alchemist()],
        'inv_args': {'cap': {'resource': 5}, 'cont': 4},
        'play_cost': None,
        'stats': {'Attack': 1, 'Health': 1, 'Defense': 8, 'Endurance': 3, 'Fortitude': 1, 'Initiative': 0, 'Taunt': -1},
        'upkeep': {'Food': 1, 'Water': 3},
        'die_set': ['1d4']
    },

    'Technophant': {
        'title': 'Technophant',
        'description': '*And now we walk the path of They who ended all things.* - [Unknown], HIVE Progenitor*',
        'type': 'class',
        'certs': ['Combat', 'Atomikist'],
        'skillsets': [Technophant()],
        'inv_args': {'cap': {'resource': 6}, 'cont': 2},
        'play_cost': None,
        'stats': {'Attack': 0, 'Health': 5, 'Defense': 10, 'Endurance': 2, 'Fortitude': 0, 'Initiative': 4, 'Taunt': 0},
        'upkeep': {'Water': 3, 'Metal': 1},
        'die_set': ['1d5']
    },


    # effects

    'Harmony': {
        'title': 'Harmony',
        'description': 'One who is attuned to the Melding.',
        'type': 'effect',
        'certs': ['Harmony'],
        'skillsets': [Harmony()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Charged': {
        'title': 'Charged',
        'description': 'One who is empowered by a greater force...',
        'type': 'effect',
        'certs': None,
        'skillsets': [Charged()],
        'inv_args': None,
        'play_cost': None,
        'stats': {'Health': 1, 'Fortitude': -1},
        'upkeep': None,
        'die_set': None
    },

    'Good Morale': {
        'title': 'Good Morale',
        'description': 'One of joyful spirit!',
        'type': 'effect',
        'certs': None,
        'skillsets': [Morale()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },


    # building logic

    'Mend': {
        'title': 'Mend',
        'description': 'MEND_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Mend()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Upkeep': {
        'title': 'Upkeep',
        'description': 'UPKP_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Upkeep()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Speed': {
        'title': 'Speed',
        'description': 'SPD_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Speed()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Sacrifice': {
        'title': 'Sacrifice',
        'description': 'SCF_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Sacrifice()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Defense': {
        'title': 'Defense',
        'description': 'DEF_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Defense()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Ward': {
        'title': 'Ward',
        'description': 'WARD_DESC',
        'type': 'building_logic',
        'certs': ['Recon'],
        'skillsets': [Ward()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Train': {
        'title': 'Train',
        'description': 'TRAIN_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Train()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Mentor': {
        'title': 'Mentor',
        'description': 'MTR_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Mentor()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Worker Boon': {
        'title': 'Worker Boon',
        'description': 'WB_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [WorkerBoon()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'District Boon': {
        'title': 'District Boon',
        'description': 'DB_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [DistrictBoon()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

    'Transport': {
        'title': 'Transport',
        'description': 'CARRY_DESC',
        'type': 'building_logic',
        'certs': None,
        'skillsets': [Transport()],
        'inv_args': None,
        'play_cost': None,
        'stats': None,
        'upkeep': None,
        'die_set': None
    },

}
