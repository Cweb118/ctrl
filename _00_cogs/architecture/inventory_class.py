from _00_cogs.mechanics.resource_class import resource_dict
from _02_global_dicts import player_dict

class Inventory():
    def __init__(self, owner, r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None):
        self.owner = owner #Player instance

        self.cont = r_cont #int
        self.cap = {
            "resource":r_cap, #int
            "unit":u_cap, #int
            "building":b_cap #int
        }
        self.slotcap = {
            "unit":u_slotcap, #int
            "building":b_slotcap #int
        }

        self.cards = {
            'units':[], #list
            'buildings':[]#list
        }
        self.resources = {
            #instance:quantity
        }
        for key in resource_dict.keys():
            resource = resource_dict[key]
            try:
                self.resources[resource]
            except:
                self.resources[resource] = 0
        self.slots = {
            "unit":[],#list
            "building":[]#list
        }

    def addCard(self,card):
        t = type(card).__name__
        can_add = False
        if self.cap[t]:
            if len(self.cards[t]) < self.cap[t]:
                can_add = True
        if can_add == True:
            self.cards[t].append(card)
        return can_add

    def delCard(self, t, card_number):
        del self.cards[t][card_number-1]

    def moveCard(self, t, card_number, new_owner_name, new_owner_id):
        card = self.cards[t][card_number-1]
        new_player = player_dict[new_owner_id]
        status = new_player.inventory.addCard(card)
        if status:
            del self.cards[card_number-1]
            report = "Your "+str(card)+"("+t+") has been given to "+new_owner_name+"!"
        else:
            report = "Error: Recipient lacks capacity for this item."
        return report

    def addResource(self, resource, quantity):
        new_val = self.resources[resource] + quantity
        can_add = False
        if self.cap['resource']:
            if new_val >= 0:
                if new_val <= self.cap['resource']:
                    if self.cont:
                        if self.resources[resource] > 0:
                            can_add = True
                        else:
                            i = 0
                            for key in self.resources.keys():
                                if self.resources[key] > 0:
                                    i += 1
                            if i < self.cont:
                                can_add = True
                    else:
                        can_add = True

        if can_add == True:
            self.resources[resource] = new_val
        return can_add

    def __str__(self):
        report = self.owner_name+"'s Inventory"
        return report

    def report(self):
        report = "-----"+str(self)+"-----\n\n--Resources:\n"

        for resource in self.resources.keys():
            report += "-"+str(resource)+": "+str(self.resources[resource])+"\n"

        report += "\n---Cards:\n"
        report += "\n--Units:\n"
        for card in self.cards['units']:
            report += "-"+str(card)+" ("+card.status+")\n"
        report += "\n--Buildings:\n"
        for card in self.cards['buildings']:
            report += "-"+str(card)+" ("+card.status+")\n"
        return report

    def cardReport(self, t, card_number):
        card = self.cards[t][card_number-1]
        return card.report()
