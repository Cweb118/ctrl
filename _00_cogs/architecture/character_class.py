from _00_cogs.mechanics.building_classes.__building_parent_class import Building
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _02_global_dicts import theJar

#This does NOT need to be pickled
class Character():
    #i have no idea if this works pls help
    def __init__(self, player_id, faction_title, location_id, inventory_kit):
        self.player = theJar['players'][player_id]
        self.location = theJar['districts'][location_id]

        self.location.movePlayer(self.player)
        self.player.modStat(theJar['resources']['Influence'], 1)

        self.resources = inventory_kit['resources']
        self.units = inventory_kit['units']
        self.buildings = inventory_kit['buildings']

        #this is ASYNC
        self.party = theJar['parties'][faction_title]
        self.party.addPlayer(self.player)

        for resource_name in self.resources.keys():
            self.player.inventory.addResource(theJar['resources'][resource_name],self.resources[resource_name])
        if len(self.units) > 0:
            for unit in self.units:
                man = Unit()
                for trait in unit:
                    man.addTrait(trait)
                self.player.inventory.addCard(unit, 'unit')

        if len(self.buildings) > 0:
            for building in self.buildings:
                hut = Building(*building)
                self.player.inventory.addCard(hut, 'building')

        self.player.cast = True
