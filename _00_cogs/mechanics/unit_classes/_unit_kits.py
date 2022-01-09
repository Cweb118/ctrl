unit_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    'template': ['title', 'description',
                 'inv_args', 'traits', 'play_cost',
                 'attack', 'health', 'defense', 'endurance', 'fortitude', 'upkeep', 'dice_stats'],

    'worker':['Worker', 'A Simple Laborer',
              [2, 2, None, None, None, None], ['Worker'], None,
              {'attack':0, 'health':1, 'defense':6, 'endurance':1, 'fortitude':3},
              {'Food':1, 'Water':1}, ['1d6']],

    'warrior':['Warrior', 'A Simple Soldier',
               [4, 2, None, None, None, None], ['Warrior', 'Aratori'], None,
               {'attack':2, 'health':2, 'defense':10, 'endurance':2, 'fortitude':3},
               {'Food':2, 'Water':1}, ['1d6']],

    'ranger':['Ranger', 'A Skilled Shot',
               [2, 2, None, None, None, None], ['Ranger', 'Yavari'], None,
              {'attack':2, 'health':1, 'defense':8, 'endurance':2, 'fortitude':4},
                {'Food':1, 'Water':1}, ['1d8']],

    'guardian':['Guardian', 'A Noble Protector',
           [6, 2, None, None, None, None], ['Guardian', 'Tevaru'], None,
            {'attack':1, 'health':3, 'defense':12, 'endurance':2, 'fortitude':1},
            {'Food':3, 'Water':1}, ['1d4']],

    'scout':['Scout', 'A Brave Adventurer',
             [8, 3, None, None, None, None], ['Scout', 'Loyavasi'], None,
             {'attack':1, 'health':2, 'defense':8, 'endurance':3, 'fortitude':3},
             {'Food':1, 'Water':2}, ['1d6']],
}
