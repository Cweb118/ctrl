import nextcord
from _00_cogs.architecture.player_class import Player
from nextcord import slash_command
from nextcord.ext import commands

guilds = [588095612436742173, 778448646642728991]
playerList = []

class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="initplayers", guild_ids=guilds)
    async def initPlayers(self, ctx):
        global playerList
        playerRole = nextcord.utils.get(ctx.guild.roles, name="player")

        for member in playerRole.members:
            playerList.append(Player(member))
        await ctx.send("Players Initialized and Channels Created.")
    
    @slash_command(name="deleteplayers", guild_ids=guilds)
    async def deletePlayers(self, ctx):
        global playerList
        
        for player in playerList:
            player.delPrivateChannel()
        playerList.clear()
        await ctx.send("Channels Deleted!")

def setup(bot):
    bot.add_cog(PlayerCog(bot))