from nextcord import guild, member
from _00_cogs.mechanics.resource_class import resource_dict
from _02_global_dicts import player_dict

class Inventory():
    def __init__(self, owner, cards = None, resources = None):
        self._owner = owner

        if cards == None and resources == None:
            self._cards = []
            self._resources = {
                #instance:quantity
            }
            for key in resource_dict.keys():
                resource = resource_dict[key]
                try:
                    self._resources[resource]
                except:
                    self._resources[resource] = 0
        else:
            self._cards = cards
            self._resources = resources


    def addCard(self,card):
        self._cards.append(card)

    def delCard(self, card_number):
        del self._cards[card_number-1]

    def moveCard(self, card_number, new_owner):
        card = self._cards[card_number-1]
        new_player = player_dict[new_owner.id]
        new_player.inventory.addCard(card)
        del self._cards[card_number-1]

        report = "Your "+str(card)+" has been given to "+new_owner.display_name+"!"
        return report

    def addResource(self, resource, quantity):
        new_val = self._resources[resource] + quantity
        if new_val >= 0:
            self._resources[resource] = new_val
            report = True
        else:
            report = False
        return report

    def __str__(self):
        report = self._owner.display_name+"'s Inventory"
        return report

    def report(self):
        report = "-----"+str(self)+"-----\n\n--Resources:\n"

        for resource in self._resources.keys():
            report += "-"+str(resource)+": "+str(self._resources[resource])+"\n"

        report += "\n--Cards:\n"
        for card in self._cards:
            report += "-"+str(card)+" ("+card.status+")\n"

        return report

    def cardReport(self, card_number):
        card = self._cards[card_number-1]
        return card.report()
    
    #checks to make sure object has been reinstated after unpickling
    def validate(self):
        if self._owner == None:
            raise Exception("Inventory was not reinstated after unpickling.")
    def reinstate(self, bot):
        guild = bot.get_guild(self._guildID)
        self._owner = guild.get_member(self._memberID)
    #getters
    @property
    def owner(self):
        self.validate()
        return self._owner
    @property
    def resources(self):
        self.validate()
        return self._resources
    @property
    def cards(self):
        self.validate()
        return self._cards
