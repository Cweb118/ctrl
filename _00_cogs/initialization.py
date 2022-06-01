from discord import Interaction
import nextcord
from nextcord import guild
from _00_cogs.architecture.player_class import Player
from _00_cogs.architecture.locations_class import Region, District
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.unit_classes._unit_kits import unit_kits_dict
from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict
from nextcord import slash_command
from nextcord.ext import commands
from _01_functions import say
from _02_global_dicts import theJar

guilds = [588095612436742173, 778448646642728991]


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="initplayers", guild_ids=guilds)
    async def initPlayers(self, ctx):
        playerRole = nextcord.utils.get(ctx.guild.roles, name="player")
        for member in playerRole.members:
            theJar['players'][member.id]=(Player(member, allegiance='Camp'))
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

    @slash_command(name="init", guild_ids=guilds)
    async def init_c(self, ctx: Interaction):

        for key in theJar['players'].keys():
            player = theJar['players'][key]
            player.inventory.addResource(theJar['resources']['Water'], 10)
            player.inventory.addResource(theJar['resources']['Food'], 10)
            player.inventory.addResource(theJar['resources']['Metal'], 10)
            player.inventory.addResource(theJar['resources']['Wood'], 10)

            #player.addCard(building_kits_dict['wooden_wall'], 'building')
            #for unit_kit in ['Knight', 'Scout', 'Ranger', 'Warrior']:
                #player.addCard(unit_kits_dict[unit_kit], 'unit')

        Region("Range", guild=ctx.guild)
        #name, region_name, size, paths=None
        District('Home', 'Range', 'medium', guild=ctx.guild)
        shooting = District('Shooting', 'Range', 'small', 'Home,', guild=ctx.guild)
        cattle = District('Cattle', 'Range', 'large', 'Home,', guild=ctx.guild)

        cattle.inventory.addResource(theJar['resources']['Food'], 50)
        cattle.inventory.addCard(Unit(*unit_kits_dict['Worker']), 'unit')
        cattle.inventory.addCard(Unit(*unit_kits_dict['Worker']), 'unit')
        shooting.inventory.addCard(Unit(*unit_kits_dict['Warrior']), 'unit')

        report = "Initilization Complete."
        await say(ctx,report)



def setup(bot):
    bot.add_cog(PlayerCog(bot))
