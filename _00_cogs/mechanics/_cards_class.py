
#-----attributes-----
class Card():
    def __init__(self, owner, title, description):
        self.title = title
        self.description = description
        self.owner = owner

        self.status = "Held"
        self.traits = []

        self.cost = {
            #item:quantity
        }

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


#Owner: Player instance
#Status: enum: [Played, Held]
#Cost (to play the card): Int
#Cost (item needed): Item instance
#^ may have multiple costs
