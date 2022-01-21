building_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    'template': ['title', 'description', 'inv_args', 'traits', 'play_cost', 'stats', 'workers_dict', 'input_dict', 'output_dict', 'cat_dict'],

    #2:

    #harmony:

    'mother_tree':['Mother Tree', 'A kind tree who drinks from the deep.',
              [4, 1, None, None, 1, None], ['Harvest', 'Harmony'], {'Food':3,'Water':2},
              {'attack':0, 'health':4, 'defense':2, 'size':1},
              ['Worker'], None, {'Water':2}, None],

    'bountiful_field':['Bountiful Field', 'A field with grounds ripe for harvesting.',
              [10, 2, None, None, 2, None], ['Production', 'Harmony'], {'Food':2},
              {'attack':0, 'health':2, 'defense':0, 'size':1},
              ['Worker'], {'Water':2}, {'Food':4}, None],


    #defensive
    'wooden_wall':['Wooden Wall', 'A Simple Wall',
                  [10, 2, None, None, 3, None], ['Defense'], {'Wood':4},
                  {'attack':0, 'health':3, 'defense':8, 'size':2},
                  None, None, None, None],

    'metal_wall':['Metal Wall', 'A Sturdy Wall',
                  [10, 2, None, None, 2, None], ['Defense'], {'Metal':4},
                  {'attack':0, 'health':4, 'defense':12, 'size':2},
                  None, None, None, None],

    'outpost':['Outpost', 'A Simple Outpost',
              [5, 1, None, None, 1, None], ['Defense'], {'Wood':1},
              {'attack':0, 'health':2, 'defense':8, 'size':1},
              None, None, None, None],

    'bunker':['Bunker', 'A Simple Bunker',
              [10, 3, None, None, 4, None], ['Defense'], {'Metal':4, 'Wood':2},
              {'attack':0, 'health':5, 'defense':14, 'size':3},
              None, None, None, None],

    'fort':['Fort', 'A Simple Fort',
              [15, 4, None, None, 6, None], ['Defense'], {'Metal':7, 'Wood':5},
              {'attack':0, 'health':8, 'defense':16, 'size':4},
              None, None, None, None],

    'bastion':['Bastion', 'A Simple Bastion',
              [20, 5, None, None, 9, None], ['Defense'], {'Metal':12, 'Wood':8},
              {'attack':0, 'health':10, 'defense':20, 'size':6},
              None, None, None, None],
    }
