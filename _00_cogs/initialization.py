import nextcord
from nextcord import guild
from _00_cogs.architecture.player_class import Player
from _00_cogs.architecture.locations_class import Region, District
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.unit_classes._unit_kits import unit_kits_dict
from nextcord import slash_command
from nextcord.ext import commands
from _01_functions import say
from _02_global_dicts import player_dict, resource_dict

guilds = [588095612436742173, 778448646642728991]


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="initplayers", guild_ids=guilds)
    async def initPlayers(self, ctx):
        playerRole = nextcord.utils.get(ctx.guild.roles, name="player")
        for member in playerRole.members:

            player_dict[member.id]=(Player(member))
            player_dict[member.id].inventory.addResource(resource_dict['Influence'], 2)

        await ctx.send("Players Initialized and Channels Created.")
    
    @slash_command(name="listplayers", guild_ids=guilds)
    async def listplayers(self, ctx):
        if len(player_dict) == 0:
            await ctx.send("There are no players :(")
            return
        for key in player_dict.keys():
            await ctx.send(player_dict[key].member.name)
    
    @slash_command(name="deleteplayers", guild_ids=guilds)
    async def deletePlayers(self, ctx):
        for snowflake in player_dict.keys():
            player_dict[snowflake].delPrivateChannel()
            del player_dict[snowflake]
        await ctx.send("Channels Deleted!")

    @slash_command(name="deletechannels", guild_ids=guilds)
    async def deletechannels(self, ctx):
        for channel in ctx.guild.channels:
            if channel.name == "jamsspinle" or channel.name == "the-cartographer":
                print("Match:", channel)
                await channel.delete()
            else:
                print("Not a match:", channel)


    @commands.command(name="init", guild_ids=guilds)
    async def init_c(self, ctx):

        for key in player_dict.keys():
            player = player_dict[key]
            player.inventory.addResource(resource_dict['Water'], 10)
            player.inventory.addResource(resource_dict['Food'], 10)
            player.inventory.addResource(resource_dict['Metal'], 10)

            for unit_kit in ['worker', 'worker', 'warrior', 'scout']:
                player.addCard(unit_kits_dict[unit_kit], 'unit')

        Region("Range")
        #name, region_name, size, paths=None
        District('Home', 'Range', 'medium')
        shooting = District('Shooting', 'Range', 'small', 'Home,')
        cattle = District('Cattle', 'Range', 'large', 'Home,')

        cattle.inventory.addResource(resource_dict['Food'], 50)
        cattle.addCard(unit_kits_dict['worker'], 'unit')
        cattle.addCard(unit_kits_dict['worker'], 'unit')
        shooting.addCard(unit_kits_dict['warrior'], 'unit')

        report = "Initilization Complete."
        await say(ctx,report)



def setup(bot):
    bot.add_cog(PlayerCog(bot))
