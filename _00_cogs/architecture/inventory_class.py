from _00_cogs.mechanics.resource_class import resource_dict
from _02_global_dicts import player_dict

class Inventory():
    def __init__(self, owner):
        self.owner = owner

        self.cards = []
        self.resources = {
            #instance:quantity
        }
        for key in resource_dict.keys():
            resource = resource_dict[key]
            try:
                self.resources[resource]
            except:
                self.resources[resource] = 0


    def addCard(self,card):
        self.cards.append(card)

    def delCard(self, card_number):
        del self.cards[card_number]

    def moveCard(self, card_number, new_owner):
        card = self.cards[card_number]
        new_player = player_dict[new_owner.id]
        new_player.inventory.addCard(card)
        del self.cards[card_number]

        report = "Your "+str(card)+" has been given to "+new_owner.display_name+"!"
        return report

    def setResource(self, resource_name, quantity):
        resource = resource_dict[resource_name]
        new_val = self.resources[resource] + quantity
        if new_val >= 0:
            self.resources[resource] = new_val
            report = True
        else:
            report = False
        return report

    def __str__(self):
        report = self.owner.display_name+"'s Inventory"
        return report

    def report(self):
        report = "-----"+str(self)+"-----\n\n--Resources:\n"

        for resource in self.resources.keys():
            report += "-"+str(resource)+": "+str(self.resources[resource])+"\n"

        report += "\n\n--Cards:\n"
        for card in self.cards:
            report += "-"+str(card)+" ("+card.status+")\n"

        return report

    def cardReport(self, card_number):
        card = self.cards[card_number-1]
        return card.report()
