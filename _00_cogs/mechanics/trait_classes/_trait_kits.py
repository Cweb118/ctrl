from _00_cogs.mechanics.trait_classes.aratori_class import Aratori

trait_kits_dict = {
    #name, description, trigger, action, mod_inv_args, mod_play_cost, mod_stats_dict, mod_upkeep_dict, new_dice_stats
    # cap:{resource/unit/building}, slotcap:{unit/building} cont
    #r_cap, r_cont, u_cap, b_cap, u_slotcap, b_slotcap
    'Aratori':['Aratori', 'A might race of great strength, the Aratori have survived through thick and thin.',
              'on_attack', Aratori(),
             {'cap':{'resource':3}, 'cont':1}, None,
             {'Attack':1,'Fortitude':2},
             {'Food':1}, [[1,4],[1,5],[1,6]]],
}
