from typing import ValuesView
import nextcord
import os
from nextcord import slash_command
import pickle
from nextcord import player
from nextcord.ext import commands

"""
IMPORT ALL VARIABLES TO SAVE HERE.
"""
from _02_global_dicts import district_dict, region_dict, resource_dict, player_dict
varsToSave = {"player_dict" : player_dict, "resource_dict" : resource_dict, "region_dict" : region_dict, "district_dict" : district_dict}
"""
ALSO ADD ALL VARIABLSE TO varsToSave LIST
"""

guilds = [588095612436742173, 778448646642728991]

class PickleFactory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="save")
    async def saveAll(self, ctx):

        if not os.path.isdir(f"{os.getcwd()}\\_01_pickle_jar\\"):
            os.makedirs(f"{os.getcwd()}\\_01_pickle_jar\\")

        for dictKey in varsToSave.keys():
            with open(f"{os.getcwd()}\\_01_pickle_jar\\{dictKey}.pkl", "wb") as file:
                pickle.dump(varsToSave[dictKey], file)

        #with open(f"{os.getcwd()}\\_01_pickle_jar\\currentSave.pkl", "wb") as file:
        #    pickle.dump(varsToSave, file)
        
        await ctx.send("Save Created!")
    
    @commands.command(name="loadSave")
    async def loadAll(self, ctx):
            player_dict.clear()
            resource_dict.clear()
            region_dict.clear()
            district_dict.clear()

            with open(f"{os.getcwd()}\\_01_pickle_jar\\resource_dict.pkl", "rb") as file:
                resources = pickle.load(file)
                for key in resources:
                    resource_dict[key] = resources[key]

            with open(f"{os.getcwd()}\\_01_pickle_jar\\player_dict.pkl", "rb") as file:
                players = pickle.load(file)
                for key in players:
                    player_dict[key] = players[key]
                    player_dict[key].reinstate(self.bot)
            
            with open(f"{os.getcwd()}\\_01_pickle_jar\\region_dict.pkl", "rb") as file:
                regions = pickle.load(file)
                for key in regions:
                    region_dict[key] = regions[key]

            #reinstating regions
            for regionKey in region_dict.keys():
                region_dict[regionKey].reinstate(self.bot.get_guild(region_dict[regionKey].guildID))
                for district in region_dict[regionKey].districts:
                    district_dict[district.name] = district

            with open(f"{os.getcwd()}\\_01_pickle_jar\\district_dict.pkl", "rb") as file:
                districts = pickle.load(file)
                for key in districts:
                    district_dict[key] = districts[key]

            for key in district_dict.keys():
                district_dict[key].reinstate(self.bot.get_guild(district_dict[key].guildID))



            
            """
            #load resources
            for key in varsToLoad[1].keys():
                print(key, varsToLoad[1][key])
                resource_dict[key] = varsToLoad[1][key]

            #load players
            for key in varsToLoad[0].keys():
                player_dict[key] = varsToLoad[0][key]
                player_dict[key].reinstate(self.bot)
            
            #load regions
            for key in varsToLoad[2].keys():
                region_dict[key] = varsToLoad[2][key]
                await region_dict[key].reinstate(self.bot)
            
            #Load districts
            for regionKey in region_dict.keys():
                print("region:", regionKey)
                for district in region_dict[regionKey].districts:
                    print("district:", district)
                    district_dict[district.name] = district
            """
            await ctx.send("Save Loaded!")

def setup(bot):
    bot.add_cog(PickleFactory(bot))