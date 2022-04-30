from _00_cogs.architecture.inventory_class import Inventory
from _00_cogs.mechanics.building_classes.__building_parent_class import Building
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _02_global_dicts import theJar


class Fab():
    def __init__(self, owner, title, starter_location = None, allegiance = None):
        self.owner = owner
        self.title = title
        self.location = starter_location
        self._allegiance = allegiance
        self._inventory = Inventory(self, r_cap=1000, u_cap=100, b_cap=100)

        theJar['fabs'][str(self)] = self


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

        title = "------"+str(self)+"------\n"
        report = ''
        fields = []
        player_rep = {'inline':True}
        player_rep['title'] = "-- Info:"
        player_rep['value'] = ''
        player_rep['value'] += "- Owner: "+str(self.owner)
        player_rep['value'] += "\n- Location: "+str(self.location)
        player_rep['value'] += "\n- Allegiance: "+str(self._allegiance)
        fields.append(player_rep)
        inv_rep, inv_title, inv_fields = self._inventory.report()
        fields += inv_fields
        return report, title, fields
