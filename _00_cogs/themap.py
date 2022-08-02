from nextcord import slash_command
from nextcord.ext import commands
from _02_global_dicts import theJar
from _00_cogs.architecture.locations_class import District, Region

#I DONT KNOW WHY THIS IS COMMENTED OUT AAAAA
class TheMap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        """
        self.district_map = {
            'Yavar':['Yavar', 'Yavari Domain', 'huge', ['Central Yavar']],

            'The Shores':['The Shores', 'Levyt Cliffside', 'medium', ['Yavar','The Rise']],

            'The Threshold':['The Threshold', 'The City of Barheim', 'small', ['The Foot of Barheim', 'The Core']],
            'The Core':['The Core', 'The City of Barheim', 'large', ['The Threshold']],
        }

        self.district_map_PENDING = {
            #[name, region_name, size, path_list]
            'Yavar':['Yavar', 'Yavari Domain', 'huge', ['Central Yavar']],

            'The Shores':['The Shores', 'Levyt Cliffside', 'medium', ['Yavar','The Rise']],
            'The Rise':['The Rise', 'Levyt Cliffside', 'tiny', ['The Shores','The Overlook']],
            'The Overlook':['The Overlook', 'Levyt Cliffside', 'small', ['The Rise','The Treeline']],

            'The Treeline':['The Treeline', 'Greven Taiga', 'medium', ['The Overlook', 'The Frigid Quiet']],
            'The Frigid Quiet':['The Frigid Quiet', 'Greven Taiga', 'large', ['The Treeline', 'The Foot of Barheim']],
            'The Foot of Barheim':['The Foot of Barheim', 'Greven Taiga', 'small', ['The Frigid Quiet', 'The Threshold']],

            'The Threshold':['The Threshold', 'The City of Barheim', 'small', ['The Foot of Barheim', 'The Core']],
            'The Core':['The Core', 'The City of Barheim', 'large', ['The Threshold']],
        }

        for key in self.district_map.keys():
            if key not in theJar['districts'].keys():
                d=District(*self.district_map[key])
                if self.district_map[key][1] not in theJar['regions'].keys():
                    Region(self.district_map[key][1], districts=[d])
        """

def setup(bot):
    bot.add_cog(TheMap(bot))
