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
    bot = ""
    def __init__(self, bot2):
        bot = bot2
    
    @commands.command(name="save")
    async def saveAll(self, ctx):
        with open(f"{os.getcwd()}\\_01_pickle_jar\\currentSave.pkl", "wb") as file:
            pickle.dump(varsToSave, file)
    
    @commands.command(name="loadSave")
    async def loadAll(self, ctx):
        with open(f"{os.getcwd()}\\_01_pickle_jar\\currentSave.pkl", "rb") as file:
            varsToLoad = pickle.load(file)
            player_dict = varsToLoad[0]
            resource_dict = varsToLoad[1]

def setup(bot):
    bot.add_cog(PickleFactory(bot))