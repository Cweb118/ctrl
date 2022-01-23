from _00_cogs.architecture.inventory_class import Inventory
from _00_cogs.mechanics.building_classes.__building_parent_class import Building
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _02_global_dicts import fab_dict


class Fab():
    def __init__(self, owner, title, starter_location = None, allegiance = None):
        self.owner = owner
        self.title = title
        self.location = starter_location
        self._allegiance = allegiance
        self._inventory = Inventory(self, r_cap=1000, u_cap=100, b_cap=100)

        fab_dict[str(self)] = self


    def addCard(self, card_kit, card_type):
        inv = self._inventory
        can_add = inv.capMathCard(card_type)
        if can_add == True:
            card = None
            kit = [self]+card_kit
            if card_type == 'unit':
                card = Unit(*kit)
            elif card_type == 'building':
                card = Building(*kit)
            if card:
                inv.cards[card_type].append(card)
            else:
                can_add = False
        return can_add, card



    def __str__(self):
        return self.title

    def report(self):
        report = "------"+str(self)+"------\n"
        report += "\n-Owner: "+str(self.owner)
        report += "\n-Location: "+str(self.location)
        report += "\n-Allegiance: "+str(self._allegiance)
        inv_rep = self._inventory.report()
        report += "\n\n"+inv_rep
        return report
