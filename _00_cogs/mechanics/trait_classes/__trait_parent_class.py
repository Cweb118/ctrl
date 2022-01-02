

class Trait():
    def __init__(self, name, description, trigger, action, mod_inv_args, mod_play_cost, mod_stats_dict, mod_upkeep_dict, new_dice_stats):

        self.trait_title = name
        self.trait_description = description
        #triggers: on_play, on_work, on_move, on_attack, on_defend, on_death,
        self.trigger = trigger
        self.action = action

        self.trait_play_cost = mod_play_cost
        self.trait_stats_dict = mod_stats_dict
        self.trait_upkeep_dict = mod_upkeep_dict
        self.trait_dice_stats = new_dice_stats

        self.trait_inv_args = mod_inv_args



    def __str__(self):
        return self.trait_title
