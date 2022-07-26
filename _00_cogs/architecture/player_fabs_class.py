from _00_cogs.architecture.inventory_class import Inventory
from _02_global_dicts import theJar


class Fab():
    def __init__(self, owner, title, starter_location = None, faction = None):
        self.owner = owner
        self.title = title
        self.location = starter_location
        self.faction = faction
        self._inventory = Inventory(self, r_cap=1000, u_cap=100, b_cap=100)

        theJar['fabs'][str(self)] = self


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
        player_rep['value'] += "\n- Allegiance: "+str(self.faction)
        fields.append(player_rep)
        inv_rep, inv_title, inv_fields = self._inventory.report()
        fields += inv_fields
        return report, title, fields
