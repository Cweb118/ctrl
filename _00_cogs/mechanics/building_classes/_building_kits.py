building_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    #'template': ['title', 'description', 'inv_args', 'traits', 'play_cost', 'stats', 'workers_dict', 'input_dict', 'output_dict', 'cat_dict'],

    #owner, title, description, inv_args, traits, logic_args, play_cost, stats, worker_req, input_dict, output_dict, cat_dict):

    #2:

    # Village:
    'cottage':['Cottage', 'A place to unwind after a long day.',
              [None, None, 4, None, 2, None], ['Reproduce'], None, {'Wood':2},
              {'attack':0, 'health':2, 'defense':1, 'size':1},
              None, None, None, None],

    'scouting_lodge':['Scouting Lodge', 'A place where prospective scouts gather to refine their trade.',
              [None, None, None, None, 1, None], ['Train'], ['Scout'], {'Wood':4},
              {'attack':0, 'health':2, 'defense':2, 'size':1},
              ['Novice'], None, None, None],

    'shooting_range':['Shooting Range', 'A place where prospective rangers gather to refine their trade.',
              [None, None, None, None, 1, None], ['Train'], ['Ranger'], {'Wood':3},
              {'attack':0, 'health':2, 'defense':2, 'size':1},
              ['Novice'], None, None, None],

    'couriers_guild':['Couriers Guild', 'An office for the quick distribution of goods.',
              [None, None, None, None, 6, None], ['Carry'], ['arg'], {'Wood':6},
              {'attack':0, 'health':2, 'defense':2, 'size':2},
              None, None, None, None, 100],

    'otavan_pub':['Otavan Pub', 'A place to unwind after a long day.',
              [None, None, None, None, 2, None], ['Boon'], ['Good Morale'], {'Wood':2},
              {'attack':0, 'health':2, 'defense':1, 'size':1},
              None, {'Water':1, 'Food':1}, None, None, 100],



    #harmony:

    'mother_tree':['Mother Tree', 'A kind tree who drinks from the deep.',
              [4, 1, None, None, 1, None], [], None, {'Food':3,'Water':2},
              {'attack':0, 'health':4, 'defense':2, 'size':1},
              ['Harvest', 'Harmony'], None, {'Water':2}, None],

    'bountiful_field':['Bountiful Field', 'A field with grounds ripe for harvesting.',
              [10, 2, None, None, 2, None], [], None, {'Food':2},
              {'attack':0, 'health':2, 'defense':0, 'size':1},
              ['Production', 'Harmony'], {'Water':2}, {'Food':4}, None],

    'healing_grove':['Healing Grove', 'A soothing respite that regenerates 1 health of units within.',
              [3, 2, None, None, 1, None], ['Mend'], ['Health', 1], None,
              {'attack':0, 'health':1, 'defense':0, 'size':1},
              None, {'Water':1, 'Food':1}, None, None],

    'living_briar':['Living Briar', 'A vicious briar of thorns which provides security those within.',
              [None, None, None, None, 4, None], ['Thorns'], None, None,
              {'attack':0, 'health':6, 'defense':8, 'size':3},
              ['Harmony'], None, None, None],

    'towering_forest':['Towering Forest', 'A forest of towering trees which can be processed into wood.',
              [14, 2, None, None, 3, None], [], None, {'Food':4},
              {'attack':0, 'health':4, 'defense':0, 'size':2},
              ['Production', 'Harmony'], {'Water':3}, {'Wood':6}, None],


    #defensive (need 10, vary wood/stone/metal)
    'wooden_wall':['Wooden Wall', 'A Simple Wall',
                  [10, 2, None, None, 3, None], [], None, {'Wood':4},
                  {'attack':0, 'health':3, 'defense':8, 'size':2},
                  None, None, None, None],

    'metal_wall':['Metal Wall', 'A Sturdy Wall',
                  [10, 2, None, None, 2, None], [], None, {'Metal':4},
                  {'attack':0, 'health':4, 'defense':12, 'size':2},
                  None, None, None, None],

    'outpost':['Outpost', 'A Simple Outpost',
              [5, 1, None, None, 1, None], [], None, {'Wood':1},
              {'attack':0, 'health':2, 'defense':8, 'size':1},
              None, None, None, None],

    'bunker':['Bunker', 'A Simple Bunker',
              [10, 3, None, None, 4, None], [], None, {'Metal':4, 'Wood':2},
              {'attack':0, 'health':5, 'defense':14, 'size':3},
              None, None, None, None],

    'fort':['Fort', 'A Simple Fort',
              [15, 4, None, None, 6, None], [], None, {'Metal':7, 'Wood':5},
              {'attack':0, 'health':8, 'defense':16, 'size':4},
              None, None, None, None],

    'bastion':['Bastion', 'A Simple Bastion',
              [20, 5, None, None, 9, None], [], None, {'Metal':12, 'Wood':8},
              {'attack':0, 'health':10, 'defense':20, 'size':6},
              None, None, None, None],
    }
