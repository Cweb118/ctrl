from nextcord import slash_command
from nextcord.ext import commands
from _02_global_dicts import theJar
import pickle
import os

class PickleFactory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        if not os.path.isdir(f"{os.getcwd()}\\_01_pickle_jar\\"):
            os.makedirs(f"{os.getcwd()}\\_01_pickle_jar\\")

    
    @commands.command(name="save")
    async def save(self, ctx):
        for entry in theJar.keys():
                print(f"Pickling entry: {entry}...")
                with open(f"{os.getcwd()}\\_01_pickle_jar\\{entry}.pkl", "wb") as file:
                    pickle.dump(theJar[entry], file)
        await ctx.send("Finished Saving!")

    @commands.command(name="load")
    async def load(self, ctx):
        for entry in theJar:
            try:
                with open(f"{os.getcwd()}\\_01_pickle_jar\\{entry}.pkl", "rb") as file:
                    temp = pickle.load(file)
                    if entry == "districts":
                        for district in temp.values():
                            guild = self.bot.get_guild(district.channel.guild)
                            district.reconstruct(guild)
                    elif entry == "players":
                        for player in temp.values():
                            player.reconstruct(self.bot)
                    theJar[entry] = temp
                    
            except FileNotFoundError:
                print(f"File \"{entry}\" not found.")
        await ctx.send("Load Completed!")

    @commands.command(name="listDist")
    async def listdist(self, ctx):
        print(theJar['districts'])

    @commands.command(name="what")
    async def what(self, ctx):
        print(theJar["control"])

    @commands.command(name="printjar")
    async def print(self, ctx):
        print(theJar,"\n\n")
        for entry in theJar:
            print(theJar[entry])
    
    @commands.command(name="clear")
    async def clear(self, ctx):
        pass




def setup(bot):
    bot.add_cog(PickleFactory(bot))
