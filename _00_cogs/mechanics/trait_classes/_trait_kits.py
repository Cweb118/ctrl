from _00_cogs.mechanics.trait_classes.trait_classes import *

trait_kits_dict = {
    #name, description, type, certs, triggers, action, mod_inv_args, mod_play_cost, mod_stats_dict, initiative, taunt, mod_upkeep_dict, new_dice_stats
    # cap:{resource/unit/building}, slotcap:{unit/building} cont
    #r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap
    'Aratori':['Aratori', 'A mighty race of great strength, the Aratori have built an empire to last the test of time.', 'race',
               None, ['on_attack'], Aratori(), {'cap':{'resource':3}, 'cont':1}, None,
               {'Attack':1,'Fortitude':2}, {'Food':1}, ['1d7']],

    'Barheim':['Barheim', 'A race of Engineers, their hearts are said to be as hard and cold as their flesh.', 'race',
               ['Engineer'], ['on_play'], Barheim(), {'cont':2}, None,
               {'Defense':2, 'Initiative':-1}, None, ['1d4']],

    'Automata':['Automata', 'A creation of the Barheim, the Automata can brave dangers no man should face.', 'race',
                ['Inorganic'], ['on_play'], Automata(), {'cont':1}, None,
                {'Health':1,'Defense':2}, {'Food':-10, 'Water':-10}, ['2d4']],

    'Eelaki':['Eelaki', 'Natural engineers, the Eelaki are strong kin with the Tevaru, whose chitinous suits they designed.', 'race',
              ['Engineer'], ['on_play'], Eelaki(), None, None,
              {'Endurance':-1, 'Initiative':-2, 'Taunt':-1}, None, ['2d3']],

    'Loyavasi':['Loyavasi', "A hoofed people from the mountains, the Loyavasi never sit still for long.", 'race',
                None, ['on_move', 'on_refresh'], Loyavasi(), {'cap':{'resource':2}}, None,
                {'Initiative':-1}, None, ['1d6', '1d2']],

    'Otavan':['Otavan', 'Descendants of Aratori colonists, these who have made their lives in the countryside have learned to subvert strength with subterfuge.', 'race',
              None, ['on_play'], Otavan(), None, None,
              {'Taunt':-2},  None, ['1d6']],

    'Prismari':['Prismari', "A regal race of birds who move quite fast for their size.", 'race',
                ['Transporter'], ['on_defend'], Prismari(), None, None,
             {'Health':1,'Endurance':1}, {'Water':1}, ['1d5']],

    'Rivenborne':['Rivenborne', 'A mysterious race, the Rivenborne seek to claim their self-proclaimed birthright as rules of Aporia.', 'race',
                  ['Charged', 'Inorganic'], ['on_play', 'on_refresh'], Rivenborne(), None, None,
                  {'Health':1}, None, ['1d4', '1d8']],

    'Tevaru':['Tevaru', 'The Tevaru are aliens to the surface world, but despite the dangerous environment they feel more welcomed here.', 'race',
              ['Aquatic'], ['on_play'], Tevaru(), {'cap':{'resource':4, 'unit':1}, 'cont':2}, None,
             {'Health':2, 'Defense':1, 'Fortitude':-1, 'Initiative':1, 'Taunt':1}, {'Water':3}, ['1d3']],

    'Xinn':['Xinn', 'An brutal race of bipedal bovines, what the Xinn lack in intellect they more than make up for in raw strength.',
              'race', ['Laborer'], ['on_play'], Xinn(),
             {'cap':{'resource':4}, 'cont':2}, None,
             {'Attack':3,'Health':1,'Fortitude':3, 'Taunt':2}, {'Food':1,'Water':1}, ['1d10']],

    'Yavari':['Yavari', 'A race hunters in tune with nature, the Yavari fight to preserve the natural order.', 'race',
              ['Harmonist'], ['on_act'], Yavari(),
             None, None, None, None, ['1d6']],



    #name, description, type,
    # certs, trigger, action, mod_inv_args, mod_play_cost,
    # mod_stats_dict, initiative, taunt, mod_upkeep_dict, new_dice_stats

    #commerce

    'Worker':['Worker', '*And let the works of a craftsman satiate their hunger. -The Book of The Patron 5:3*', 'class',
              ['Worker'], ['on_play'], Worker(), {'cap':{'resource':3}, 'cont':2}, None,
              {'Attack':0, 'Health':1, 'Defense':6, 'Endurance':1, 'Fortitude':4, 'Initiative':10, 'Taunt':-10}, {'Food':2, 'Water':1}, ['1d6']],

    'Laborer':['Laborer', '*Let no man\'s bounty exceed the sweat of their brow -The Book of The Patron 5:2*', 'class',
               ['Worker', 'Laborer'], ['on_play'], Laborer(), {'cap':{'resource':3}, 'cont':2}, None,
               {'Attack':0, 'Health':1, 'Defense':6, 'Endurance':1, 'Fortitude':5, 'Initiative':10, 'Taunt':-10}, {'Food':1, 'Water':2}, ['1d7']],

    'Engineer':['Engineer', '*The dullest wit would put even the sharpest blade to shame. -Barheimian Proverb*', 'class',
                ['Worker', 'Engineer'], ['on_play'], Engineer(), {'cap':{'resource':2}, 'cont':2}, None,
                {'Attack':0, 'Health':1, 'Defense':6, 'Endurance':1, 'Fortitude':3, 'Initiative':10, 'Taunt':-10}, {'Food':1, 'Water':1}, ['1d5']],

    'Courier':['Courier', '*May your feet be swift, and your loads light! - A parting adage among Couriers*', 'class',
               ['Transporter'], ['on_play'], Transport(), {'cap':{'resource':2}, 'cont':2}, None,
               {'Attack':0, 'Health':1, 'Defense':6, 'Endurance':2, 'Fortitude':3, 'Initiative':10, 'Taunt':-10}, {'Food':1, 'Water':1}, ['1d6']],

    'Caravan':['Caravan', '*Safety in numbers... - An old adage*', 'class',
               ['Transporter'], ['on_play'], Transport(), {'cap':{'resource':15}, 'cont':6}, None,
               {'Attack':0, 'Health':2, 'Defense':8, 'Endurance':3, 'Fortitude':3, 'Initiative':10, 'Taunt':-10}, {'Wood':1, 'Stone':1}, ['1d6']],

    'Architect':['Architect', '*We walk in the very footsteps of the gods. -Unknown Scribe (likely an Architect)*', 'class',
                 ['Architect'], ['on_act', 'on_harvest'], Architect(), {'cap':{'resource':2}, 'cont':2}, None,
                 {'Attack':0, 'Health':1, 'Defense':6, 'Endurance':1, 'Fortitude':3, 'Initiative':10, 'Taunt':-10}, {'Food':1, 'Water':1}, ['1d6']],


    #recon

    'Pathfinder':['Pathfinder', '*Should you seek after Her own heart, given an eternity, you will find Her. - Unknown Scribe*', 'class',
                  ['Recon'], ['on_act', 'on_harvest'], Pathfinder(), {'cap':{'resource':6}, 'cont':3}, None,
                  {'Attack':1, 'Health':2, 'Defense':7, 'Endurance':3, 'Fortitude':5, 'Initiative':3, 'Taunt':-4}, {'Food':2, 'Water':1}, ['1d7']],

    'Scout':['Scout', '*Think of it this way, the more time we spend out roaming the wilds, the less we spend tilling fields. -Unknown Scout*', 'class',
             ['Recon'], ['on_act', 'on_harvest'], Scout(), {'cap':{'resource':6}, 'cont':3}, None,
             {'Attack':1, 'Health':2, 'Defense':8, 'Endurance':3, 'Fortitude':3, 'Initiative':5, 'Taunt':-5},  {'Food':1, 'Water':2}, ['1d6']],

    'Sentry':['Sentry', '*Nothing remains unseen under a watchful eye. -An adage among Sentries *', 'class',
              ['Recon'], ['on_harvest'], Sentry(), {'cap':{'resource':5}, 'cont':2}, None,
              {'Attack':1, 'Health':3, 'Defense':9, 'Endurance':2, 'Fortitude':2, 'Initiative':2, 'Taunt':1}, {'Food':1, 'Water':1}, ['1d5']],

    #combat

    'Warrior':['Warrior', '*None shall remain. - A quote attributed to The Harbinger*', 'class',
               ['Combat'], ['on_attack'], Warrior(), {'cap':{'resource':4}, 'cont':2}, None,
               {'Attack':2, 'Health':2, 'Defense':10, 'Endurance':2, 'Fortitude':3, 'Initiative':0, 'Taunt':0}, {'Food':2, 'Water':1}, ['1d6']],

    'Ranger':['Ranger', '*A sword should never touch they who are of nimble mind. - Yavari Proverb*', 'class',
              ['Combat'], ['on_attack'], Ranger(), {'cap':{'resource':3}, 'cont':2}, None,
              {'Attack':2, 'Health':1, 'Defense':8, 'Endurance':2, 'Fortitude':4, 'Initiative':-1, 'Taunt':-1}, {'Food':1, 'Water':1}, ['1d8']],

    'Guardian':['Guardian', '*As I have cared for you, so ought you care for one another. - The Matriarch*', 'class',
                ['Combat'], ['on_defend', 'on_attack'], Guardian(), {'cap':{'resource':6}, 'cont':2}, None,
                {'Attack':1, 'Health':3, 'Defense':12, 'Endurance':2, 'Fortitude':1, 'Initiative':2, 'Taunt':3}, {'Food':3, 'Water':1}, ['1d4']],

    'Witch':['Witch', '*[concerning, incoherent whispering] -???*', 'class',
             ['Combat', 'Arkanist'], ['on_attack', 'on_defend'], Witch(), {'cap':{'resource':2}, 'cont':2}, None,
             {'Attack':0, 'Health':2, 'Defense':7, 'Endurance':2, 'Fortitude':1, 'Initiative':-2, 'Taunt':-2}, {'Food':1, 'Water':1}, ['1d5']],

    'Knight':['Knight', '*Let the stalwart of us take up arms, that the weak may live as the brave. -Keive, Aratori Hero*', 'class',
              ['Combat', 'Arkanist'], ['on_attack', 'on_defend'], Knight(), {'cap':{'resource':4}, 'cont':2}, None,
              {'Attack':3, 'Health':3, 'Defense':10, 'Endurance':2, 'Fortitude':4, 'Initiative':0, 'Taunt':1}, {'Food':2, 'Water':2}, ['1d5', '1d7']],

    'Alchemist':['Alchemist', '*We stand on the cusp of a new magic- what a time to walk Aporia! - Jarrio, Great Aratori Engineer*', 'class',
                 ['Combat', 'Industrialist', 'Engineer'], ['on_attack'], Alchemist(), {'cap':{'resource':5}, 'cont':4}, None,
                 {'Attack':1, 'Health':1, 'Defense':8, 'Endurance':3, 'Fortitude':1, 'Initiative':0, 'Taunt':-1}, {'Food':1, 'Water':3}, ['1d4']],

    'Technophant':['Technophant', '*And now we walk the path of They who ended all things.* - [Unknown], HIVE Progenitor*', 'class',
                   ['Combat', 'Atomikist'], ['on_attack', 'on_refresh'], Technophant(), {'cap':{'resource':6}, 'cont':2}, None,
                   {'Attack':0, 'Health':5, 'Defense':10, 'Endurance':2, 'Fortitude':0, 'Initiative':4, 'Taunt':0}, {'Water':3, 'Metal':1}, ['1d5']],

    #effects
    'Harmony':['Harmony', 'One who is attuned to the Melding.',
              'effect', ['Harmony'], ['on_harvest'], Harmony(),
             None, None, None, None, None],

    'Charged':['Charged', 'One who is empowered by a greater force...',
              'effect', ['Charged'], ['on_harvest'], Charged(),
             None, None, {'Health':1,'Fortitude':-1}, None, None],

    'Good Morale':['Good Morale', 'One of joyful spirit!',
                   'effect', None, ['on_work'], Morale(),
                   None, None, None, None, None],

    #building_logic

    'Mend':['Mend', 'MEND_DESC', 'building_logic', None, ['on_work'], Mend(), None, None, None, None, None],
    'Upkeep':['Upkeep', 'UPKP_DESC', 'building_logic', None, ['on_work'], Upkeep(), None, None, None, None, None],
    'Speed':['Speed', 'SPD_DESC', 'building_logic', None, ['on_work'], Speed(), None, None, None, None, None],
    'Sacrifice':['Sacrifice', 'SCF_DESC', 'building_logic', None, ['on_work'], Sacrifice(), None, None, None, None, None],
    'Defense':['Defense', 'DEF_DESC', 'building_logic', None, ['on_work'], Defense(), None, None, None, None, None],
    'Ward':['Ward', 'WARD_DESC', 'building_logic', None, ['on_work'], Ward(), None, None, None, None, None],
    'Train':['Train', 'TRAIN_DESC', 'building_logic', None, ['on_work'], Train(), None, None, None, None, None],
    'Mentor':['Mentor', 'MTR_DESC', 'building_logic', None, ['on_work'], Mentor(), None,None, None, None, None],
    'Worker Boon':['Worker Boon', 'WB_DESC', 'building_logic', None, ['on_work'], WorkerBoon(), None, None, None, None, None],
    'District Boon':['District Boon', 'DB_DESC', 'building_logic', None, ['on_work'], DistrictBoon(),  None, None, None, None, None],
    'Transport':['Transport', 'CARRY_DESC', 'building_logic', None, ['on_act', 'on_harvest', 'on_refresh'], Transport(),  None, None, None, None, None],

    #building_effects

}

