import nextcord
import os
from nextcord import slash_command
import pickle
from nextcord import player
from nextcord.ext import commands

"""
IMPORT ALL VARIABLES TO SAVE HERE.
"""
from _02_global_dicts import player_dict, resource_dict
varsToSave = [player_dict, resource_dict]
"""
ALSO ADD ALL VARIABLSE TO varsToSave LIST
"""

guilds = [588095612436742173, 778448646642728991]

class PickleFactory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="save")
    async def saveAll(self, ctx):
        with open(f"{os.getcwd()}\\_01_pickle_jar\\currentSave.pkl", "wb") as file:
            pickle.dump(varsToSave, file)
    
    @commands.command(name="loadSave")
    async def loadAll(self, ctx):
        with open(f"{os.getcwd()}\\_01_pickle_jar\\currentSave.pkl", "rb") as file:
            varsToLoad = pickle.load(file)
            player_dict.clear()

            for key in varsToLoad[0].keys():
                player_dict[key] = varsToLoad[0][key]
                player_dict[key].reinstate(self.bot)

def setup(bot):
    bot.add_cog(PickleFactory(bot))