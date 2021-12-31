from _00_cogs.architecture.inventory_class import Inventory

#-----attributes-----
class Card():
    def __init__(self, owner, title, description, inv_args=None, traits=None, play_cost=None):
        self.title = title
        self.description = description
        self.owner = owner

        self.status = "Held"

        self.traits = traits
        self.play_cost = play_cost
        #Item:quantity

        if inv_args:
            self.inventory = Inventory(*inv_args)


    def toggleStatus(self):
        if self.status == "Held":
            self.status = "Played"
        elif self.status == "Played":
            self.status = "Held"

    def toggleLife(self):
        if self.status == "DEAD":
            self.status = "Held"

    def addTrait(self, trait):
        if trait not in self.traits:
            self.traits.append(trait)

    def delTrait(self, trait):
        if trait in self.traits:
            self.traits.remove(trait)
