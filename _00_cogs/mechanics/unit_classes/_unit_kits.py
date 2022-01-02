unit_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    'template': ['title', 'description',
                 'inv_args', 'traits', 'play_cost',
                 'attack', 'health', 'defense', 'endurance', 'fortitude', 'upkeep', 'dice_stats'],

    'worker':['Worker', 'A Simple Laborer',
              [2, 2, None, None, None, None], [], None,
              {'attack':0, 'health':1, 'defense':6, 'endurance':1, 'fortitude':3},
              {'Food':1, 'Water':1}, [[1,6]]],

    'warrior':['Warrior', 'A Simple Soldier',
               [4, 2, None, None, None, None], ['Aratori'], None,
               {'attack':2, 'health':2, 'defense':10, 'endurance':2, 'fortitude':1},
               {'Food':2, 'Water':1}, [[1,6]]],

    'ranger':['Ranger', 'A Skilled Shot',
               [2, 2, None, None, None, None], [], None,
              {'attack':2, 'health':1, 'defense':8, 'endurance':2, 'fortitude':3},
                {'Food':1, 'Water':1}, [[1,8]]],

    'guardian':['Guardian', 'A Noble Protector',
           [6, 2, None, None, None, None], [], None,
            {'attack':1, 'health':3, 'defense':12, 'endurance':2, 'fortitude':1},
            {'Food':3, 'Water':1}, [[1,4]]],

    'scout':['Scout', 'A Brave Adventurer',
             [8, 3, None, None, None, None], [], None,
             {'attack':1, 'health':2, 'defense':8, 'endurance':3, 'fortitude':5},
             {'Food':1, 'Water':2}, [[1,6]]],
}
