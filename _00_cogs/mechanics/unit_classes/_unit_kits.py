unit_kits_dict = {
    #inv_args: (r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None)
    'template':('title', 'description',
                'inv_args', 'traits', 'play_cost',
                'attack', 'defence', 'endurance', 'fortitude', 'upkeep', 'dice_stats'),

    'worker':('Worker', 'A Simple Laborer',
              [None, None, None, None, None, None], [], {},
              0, 1, 1, 9, {'Food':1, 'Water':1}, [1,6]),

    'warrior':('Warrior', 'A Simple Soldier',
               [2, 1, None, None, None, None], [], {},
               2, 2, 2, 11, {'Food':2, 'Water':1}, [1,6]),

    'scout':('Scout', 'A Reconnaissance Unit',
             [4, 3, None, None, None, None], [], {},
             1, 2, 3, 12, {'Food':1, 'Water':2}, [1,6]),
}
