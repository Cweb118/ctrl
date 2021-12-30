from _00_cogs.mechanics.resource_class import resource_dict

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

    def setResource(self, resource_name, quantity):
        resource = resource_dict[resource_name]
        new_val = self.resources[resource] + quantity
        if new_val >= 0:
            self.resources[resource] = new_val

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
