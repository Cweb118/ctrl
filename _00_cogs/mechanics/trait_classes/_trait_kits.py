from _00_cogs.mechanics.trait_classes.trait_classes import *

trait_kits_dict = {
    #name, description, trigger, action, mod_inv_args, mod_play_cost, mod_stats_dict, initiative, taunt, mod_upkeep_dict, new_dice_stats
    # cap:{resource/unit/building}, slotcap:{unit/building} cont
    #r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap
    'Aratori':['Aratori', 'A mighty race of great strength, the Aratori have built an empire to last the test of time.',
              ['on_attack'], Aratori(),
             {'cap':{'resource':3}, 'cont':1}, None,
             {'Attack':1,'Fortitude':2}, None, None,
             {'Food':1}, ['1d7']],

    'Barheim':['Barheim', 'A mighty race of great strength, the Barheim have built an empire to last the test of time.',
              ['on_play'], Barheim(),
             {'cont':2}, None,
               None, None, -1,
               None, ['1d4']],

    'Automata':['Automata', 'A creation of the Barheim.',
              ['on_play'], Automata(),
             {'cont':1}, {'Health':1,'Defense':2}, None, None, None, {'Food':-10, 'Water':-10}, ['2d4']],

    'Eelaki':['Eelaki', 'Natural engineers, the Eelaki are strong kin with the Tevaru, whose chitinous suits they designed.',
              ['on_play'], Eelaki(),
              None, None, None, -2, None, None, ['2d3']],

    'Loyavasi':['Loyavasi', "A mighty race of great strength, the Loyavasi have built an empire to last the test of time.",
                ['on_move'], Loyavasi(),
                {'cap':{'resource':2}}, None,
                {'Endurance':2}, -1, None, None, ['1d6']],

    'Prismari':['Prismari', "A regal race of birds who move quite fast for their size.",
              ['on_defend'], Prismari(),
             None, None,
             {'Health':1,'Endurance':1}, None, None,
             {'Water':1}, ['1d5']],

    'Rivenborne':['Rivenborne', 'A mighty race of great strength, the Barheim have built an empire to last the test of time.',
              ['on_play'], Rivenborne(),
             None, None, {'Health':2}, None, None, None, ['1d4', '1d8']],

    'Tevaru':['Tevaru', 'The Tevaru are aliens to the surface world, but despite the dangerous environment they feel more at home here.',
              ['on_play'], Tevaru(),
             {'cap':{'resource':4, 'unit':1}, 'cont':2}, None,
             {'Health':2,'Fortitude':-1}, 1, None,
             {'Water':3}, ['1d3']],

    'Xinn':['Xinn', 'A towering race of behemoths, the Xinn have been through thick and thin.',
              ['on_play'], Xinn(),
             {'cap':{'resource':4}, 'cont':2}, None,
             {'Attack':3,'Health':1,'Fortitude':3}, None, 2,
             {'Food':1,'Water':1}, ['1d10']],

    'Yavari':['Yavari', 'A mighty race of great strength, the Yavari have survived through thick and thin.',
              ['on_play'], Yavari(),
             None, None, None, None, None, None, ['1d6']],

    'Yhont':['Yhont', 'A mighty race of great strength, the Yhont have survived through thick and thin.',
              ['on_play'], Yhont(),
             None, None, None, None, -2, None, ['1d6']],

    #name, description, trigger, action, mod_inv_args, mod_play_cost, mod_stats_dict, initiative, taunt, mod_upkeep_dict, new_dice_stats
    'Worker':['Worker', 'The mark of a Worker', ['on_play'], Worker(), None, None, None, None, None, None, None],
    'Warrior':['Warrior', 'The mark of a Warrior', ['on_attack'], Warrior(), None, None, None, None, None, None, None],
    'Guardian':['Guardian', 'The mark of a Guardian', ['on_defend', 'on_attack'], Guardian(), None, None, None, None, None, None, None],
    'Ranger':['Ranger', 'The mark of a Ranger', ['on_attack'], Ranger(), None, None, None, None, None, None, None],
    'Scout':['Scout', 'The mark of a Worker', ['on_play'], Scout(), None, None, None, None, None, None, None],
    'Knight':['Knight', 'The mark of a Knight', ['on_attack', 'on_defend'], Knight(), None, None, None, None, None, None, None],
    'Alchemist':['Alchemist', 'The mark of an Alchemist', ['on_attack'], Alchemist(), None, None, None, None, None, None, None],
    'Technophant':['Technophant', 'The mark of a Technophant', ['on_attack'], Technophant(), None, None, None, None, None, None, None],

}
