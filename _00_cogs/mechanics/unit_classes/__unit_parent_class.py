from _00_cogs.mechanics.dice_class import Dice
#Inherits from: Card

class Unit():
    def __init__(self, owner, title, description, attack, defence, endurance, fortitude, dice_stats):
        self.title = title
        self.description = description
        self.owner = owner

        self.stats = {
            'attack':attack,
            'defence':defence,
            'endurance':endurance,
            'fortitude':fortitude
        }

        self.die_set = Dice(*dice_stats)

    def __str__(self):
        report = "Title: "+self.title+\
                 "\nDescription: "+self.description+\
                 "\nOwner: "+str(self.owner)+\
                 "\nStats: "+str(self.stats)+\
                 "\nDie Set: "+str(self.die_set)
        return report

    def mod_stat(self, stat, quantity):
        self.stats[stat] += quantity

#Title: Str
#Description: Str

#Attack: Int
#Defence: Int
#Endurance: Int [Movement]
#Fortitude: Int [Upkeep success int]

#Race: Race instance
#Knows: Str [Age Technology Type(s)]
#Affinity: Str

#Die: Dice instance

#upkeep_quantity: Int
#upkeep_obj: Item/Unit instance

#output_quantity: Int
#output_obj: Item/Unit instance

#catylist_quantity: Int
#catylist_obj: Item/Unit instance
