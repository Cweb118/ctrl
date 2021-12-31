from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics._cards_class import Card
from _00_cogs.architecture.inventory_class import Inventory
from _02_global_dicts import player_dict, resource_dict


class Unit(Card):
    def __init__(self, owner, title, description, inv_args, traits, play_cost, attack, defence, endurance, fortitude, upkeep_dict, dice_stats):
        inv_args = [owner]+inv_args
        super().__init__(owner, title, description, inv_args=inv_args, traits=traits, play_cost=play_cost)

        self.stats = {
            'Attack':attack,
            'Defense':defence,
            'Endurance':endurance,
            'Fortitude':fortitude
        }
        self.upkeep = {}
        self.die_set = Dice(*dice_stats)

        for key in upkeep_dict.keys():
            resource = resource_dict[key]
            self.upkeep[resource] = upkeep_dict[key]

        #owner.inventory.addCard(self, 'unit')

    def setStat(self, stat, quantity):
        self.stats[stat] += quantity
        if self.stats[stat] < 0:
            self.stats[stat] = 0

    def setHealth(self, quantity):
        self.setStat('Defense', quantity)
        if self.stats['Defense'] <= 0:
            self.status = "DEAD"
            report = "Your "+str(self)+' has died.'
        else:
            report = "Your "+str(self)+' now has '+str(self.stats['Defense'])+' Defense.'
        return report

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
        #if self.status == "Played"
        player = player_dict[self.owner.id]
        f = 0
        for resource in self.upkeep.keys():
            quantity = self.upkeep[resource]
            i = 0
            while i < quantity:
                if not player.inventory.addResource(resource, -1):
                    self.setStat('Fortitude', -1)
                    f += 1
                i += 1
        fort_report = "Your "+str(self)+' has lost '+str(f)+' fortitude due to lacking required resources.'
        hit, report_dict = self.die_set.roll_math(self.stats['Fortitude'])
        if hit:
            health_report = self.setHealth(-1)
        else:
            health_report = "Your "+str(self)+' has sustained no damage.'

        report = "-----"+str(self)+" Upkeep Results-----\n\n"+\
                     "Rolled: "+str(self)+", "+str(self.die_set)+"\n"+\
                     "Rolls: "+str(report_dict['rolls'])+"\n"+\
                     "Fortitude: "+str(report_dict['threshold'])+"\n"+\
                     "Damage Taken: "+str(report_dict['hit_count'])+"\n\n"+\
                     fort_report+"\n"+\
                     health_report

        return report

    def __str__(self):
        return self.title

    def report(self):
        report = "-----Unit Report-----\n"+\
                 "\nTitle: "+self.title+\
                 "\nDescription: "+self.description+\
                 "\nStatus: "+str(self.status)+\
                 "\nTraits: "+str(self.traits)+\
                 "\nStats: "
        for key in self.stats.keys():
            value = self.stats[key]
            report += str(value)+" "+str(key) +", "
        report = report[:-1]

        report += "\nUpkeep: "
        for key in self.upkeep.keys():
            value = self.upkeep[key]
            report += str(value)+" "+str(key) +", "
        report = report[:-2]

        report += "\nDie Set: "+str(self.die_set)
        return report




#upkeep_quantity: Int
#upkeep_obj: Item/Unit instance

#output_quantity: Int
#output_obj: Item/Unit instance

#catylist_quantity: Int
#catylist_obj: Item/Unit instance
