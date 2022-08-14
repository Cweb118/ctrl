from nextcord import slash_command
from nextcord.ext import commands

from _00_cogs.architecture.channels_class import Channel
from _02_global_dicts import theJar
from _00_cogs.architecture.locations_class import District, Region

class TheMap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.district_map = {
            'The Core':['The Core', 'The City of Barheim', 'large', []],
            'The Threshold':['The Threshold', 'The City of Barheim', 'small', ['The Core']],


            'The Shores':['The Shores', 'Levyt Cliffside', 'medium', []],
            'Yavar':['Yavar', 'Yavari Domain', 'huge', ['The Shores']],
        }

        self.district_map_PENDING = {
            #[name, region_name, size, path_list]
            'The Core':['The Core', 'The City of Barheim', 'large', ['The Threshold']],
            'The Threshold':['The Threshold', 'The City of Barheim', 'small', ['The Foot of Barheim', 'The Core']],

            'The Foot of Barheim':['The Foot of Barheim', 'Greven Taiga', 'small', ['The Frigid Quiet', 'The Threshold']],
            #'The Frigid Quiet':['The Frigid Quiet', 'Greven Taiga', 'large', ['The Treeline', 'The Foot of Barheim']],
            'The Treeline':['The Treeline', 'Greven Taiga', 'medium', ['The Overlook', 'The Frigid Quiet']],

            'The Overlook':['The Overlook', 'Levyt Cliffside', 'small', ['The Rise','The Treeline']],
            'The Rise':['The Rise', 'Levyt Cliffside', 'tiny', ['The Shores','The Overlook']],

            'The Shores':['The Shores', 'Levyt Cliffside', 'medium', ['Yavar','The Rise']],
            'Yavar':['Yavar', 'Yavari Domain', 'huge', ['The Shores']],
        }

    async def reloadMap(self, guild):
        ex = await Channel(guild, 'explore-log', 'control').init()
        theJar['control']['explore-log'] = ex
        for key in self.district_map.keys():
            if self.district_map[key][1] not in theJar['regions'].keys():
                await Region(self.district_map[key][1], guild=guild).init()
            if key not in theJar['districts'].keys():
                await District(*self.district_map[key], guild=guild).init()



def setup(bot):
    bot.add_cog(TheMap(bot))
