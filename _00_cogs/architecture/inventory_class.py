from _00_cogs.mechanics.resource_class import resource_dict

class Inventory():
    def __init__(self, owner):
        self.owner = owner

        self.cards = []
        self.resources = {
            #instance:quantity
            resource_dict['influence']:2
        }

    def addCard(self,card):
        self.cards.append(card)

    def __str__(self):
        cardstr = [str(i) for i in self.cards]
        report = "Title: "+self.owner.display_name+\
                 "\nCards: "+str(cardstr)+\
                 "\nResources: "+str(self.resources)
        return report
