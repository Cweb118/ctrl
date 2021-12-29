from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics._cards_class import Card
from _00_cogs.initialization import player_dict

class Unit(Card):
    def __init__(self, owner, title, description, attack, defence, endurance, fortitude, dice_stats):
        super().__init__(owner, title, description)

        self.stats = {
            'attack':attack,
            'defence':defence,
            'endurance':endurance,
            'fortitude':fortitude
        }

        self.die_set = Dice(*dice_stats)

        player = player_dict[owner.id]
        player.inventory.addCard(self)

    def __str__(self):
        report = "Title: "+self.title+\
                 "\nDescription: "+self.description+\
                 "\nStatus: "+str(self.status)+\
                 "\nTraits: "+str(self.traits)+\
                 "\nStats: "+str(self.stats)+\
                 "\nDie Set: "+str(self.die_set)
        return report

    def setStat(self, stat, quantity):
        self.stats[stat] += quantity


#upkeep_quantity: Int
#upkeep_obj: Item/Unit instance

#output_quantity: Int
#output_obj: Item/Unit instance

#catylist_quantity: Int
#catylist_obj: Item/Unit instance
