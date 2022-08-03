import asyncio

from discord import Interaction
import nextcord
from nextcord import guild

from _00_cogs.architecture.character_class import Character
from _00_cogs.architecture.factions_class import init_factions
from _00_cogs.architecture.kits.faction_kits import faction_kits_dict
from _00_cogs.architecture.kits.character_kits import character_kits_dict
from _00_cogs.architecture.player_class import Player
from _00_cogs.architecture.locations_class import Region, District
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict
from nextcord import slash_command
from nextcord.ext import commands

from _00_cogs.themap import TheMap
from _01_functions import say
from _02_global_dicts import theJar

guilds = [588095612436742173, 778448646642728991]

class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def playerInit(self, ctx):
        playerRole = nextcord.utils.get(ctx.guild.roles, name="player")
        for member in playerRole.members:
            theJar['players'][member.id]=(Player(member))
            if member.id != 161520114657656832:
                charkit = character_kits_dict[member.id]
                ch = Character(*charkit)
                await ch.setFaction()
            else:
                print('no charkit for '+member.display_name)
        await ctx.send("Players Initialized and Channels Created.")
    
    @slash_command(name="listplayers", guild_ids=guilds)
    async def listplayers(self, ctx):
        if len(theJar['players']) == 0:
            await ctx.send("There are no players :(")
            return
        for key in theJar['players'].keys():
            await ctx.send(theJar['players'][key].member.name)
    
    @slash_command(name="deleteplayers", guild_ids=guilds)
    async def deletePlayers(self, ctx):
        for snowflake in theJar['players'].keys():
            theJar['players'][snowflake].delPrivateChannel()
            del theJar['players'][snowflake]
        await ctx.send("Channels Deleted!")

    @slash_command(name="deletechannels", guild_ids=guilds)
    async def deletechannels(self, ctx):
        for channel in ctx.guild.channels:
            #What is happening here lol
            if channel.name == "jamsspinle" or channel.name == "the-cartographer":
                print("Match:", channel)
                await channel.delete()
            else:
                print("Not a match:", channel)

    #For testing
    @commands.command(name="print")
    async def print_c(self, ctx, name):
        match name:
            case "districts":
                await ctx.send(theJar['districts'])
            case "resources":
                await ctx.send(theJar['resources'])
            case "players":
                await ctx.send(theJar['players'])
            case "regions":
                await ctx.send(theJar['regions'])
            case _:
                await ctx.send("invalid input")

    @slash_command(name="init_game", guild_ids=guilds)
    async def init_c(self, ctx: Interaction):
        #INIT ORDER: Factions > Map > Players > Characters
        await init_factions(faction_kits_dict, ctx.guild)
        print(theJar['factions'])
        await TheMap(self.bot).reloadMap(ctx.guild)
        await asyncio.sleep(1)
        await self.playerInit(ctx)

        #for key in theJar['players'].keys():
            #player = theJar['players'][key]
            #player.inventory.addResource(theJar['resources']['Water'], 10)
            #player.inventory.addResource(theJar['resources']['Food'], 10)
            #player.inventory.addResource(theJar['resources']['Metal'], 10)
            #player.inventory.addResource(theJar['resources']['Wood'], 10)

        #Region("Range", guild=ctx.guild)
        #name, region_name, size, paths=None
        #District('Home', 'Range', 'huge', guild=ctx.guild)
        #District('Shooting', 'Range', 'small', ['Home'], guild=ctx.guild)
        #District('Cattle', 'Range', 'medium', ['Home'], guild=ctx.guild)
        #District('Free', 'Range', 'large', ['Cattle'], guild=ctx.guild)

        report = "Initialization Complete."
        await say(ctx,report)

def setup(bot):
    bot.add_cog(PlayerCog(bot))
