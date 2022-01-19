unit_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    'template': ['title', 'description',
                 'inv_args', 'traits', 'play_cost',
                 'attack', 'health', 'defense', 'endurance', 'fortitude', 'upkeep', 'dice_stats'],

    'Worker':['Worker', 'A Simple Laborer',
              [2, 2, None, None, None, None], ['Worker'], None,
              {'attack':0, 'health':1, 'defense':6, 'endurance':1, 'fortitude':3},
              {'Food':1, 'Water':1}, 10, -10, ['1d6']],

    'Warrior':['Warrior', 'A Simple Soldier',
               [4, 2, None, None, None, None], ['Warrior'], None,
               {'attack':2, 'health':2, 'defense':10, 'endurance':2, 'fortitude':3},
               {'Food':2, 'Water':1}, 0, 0, ['1d6']],

    'Ranger':['Ranger', 'A Skilled Shot',
               [2, 2, None, None, None, None], ['Ranger'], None,
              {'attack':2, 'health':1, 'defense':8, 'endurance':2, 'fortitude':4},
                {'Food':1, 'Water':1}, -1, -1, ['1d8']],

    'Guardian':['Guardian', 'A Noble Protector',
           [6, 2, None, None, None, None], ['Guardian'], None,
            {'attack':1, 'health':3, 'defense':12, 'endurance':2, 'fortitude':1},
            {'Food':3, 'Water':1}, 2, 3, ['1d4']],

    'Scout':['Scout', 'A Brave Adventurer',
             [8, 3, None, None, None, None], ['Scout'], None,
             {'attack':1, 'health':2, 'defense':8, 'endurance':3, 'fortitude':3},
             {'Food':1, 'Water':2}, 5, -5, ['1d6']],

    'Knight':['Knight', 'A Noble Swordsman',
             [4, 2, None, None, None, None], ['Knight'], None,
             {'attack':3, 'health':3, 'defense':10, 'endurance':2, 'fortitude':4},
             {'Food':2, 'Water':2}, 0, 1, ['1d5', '1d7']],

    'Alchemist':['Alchemist', 'A Crafty Chemist',
             [4, 4, None, None, None, None], ['Alchemist'], None,
             {'attack':1, 'health':1, 'defense':8, 'endurance':3, 'fortitude':1},
             {'Food':1, 'Water':3}, 0, -1, ['1d4']],

    'Technophant':['Technophant', 'A Fearsome Technophant',
             [6, 2, None, None, None, None], ['Technophant'], None,
             {'attack':0, 'health':5, 'defense':10, 'endurance':2, 'fortitude':0},
             {'Water':4}, 4, 0, ['1d5']],
}
