import nextcord
from nextcord import guild
from _00_cogs.architecture.player_class import Player
from nextcord import slash_command
from nextcord.ext import commands
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

def setup(bot):
    bot.add_cog(PlayerCog(bot))
