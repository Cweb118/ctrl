from _00_cogs.mechanics._cards_class import Card

class Building(Card):
    def __init__(self, owner, title, description, inv_args, traits, play_cost, stats, input_dict, output_dict, cat_dict):
        inv_args = [self]+inv_args
        super().__init__(owner, title, description, inv_args=inv_args, play_cost=play_cost)

        self.stats = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Size':stats['size'],

        }
        self.statcaps = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Size':stats['size'],
        }
        self.trait_list = traits

        self.input = input_dict
        self.output = output_dict
        self.catalyst = cat_dict

        input = {}

    def setStat(self, stat, quantity):
        self.stats[stat] += quantity
        if self.stats[stat] < 0:
            self.stats[stat] = 0
        return self.stats[stat]


    def setHealth(self, quantity):
        self.setStat('Health', quantity)
        if self.stats['Health'] <= 0:
            self.status = "DESTROYED"
            report = "The "+str(self)+' has been destroyed.'
        else:
            report = "The "+str(self)+' now has '+str(self.stats['Health'])+' Health.'
        return report

    def dmg(self, attack_value):
        if self.stats['Defense'] > 0:
            new_def_def = self.setStat('Defense', -attack_value)
            health_rep = "The "+str(self)+"'s Defense has been lowered to "+str(new_def_def)
        else:
            health_rep = self.setHealth(-attack_value)
        return health_rep

    def __str__(self):
        return self.title

    def report(self):
        report = "-----Building Report-----\n"+\
                 "\nTitle: "+self.title+\
                 "\nDescription: "+self.description+\
                 "\nStatus: "+str(self.status)+\
                 "\nLocation: "+str(self.location)+\
                 "\nTraits: "+str(self.trait_list)+\
                 "\nStats: "
        for key in self.stats.keys():
            value = self.stats[key]
            cap = self.statcaps[key]
            report += str(value)+"/"+str(cap)+" "+str(key)+", "
        report = report[:-2]

        """
        report += "\nUpkeep: "
        for key in self.upkeep.keys():
            value = self.upkeep[key]
            report += str(value)+" "+str(key) +", "
        report = report[:-2]
        """


        report += "\n\n"+self.inventory.report()
        return report
#Inherits from: Card

#Name: Str
#Description: Str

#Attack: Int
#Defence: Int
#Size: Int
#Age: Str
#Affinity: Str

#input_quantity: Int
#input_obj: Item/Unit instance

#output_quantity: Int
#output_obj: Item/Unit instance

#catylist_quantity: Int
#catylist_obj: Item/Unit instance

