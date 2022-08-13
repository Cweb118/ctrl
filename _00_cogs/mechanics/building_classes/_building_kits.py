building_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    #'template': ['title', 'description', 'inv_args', 'traits', 'play_cost', 'stats', 'workers_dict', 'input_dict', 'output_dict', 'cat_dict'],

    #owner, title, description, inv_args, traits, logic_args, play_cost, stats, worker_req, input_dict, output_dict, cat_dict):





    # Village:

    'woodland_ranger_barracks':{
        'title':'Woodland Ranger Barracks',
        'description':'A training grounds for Rangers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Ranger'],
        'play_cost': {'Wood':3},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':None,
        'input_dict':{'Woodland Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'woodland_scout_guild':{
        'title':'Woodland Scouting Guild',
        'description':'A training grounds for Scouts',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Scout'],
        'play_cost': {'Wood':2},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':None,
        'input_dict':{'Woodland Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'woodland_sentry_guild':{
        'title':'Woodland Sentry Guild',
        'description':'A training grounds for Sentries',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Sentry'],
        'play_cost': {'Wood':2},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':None,
        'input_dict':{'Woodland Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'woodland_laborer_guild':{
        'title':'Woodland Labor Guild',
        'description':'A training grounds for Laborers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Laborer'],
        'play_cost': {'Wood':2},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':None,
        'input_dict':{'Woodland Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'woodland_courier_guild':{
        'title':'Woodland Courier Guild',
        'description':'A training grounds for Couriers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Courier'],
        'play_cost': {'Wood':3},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':None,
        'input_dict':{'Woodland Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'woodland_architect_guild':{
        'title':'Woodland Architect Guild',
        'description':'A training grounds for Architects',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Architect'],
        'play_cost': {'Wood':3},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':None,
        'input_dict':{'Woodland Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'pub':{
        'title':'Pub',
        'description':'A place to unwind after a long day...',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 2, None, None, 2, None],
        'mechanics': ['Worker Boon'], #aka traits
        'mechanics_args': ['Good Morale'],
        'play_cost': {'Wood':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':None,
        'input_dict':{'Water':1, 'Food':1},
        'output_dict':None,
        'cat_dict':None
    },

    'dam':{
        'title':'Dam',
        'description':'A structure built to create a static supply of water',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[6, 1, None, None, 3, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Wood':4, 'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':3},
        'worker_req':['Laborer'],
        'input_dict':None,
        'output_dict':{'Water':4},
        'cat_dict':None
    },

    'sawmill':{
        'title':'Sawmill',
        'description':'A workshop made for processing trees into lumber',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[3, 1, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Wood':3, 'Stone':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Laborer'],
        'input_dict':None,
        'output_dict':{'Wood':2},
        'cat_dict':None
    },

    'garden':{
        'title':'Garden',
        'description':'A small plot of land for growing basic vegetables',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[5, 2, None, None, 1, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Water':1, 'Stone':1},
        'stats':{'attack':0, 'health':1, 'defense':1, 'size':1},
        'worker_req':['Worker'],
        'input_dict':{'Water':2},
        'output_dict':{'Food':3},
        'cat_dict':None
    },

    'woodshop':{
        'title':'Woodshop',
        'description':'A kind tree who drinks from the deep',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[3, 4, None, None, 1, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Wood':3, 'Stone':2},
        'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
        'worker_req':['Worker'],
        'input_dict':{'Wood':2, 'Stone':1, 'Food':1, 'Water':1,},
        'output_dict':{'Woodland Gear':1},
        'cat_dict':None
    },

    'storehouse':{
        'title':'Storehouse',
        'description':'A large building used for storing resources',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[12, 6, 2, 2, None, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Wood':5, 'Stone':3},
        'stats':{'attack':0, 'health':3, 'defense':2, 'size':3},
        'worker_req':None,
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    # Surivivalist:

    'survivalist_warrior_barracks':{
        'title':'Survivalist Warrior Barracks',
        'description':'A training grounds for Warriors',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Warrior'],
        'play_cost': {'Metal':2},
        'stats':{'attack':0, 'health':4, 'defense':5, 'size':1},
        'worker_req':None,
        'input_dict':{'Survivalist Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'survivalist_pathfinder_guild':{
        'title':'Survivalist Pathfinding Guild',
        'description':'A training grounds for Pathfinders',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Pathfinder'],
        'play_cost': {'Metal':1},
        'stats':{'attack':0, 'health':4, 'defense':5, 'size':1},
        'worker_req':None,
        'input_dict':{'Survivalist Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'survivalist_sentry_guild':{
        'title':'Survivalist Sentry Guild',
        'description':'A training grounds for Sentries',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Sentry'],
        'play_cost': {'Metal':1},
        'stats':{'attack':0, 'health':4, 'defense':5, 'size':1},
        'worker_req':None,
        'input_dict':{'Survivalist Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'survivalist_laborer_guild':{
        'title':'Survivalist Labor Guild',
        'description':'A training grounds for Laborers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Laborer'],
        'play_cost': {'Metal':1},
        'stats':{'attack':0, 'health':4, 'defense':5, 'size':1},
        'worker_req':None,
        'input_dict':{'Survivalist Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'survivalist_courier_guild':{
        'title':'Survivalist Courier Guild',
        'description':'A training grounds for Couriers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Courier'],
        'play_cost': {'Metal':2},
        'stats':{'attack':0, 'health':4, 'defense':5, 'size':1},
        'worker_req':None,
        'input_dict':{'Survivalist Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'survivalist_architect_guild':{
        'title':'Survivalist Architect Guild',
        'description':'A training grounds for Architects',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Architect'],
        'play_cost': {'Metal':2},
        'stats':{'attack':0, 'health':4, 'defense':5, 'size':1},
        'worker_req':None,
        'input_dict':{'Survivalist Gear':1},
        'output_dict':None,
        'cat_dict':None
    },

    'quarry':{
        'title':'Quarry',
        'description':'A place hewn out of stone, allowing for easier access',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[3, 1, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': None,
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':2},
        'worker_req':['Laborer'],
        'input_dict':None,
        'output_dict':{'Stone':2},
        'cat_dict':None
    },

    'mine':{
        'title':'Mine',
        'description':'An artificial cave used for gathering valuable minerals',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[3, 2, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Metal':2, 'Stone':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Laborer'],
        'input_dict':None,
        'output_dict':{'Coal':2, 'Ore':1},
        'cat_dict':None
    },

    'traps':{
        'title':'Traps',
        'description':'A series of traps with the intent of catching prey',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[2, 2, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': None,
        'stats':{'attack':0, 'health':1, 'defense':1, 'size':1},
        'worker_req':['Worker'],
        'input_dict':{'Stone':1},
        'output_dict':{'Food':2},
        'cat_dict':{'Metal':1},
    },

    'metal_forge':{
        'title':'Metal Forge',
        'description':'A place dedicated for the refining of ore into metal',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[3, 3, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Metal':1, 'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':4, 'size':1},
        'worker_req':['Worker'],
        'input_dict':{'Ore':2, 'Coal':1},
        'output_dict':{'Metal':2},
        'cat_dict':None
    },

    'blacksmithy':{
        'title':'Blacksmithy',
        'description':'A kind tree who drinks from the deep',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[3, 4, None, None, 1, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Metal':1, 'Stone':2},
        'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
        'worker_req':['Worker'],
        'input_dict':{'Metal':1, 'Stone':2, 'Food':1, 'Water':1,},
        'output_dict':{'Survivalist Gear':1},
        'cat_dict':None
    },

    'warehouse':{
        'title':'Warehouse',
        'description':'A large building used for storing resources',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[18, 4, 3, 3, None, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Metal':5, 'Stone':3},
        'stats':{'attack':0, 'health':5, 'defense':7, 'size':3},
        'worker_req':None,
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },


    #harmony:

    'harmonist_pathfinder_guild':{
        'title':'Harmonist Pathfinding Guild',
        'description':'A training grounds for Pathfinders',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Pathfinder'],
        'play_cost': {'Wood':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Harmonist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'harmonist_scout_guild':{
        'title':'Harmonist Scouting Guild',
        'description':'A training grounds for Scouts',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Scout'],
        'play_cost': {'Wood':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Harmonist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'harmonist_laborer_guild':{
        'title':'Harmonist Labor Guild',
        'description':'A training grounds for Laborers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Laborer'],
        'play_cost': {'Wood':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Harmonist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'mother_tree':{
        'title':'Mother Tree',
        'description':'A kind tree who drinks from the deep',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[4, 1, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Food':3,'Water':2},
        'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
        'worker_req':['Laborer', 'Harmonist'],
        'input_dict':None,
        'output_dict':{'Water':2},
        'cat_dict':None
    },

    'father_tree':{
        'title':'Father Tree',
        'description':'A generous tree who upheaves the earth',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[6, 2, None, None, 3, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Food':4,'Water':2},
        'stats':{'attack':0, 'health':4, 'defense':2, 'size':2},
        'worker_req':['Laborer', 'Harmonist'],
        'input_dict':None,
        'output_dict':{'Stone':3, 'Ore':1},
        'cat_dict':None
    },

    'bountiful_field':{
        'title':'Bountiful Field',
        'description':'A field with grounds ripe for harvesting',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[8, 2, None, None, 2, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Food':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':2},
        'worker_req':['Worker', 'Harmonist'],
        'input_dict':{'Water':2},
        'output_dict':{'Food':4},
        'cat_dict':None
    },

    'towering_forest':{
        'title':'Towering Forest',
        'description':'A forest of towering trees which can be processed into wood',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[12, 2, None, None, 3, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Food':4},
        'stats':{'attack':0, 'health':4, 'defense':2, 'size':3},
        'worker_req':['Worker', 'Harmonist'],
        'input_dict':{'Water':3},
        'output_dict':{'Wood':6},
        'cat_dict':None
    },

    'living_briar':{
        'title':'Living Briar',
        'description':'A vicious briar of thorns which provides security',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, None, None],
        'mechanics': ['Defense'], #aka traits
        'mechanics_args': None,
        'play_cost': {'Food':2},
        'stats':{'attack':0, 'health':6, 'defense':8, 'size':3},
        'worker_req':None,
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'aqueduct':{
        'title':'Aqueduct',
        'description':'A constructed passage through which water can flow',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, None, None],
        'mechanics': ['Transport'], #aka traits
        'mechanics_args': ['Water'],
        'play_cost': {'Wood':2, 'Stone':2},
        'stats':{'attack':0, 'health':1, 'defense':1, 'size':1},
        'worker_req':None,
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'healing_grove':{
        'title':'Healing Grove',
        'description':'A soothing respite that regenerates 2 health of units within',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[2, 2, None, None, 1, None],
        'mechanics': ['Mend'], #aka traits
        'mechanics_args': ['Health', 2],
        'play_cost': {'Food':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':2},
        'worker_req':['Harmonist'],
        'input_dict':{'Water':1, 'Food':1},
        'output_dict':None,
        'cat_dict':None
    },

    #Arcanae

    'wayoftheknight':{
        'title':'Way of the Knight',
        'description':'A training grounds for Knights',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Knight'],
        'play_cost': {'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Arkanist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'wayofthewitch':{
        'title':'Way of the Witch',
        'description':'A training grounds for Witches',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Witch'],
        'play_cost': {'Wood':3, 'Stone':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Arkanist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':{'Vessel':1}
    },

    'wayofthearchitect':{
        'title':'Way of the Architect',
        'description':'A training grounds for Architects',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Architect'],
        'play_cost': {'Wood':2, 'Stone':1},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Arkanist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'wayofthesentry':{
        'title':'Way of the Sentry',
        'description':'A training grounds for Sentries',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Sentry'],
        'play_cost': {'Wood':1, 'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Arkanist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'templeofthelibrarian':{
            'title':'Temple of the Librarian',
            'description':'An alter to the Librarian. May Her wealth of knowledge be a blessing and not a curse.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[None, None, None, None, 1, None],
            'mechanics': ['Train'], #aka traits
            'mechanics_args': ['Arkanist'],
            'play_cost': {'Wood':1, 'Stone':2},
            'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
            'worker_req':['Arkanist'],
            'input_dict':None,
            'output_dict':None,
            'cat_dict':{'Vessel':1}
        },

    'templeoftheharbinger':{
            'title':'Temple of the Harbinger',
            'description':'An alter to the Harbinger. May the old be cleansed that the new may be reborn.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[1, 1, None, None, 1, None],
            'mechanics': ['Sacrifice'], #aka traits
            'mechanics_args': None,
            'play_cost': {'Wood':2,'Stone':3, 'Metal':1},
            'stats':{'attack':0, 'health':4, 'defense':3, 'size':2},
            'worker_req':None,
            'input_dict':None,
            'output_dict':{'Vessel':1},
            'cat_dict':None
        },

    'templeofthebiologist':{
            'title':'Temple of the Biologist',
            'description':'An alter to the Biologist. May the life She has given you be lived to the fullest.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[9, 2, 0, None, 1, None],
            'mechanics': None, #aka traits
            'mechanics_args': None,
            'play_cost': {'Wood':5},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':['Arkanist'],
            'input_dict':{'Food':4},
            'output_dict':{'Food':9},
            'cat_dict':{'Vessel':1}
        },

    'templeofthematriarch':{
            'title':'Temple of the Matriarch',
            'description':'An alter to the Matriarch. May Her loving-kindness quench your thirst.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[12, 2, 0, None, 1, None],
            'mechanics': None, #aka traits
            'mechanics_args': None,
            'play_cost': {'Stone':5},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':['Arkanist'],
            'input_dict':{'Water':5},
            'output_dict':{'Water':12},
            'cat_dict':{'Vessel':1}
        },

    'templeofthearchitect':{
            'title':'Temple of the Architect',
            'description':'An alter to the Architect. May His wisdom and foresight tend to all your needs.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[5, 2, 0, None, 1, None],
            'mechanics': None, #aka traits
            'mechanics_args': None,
            'play_cost': {'Metal':5},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':['Arkanist'],
            'input_dict':{'Metal':3},
            'output_dict':{'Metal':5},
            'cat_dict':{'Vessel':1}
        },

    'templeofthewarlord':{
            'title':'Temple of the Warlord',
            'description':'An alter to the Warlord. May His strength fall upon you so that you may be a blight to your enemies.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[1, 1, 0, None, None, None],
            'mechanics': ['Defense'], #aka traits
            'mechanics_args': [2], #Defense Modifier
            'play_cost': {'Metal':3, 'Stone':2},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':['Arkanist'],
            'input_dict':None,
            'output_dict':None,
            'cat_dict':{'Vessel':1}
        },

    'templeofthepatron':{
            'title':'Temple of the Patron',
            'description':'An alter to the Patron. May His loving embrace satiate your hunger.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[1, 1, 0, None, 2, None],
            'mechanics': ['Upkeep'], #aka traits
            'mechanics_args': None,
            'play_cost': {'Wood':3, 'Stone':2},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':['Arkanist'],
            'input_dict':None,
            'output_dict':None,
            'cat_dict':None,
        },

    'templeofthevigil':{
            'title':'Temple of the Vigil',
            'description':'An alter to the Vigil. May His watchful eye be your ward.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[1, 1, 0, None, None, None],
            'mechanics': ['Ward'], #aka traits
            'mechanics_args': [0], #Range
            'play_cost': {'Metal':2, 'Stone':3},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':None,
            'input_dict':None,
            'output_dict':None,
            'cat_dict':{'Vessel':1},
        },

    'templeofthetraveler':{
            'title':'Temple of the Traveler',
            'description':'An alter to the Traveler. May His wanderings inspire you to go far and wide.',
            #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
            'inv_args':[1, 1, 0, None, 2, None],
            'mechanics': ['Speed'], #aka traits
            'mechanics_args': None,
            'play_cost': {'Wood':2, 'Stone':3},
            'stats':{'attack':0, 'health':3, 'defense':2, 'size':2},
            'worker_req':['Arkanist'],
            'input_dict':None,
            'output_dict':None,
            'cat_dict':{'Vessel':1},
        },


    # Industrialist:

    'industrialist_ranger_barracks':{
        'title':'Industrialist Ranger Barracks',
        'description':'A training grounds for Rangers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Ranger'],
        'play_cost': {'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':2, 'size':1},
        'worker_req':['Industrialist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'industrialist_alchemist_barracks':{
        'title':'Industrialist Alchemist Barracks',
        'description':'A training grounds for Rangers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[1, 1, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Alchemist'],
        'play_cost': {'Stone':2, 'Metal':1, 'Water':1},
        'stats':{'attack':0, 'health':3, 'defense':4, 'size':1},
        'worker_req':['Industrialist'],
        'input_dict':{'Heart':1},
        'output_dict':None,
        'cat_dict':None
    },

    'industrialist_scout_guild':{
        'title':'Industrialist Scouting Guild',
        'description':'A training grounds for Scouts',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Scout'],
        'play_cost': {'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Industrialist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'industrialist_engineering_guild':{
        'title':'Industrialist Engineering Guild',
        'description':'A training grounds for Engineers',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[None, None, None, None, 1, None],
        'mechanics': ['Train'], #aka traits
        'mechanics_args': ['Engineer'],
        'play_cost': {'Stone':2},
        'stats':{'attack':0, 'health':2, 'defense':1, 'size':1},
        'worker_req':['Industrialist'],
        'input_dict':None,
        'output_dict':None,
        'cat_dict':None
    },

    'mechanized_excavator':{
        'title':'Mechanized Excavator',
        'description':'A series of apparatus which allows for significantly more harvesting of minerals.',
        #[r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap]
        'inv_args':[5, 3, None, None, 3, None],
        'mechanics': None, #aka traits
        'mechanics_args': None,
        'play_cost': {'Metal':3, 'Heart':1},
        'stats':{'attack':0, 'health':4, 'defense':2, 'size':1},
        'worker_req':['Engineer'],
        'input_dict':None,
        'output_dict':{'Stone':3, 'Coal':2,'Ore':2},
        'cat_dict':None
    },

    }
