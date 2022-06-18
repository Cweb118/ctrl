from _00_cogs.mechanics.trait_classes.trait_classes import *

trait_kits_dict = {
    #name, description, type, certs, triggers, action, mod_inv_args, mod_play_cost, mod_stats_dict, initiative, taunt, mod_upkeep_dict, new_dice_stats
    # cap:{resource/unit/building}, slotcap:{unit/building} cont
    #r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap
    'Aratori':['Aratori', 'A mighty race of great strength, the Aratori have built an empire to last the test of time.',
              'race', None, ['on_attack'], Aratori(),
             {'cap':{'resource':3}, 'cont':1}, None,
             {'Attack':1,'Fortitude':2}, None, None,
             {'Food':1}, ['1d7']],

    'Barheim':['Barheim', 'A race of Engineers, their hearts are said to be as hard and cold as their flesh.',
              'race', None, ['on_play'], Barheim(),
             {'cont':2}, None,
               None, None, -1,
               None, ['1d4']],

    'Automata':['Automata', 'A creation of the Barheim, the Automata can brave dangers no man should face.',
              'race', None, ['on_play'], Automata(),
             {'cont':1}, None,
             {'Health':1,'Defense':2}, None, None,
             {'Food':-10, 'Water':-10}, ['2d4']],

    'Eelaki':['Eelaki', 'Natural engineers, the Eelaki are strong kin with the Tevaru, whose chitinous suits they designed.',
              'race', None, ['on_play'], Eelaki(),
              None, None, {'Endurance':-1}, -2, -1, None, ['2d3']],

    'Loyavasi':['Loyavasi', "A hoofed people from the mountains, the Loyavasi never sit still for long.",
                'race', None, ['on_refresh'], Loyavasi(),
                {'cap':{'resource':2}}, None,
                None, -1, None, None, ['1d6', '1d2']],

    'Otavan':['Otavan', 'Descendants of Aratori colonists, these who have made their lives in the countryside have learned to subvert strength with subterfuge.',
              'race', None, ['on_play'], Otavan(),
             None, None, None, None, -2, None, ['1d6']],

    'Prismari':['Prismari', "A regal race of birds who move quite fast for their size.",
              'race', None, ['on_defend'], Prismari(),
             None, None,
             {'Health':1,'Endurance':1}, None, None,
             {'Water':1}, ['1d5']],

    'Rivenborne':['Rivenborne', 'A mysterious race full of intrigue, the Rivenborne seek to claim their birthright as rules of Aporia.',
              'race', ['Charged'], ['on_play', 'on_refresh'], Rivenborne(),
             None, None, {'Health':1}, None, None, None, ['1d4', '1d8']],

    'Tevaru':['Tevaru', 'The Tevaru are aliens to the surface world, but despite the dangerous environment they feel more at home here.',
              'race', None, ['on_play'], Tevaru(),
             {'cap':{'resource':4, 'unit':1}, 'cont':2}, None,
             {'Health':2,'Fortitude':-1}, 1, 1,
             {'Water':3}, ['1d3']],

    'Xinn':['Xinn', 'An brutal race of bipedal bovines, what the Xinn lack in intellect they more than make up for in raw strength.',
              'race', ['Harvest'], ['on_play'], Xinn(),
             {'cap':{'resource':4}, 'cont':2}, None,
             {'Attack':3,'Health':1,'Fortitude':3}, None, 2,
             {'Food':1,'Water':1}, ['1d10']],

    'Yavari':['Yavari', 'A race hunters in tune with nature, the Yavari fight to preserve the natural order.',
              'race', None, ['on_act'], Yavari(),
             None, None, None, None, None, None, ['1d6']],



    #name, description, type, certs, trigger, action, mod_inv_args, mod_play_cost, mod_stats_dict, initiative, taunt, mod_upkeep_dict, new_dice_stats
    'Worker':['Worker', '*No man\'s bounty may exceed the sweat of his brow. -The Book of The Patron 5:2*', 'class', ['Novice', 'Harvest', 'Production'], ['on_play'], Worker(), None, None, None, None, None, None, None],
    'Warrior':['Warrior', '*None shall remain. - The Harbinger*', 'class', ['Combat'], ['on_attack'], Warrior(), None, None, None, None, None, None, None],
    'Guardian':['Guardian', '*As I have cared for you, so ought you care for one another. - The Matriarch*', 'class', ['Combat'], ['on_defend', 'on_attack'], Guardian(), None, None, None, None, None, None, None],
    'Ranger':['Ranger', '*A sword should never touch they who are of nimble mind. - Yavari Proverb*', 'class', ['Combat'], ['on_attack'], Ranger(), None, None, None, None, None, None, None],
    'Scout':['Scout', '*Should you seek after Her own heart, given an eternity, you will find Her.* - Unknown Scribe' , 'class', ['Combat'], ['on_play'], Scout(), None, None, None, None, None, None, None],
    'Knight':['Knight', '*Let the stalwart of us take up arms, that the weak may live as the brave. -Keive, Aratori Hero*', 'class', ['Combat'], ['on_attack', 'on_defend'], Knight(), None, None, None, None, None, None, None],
    #'Witch':['Witch', 'The mark of a Witch', 'class', ['Combat', 'Arcanae'], ['on_battle','on_attack'], Witch(), None, None, None, None, None, None, None],
    'Alchemist':['Alchemist', 'The mark of an Alchemist', 'class', ['Combat', 'Engineer'], ['on_attack'], Alchemist(), None, None, None, None, None, None, None],
    'Technophant':['Technophant', 'The mark of a Technophant', 'class', ['Combat', 'Atomikist'], ['on_attack'], Technophant(), None, None, None, None, None, None, None],
    'Worker':['Worker', 'The mark of a Worker', 'class', ['Novice', 'Harvest', 'Production'], ['on_play'], Worker(),
              {'cap':{'resource':2}, 'cont':2}, None, {'Attack':0, 'Health':1, 'Defense':6, 'Endurance':1, 'Fortitude':3}, 10, -10, {'Food':1, 'Water':1}, ['1d6']],
    'Warrior':['Warrior', 'The mark of a Warrior', 'class', ['Combat'], ['on_attack'], Warrior(),
               {'cap':{'resource':4}, 'cont':2}, None, {'Attack':2, 'Health':2, 'Defense':10, 'Endurance':2, 'Fortitude':3}, 0, 0, {'Food':2, 'Water':1}, ['1d6']],
    'Ranger':['Ranger', 'The mark of a Ranger', 'class', ['Combat'], ['on_attack'], Ranger(),
              {'cap':{'resource':2}, 'cont':2}, None, {'Attack':2, 'Health':1, 'Defense':8, 'Endurance':2, 'Fortitude':4}, -1, -1, {'Food':1, 'Water':1}, ['1d8']],
    'Guardian':['Guardian', 'The mark of a Guardian', 'class', ['Combat'], ['on_defend', 'on_attack'], Guardian(),
                {'cap':{'resource':6}, 'cont':2}, None, {'Attack':1, 'Health':3, 'Defense':12, 'Endurance':2, 'Fortitude':1}, 2, 3, {'Food':3, 'Water':1}, ['1d4']],
    'Scout':['Scout', 'The mark of a Scout', 'class', ['Combat', 'Scout'], ['on_play'], Scout(),
             {'cap':{'resource':8}, 'cont':3}, None, {'Attack':1, 'Health':2, 'Defense':8, 'Endurance':3, 'Fortitude':3},  5, -5, {'Food':1, 'Water':2}, ['1d6']],
    'Knight':['Knight', 'The mark of a Knight', 'class', ['Combat'], ['on_attack', 'on_defend'], Knight(),
              {'cap':{'resource':4}, 'cont':2}, None, {'Attack':3, 'Health':3, 'Defense':10, 'Endurance':2, 'Fortitude':4}, 0, 1, {'Food':2, 'Water':2}, ['1d5', '1d7']],
    'Alchemist':['Alchemist', 'The mark of an Alchemist', 'class', ['Combat', 'Engineer'], ['on_attack'], Alchemist(),
                 {'cap':{'resource':4}, 'cont':4}, None, {'Attack':1, 'Health':1, 'Defense':8, 'Endurance':3, 'Fortitude':1},  0, -1, {'Food':1, 'Water':3}, ['1d4']],
    'Technophant':['Technophant', 'The mark of a Technophant', 'class', ['Combat', 'Atomikist'], ['on_attack', 'on_refresh'], Technophant(),
                   {'cap':{'resource':6}, 'cont':2}, None, {'Attack':0, 'Health':5, 'Defense':10, 'Endurance':2, 'Fortitude':0}, 4, 0, {'Water':4}, ['1d5']],

    'Harmony':['Harmony', 'One who is attuned to the Melding.',
              'effect', ['Harmony'], ['on_harvest'], Harmony(),
             None, None, None, None, None, None, None],

    'Charged':['Charged', 'One who is empowered by a greater force...',
              'effect', ['Charged'], ['on_harvest'], Charged(),
             None, None, {'Health':1,'Fortitude':-1}, None, None, None, None],

    #building_logic

    'Mend':['Mend', 'MEND_DESC', 'building_logic', None, ['on_work'], Mend(), None, None, None, None, None, None, None],
    'Train':['Train', 'TRAIN_DESC', 'building_logic', None, ['on_work'], Train(), None, None, None, None, None, None, None],
    'Reproduce':['Reproduce', 'REPO_DESC', 'building_logic', None, ['on_work'], Reproduce(), None, None, None, None, None, None, None],
    'Boon':['Boon', 'BOON_DESC', 'building_logic', None, ['on_work'], Boon(), None, None, None, None, None, None, None],
    'Carry':['Carry', 'CARRY_DESC', 'building_logic', None, ['on_act', 'on_work', 'on_harvest'], Carry(), None, None, None, None, None, None, None],

    #building_effects
    'Good Morale':['Good Morale', 'GM_DESC', 'building_effect', None, ['on_work'], Morale(), None, None, None, None, None, None, None],

}

