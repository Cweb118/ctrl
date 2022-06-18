class Trait():
    def __init__(self, name, description, type, certs, trigger, action, mod_inv_args, mod_play_cost, mod_stats_dict, mod_initiative, mod_threat, mod_upkeep_dict, new_dice_stats):

        self.trait_title = name
        self.trait_description = description
        self.trait_type = type
        #triggers: on_act, on_play, on_work, on_move, on_battle, on_attack, on_defend, on_death, on_harvest, on_refresh
        self.trigger = trigger
        self.trait_certs = certs
        #action: the class which holds the trait code (in trait_classes.py)
        self.action = action

        self.trait_play_cost = mod_play_cost
        self.trait_stats_dict = mod_stats_dict
        self.trait_initiative = mod_initiative
        self.trait_threat = mod_threat
        self.trait_upkeep_dict = mod_upkeep_dict
        self.trait_dice_stats = new_dice_stats

        self.trait_inv_args = mod_inv_args



    def __str__(self):
        return self.trait_title

    def report(self):
        fields = []
        title = "-----"+self.trait_title+"-----"

        report = self.trait_description

        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] =  "\n- Status: "+str(self.status)+\
                             "\n- Location: "+str(self.location)+\
                             "\n- Traits: "+str(self.trait_list)
        info_rep['value'] += "\n- Die Set: "+str(self.trait_die_set)
        info_rep['value'] += "\n- Upkeep: "
        for key in self.trait_upkeep_dict.keys():
            value = self.trait_upkeep_dict[key]
            info_rep['value'] += str(value)+" "+str(key) +", "
        info_rep['value'] = info_rep['value'][:-2]
        fields.append(info_rep)

        stats_rep = {'inline':True}
        stats_rep['title'] = "-- Stats:"
        stats_rep['value'] = ''
        for key in self.trait_stats.keys():
            value = self.trait_stats[key]
            cap = self.trait_statcaps[key]
            stats_rep['value'] += "- "+str(key)+" "+str(value)+"/"+str(cap)+"\n"
        stats_rep['value'] = stats_rep['value'][:-1]
        fields.append(stats_rep)

        return report, title, fields
