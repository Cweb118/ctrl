from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics._cards_class import Card
from _00_cogs.mechanics.trait_classes.__trait_parent_class import Trait
from _00_cogs.mechanics.trait_classes._trait_kits import trait_kits_dict

from _00_cogs.architecture.inventory_class import Inventory
from _02_global_dicts import player_dict, resource_dict


class Unit(Card):
    def __init__(self, owner, title, description, inv_args, traits, play_cost, stats, upkeep_dict, dice_stats):
        inv_args = [owner]+inv_args
        super().__init__(owner, title, description, inv_args=inv_args, play_cost=play_cost)

        self.stats = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Endurance':stats['endurance'],
            'Fortitude':stats['fortitude']
        }
        self.statcaps = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Endurance':stats['endurance'],
            'Fortitude':stats['fortitude']
        }

        self.upkeep = {}
        self.die_list = dice_stats
        self.die_set = Dice(dice_stats)

        for key in upkeep_dict.keys():
            resource = resource_dict[key]
            self.upkeep[resource] = upkeep_dict[key]

        self.trait_list = traits
        self.traits = {
            'on_play': [],
            'on_work': [],
            'on_move': [],

            'on_attack': [],
            'on_defend': [],
            'on_death': [],
        }
        for trait in traits:
            self.addTrait(trait)

    def setNick(self, nick):
        self.title = self.title+" \""+nick+"\""

    def setStat(self, stat, quantity):
        self.stats[stat] += quantity
        if self.stats[stat] < 0:
            self.stats[stat] = 0

    def setHealth(self, quantity):
        self.setStat('Health', quantity)
        if self.stats['Health'] <= 0:
            self.status = "DEAD"
            report = "Your "+str(self)+' has died.'
        else:
            report = "Your "+str(self)+' now has '+str(self.stats['Health'])+' Health.'
        return report

    def addTrait(self, trait):
        trait = Trait(*trait_kits_dict[trait])
        if trait.trait_title not in self.title:
            self.title = trait.trait_title +" "+self.title
        if trait.trait_stats_dict:
            for mod_stat in trait.trait_stats_dict.keys():
                value = trait.trait_stats_dict[mod_stat]
                self.stats[mod_stat] += value
                self.statcaps[mod_stat] += value
        if trait.trait_play_cost:
            for mod_cost in trait.trait_play_cost.keys():
                value = trait.trait_play_cost[mod_cost]
                try:
                    self.upkeep[mod_cost] += value
                except:
                    self.upkeep[mod_cost] = value
        if trait.trait_upkeep_dict:
            for mod_upkeep in trait.trait_upkeep_dict.keys():
                resource = resource_dict[mod_upkeep]
                value = trait.trait_upkeep_dict[mod_upkeep]
                try:
                    self.upkeep[resource] += value
                except:
                    self.upkeep[resource] = value
        if trait.trait_inv_args:
            inv = self.inventory
            for key in trait.trait_inv_args.keys():
                value = trait.trait_inv_args[key]
                if key == 'cont':
                    try:
                        inv.cont += value
                    except:
                        inv.cont = value
                elif key == "cap":
                    for type in value.keys():
                        mod = value[type]
                        try:
                            inv.cap[type] += mod
                        except:
                            inv.cap[type] = mod
                elif key == "slotcap":
                    for type in value.keys():
                        mod = value[type]
                        try:
                            inv.slotcap[type] += mod
                        except:
                            inv.slotcap[type] = mod
                else:
                    print("ERROR: Invalid inventory constraint.")
        if trait.trait_dice_stats:
            new_set = self.die_list + trait.trait_dice_stats
            self.die_list = new_set
            self.die_set = Dice(new_set)
        self.traits[trait.trigger].append(trait)


    def addCard(self, card_kit, card_type):
        inv = self.inventory
        can_add = inv.capMathCard(card_type)
        if can_add == True:
            card = None
            kit = [self]+card_kit
            if card_type == 'unit':
                card = Unit(*kit)
            elif card_type == 'building':
                #card = Building(*kit)
                print("no")
            if card:
                inv.cards[card_type].append(card)
            else:
                can_add = False
        return can_add

    def harvest(self):
        if self.status == "Played":
            #player = player_dict[self.owner.id]
            f = 0
            for resource in self.upkeep.keys():
                quantity = self.upkeep[resource]
                i = 0
                while i < quantity:
                    if not self.inventory.addResource(resource, -1):
                        self.setStat('Defense', -1)
                        f += 1
                    i += 1
            if self.stats['Defense'] > 0:
                def_report = "Your "+str(self)+' has lost '+str(f)+' Defense due to lacking required resources.'
            else:
                def_report = "Your "+str(self)+' has no Defense remaining.'
            hit, report_dict = self.die_set.roll_math(self.stats['Defense']+self.stats['Fortitude'])
            if hit:
                health_report = self.setHealth(-1)
            else:
                health_report = "Your "+str(self)+' has sustained no damage.'

            report = "-----"+str(self)+" Upkeep Results-----\n\n"+\
                         "Rolled: "+str(self)+", "+str(self.die_set)+"\n"+\
                         "Rolls: "+str(report_dict['rolls'])+"\n"+\
                         "Defense + Fortitude: "+str(report_dict['threshold'])+"\n"+\
                         "Damage Taken: "+str(report_dict['hit_count'])+"\n\n"+\
                         def_report+"\n"+\
                         health_report

            return report

    def __str__(self):
        return self.title

    def report(self):
        report = "-----Unit Report-----\n"+\
                 "\nTitle: "+self.title+\
                 "\nDescription: "+self.description+\
                 "\nStatus: "+str(self.status)+\
                 "\nTraits: "+str(self.trait_list)+\
                 "\nStats: "
        for key in self.stats.keys():
            value = self.stats[key]
            cap = self.statcaps[key]
            report += str(value)+"/"+str(cap)+" "+str(key)+", "
        report = report[:-2]

        report += "\nUpkeep: "
        for key in self.upkeep.keys():
            value = self.upkeep[key]
            report += str(value)+" "+str(key) +", "
        report = report[:-2]

        report += "\nDie Set: "+str(self.die_set)

        report += "\n\n"+self.inventory.report()
        return report




#upkeep_quantity: Int
#upkeep_obj: Item/Unit instance

#output_quantity: Int
#output_obj: Item/Unit instance

#catylist_quantity: Int
#catylist_obj: Item/Unit instance
