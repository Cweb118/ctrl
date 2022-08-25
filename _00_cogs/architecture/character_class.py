from _00_cogs.mechanics.building_classes.__building_parent_class import Building
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.architecture.kits.character_kits import character_briefs_dict
from _01_functions import say
from _02_global_dicts import theJar

#This does NOT need to be pickled
class Character():
    #i have no idea if this works pls help
    def __init__(self):
        pass

    async def init(self, player_id, char_id, location_name, faction_title, inventory_kit):
        self.player = theJar['players'][player_id]
        print(self.player)
        self.location = theJar['districts'][location_name]
        self.faction = theJar['factions'][faction_title]



        await self.location.movePlayer(self.player)
        self.player.modStat('Influence', 1)

        self.stats = inventory_kit['stats']
        self.resources = inventory_kit['resources']
        self.units = inventory_kit['units']
        self.buildings = inventory_kit['buildings']

        self.player.setStatCap('Influence', self.stats['Influence'])

        for resource_name in self.resources.keys():
            self.player.inventory.addResource(resource_name,self.resources[resource_name])

        if len(self.units) > 0:
            for unit in self.units:
                man = Unit()
                for trait in unit:
                    man.addTrait(trait)
                self.player.inventory.addCard(man, 'unit')

        if len(self.buildings) > 0:
            for building_kit in self.buildings:
                hut = Building(building_kit)
                self.player.inventory.addCard(hut, 'building')

        self.briefing = character_briefs_dict['intro']+'\n'
        try:
            self.briefing += character_briefs_dict['locations'][location_name]+'\n'
        except:
            pass
        try:
            self.briefing += character_briefs_dict['factions'][faction_title]+'\n'
        except:
            pass
        try:
            self.briefing += character_briefs_dict['characters'][char_id]+'\n'
        except:
            pass
        self.briefing += character_briefs_dict['outro']+'\n'
        await say(None, self.briefing, channel=self.player.channel)


        self.player.cast = True

    async def setFaction(self):
        await self.faction.addPlayer(self.player)
