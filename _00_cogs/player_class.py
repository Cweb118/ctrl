import asyncio
import nextcord
import time
from nextcord import slash_command
from nextcord import player
from nextcord import guild
from nextcord.ext import commands

guilds = [588095612436742173, 778448646642728991]
playerList = []

class Player():
    def __init__(self, member, bot):
        self.bot = bot
        self.member = member
        self.guild = member.guild
        self.channel = ""
        self.createPrivateChannel()
    
    def createPrivateChannel(self):
        future = asyncio.run_coroutine_threadsafe(self.guild.create_text_channel(self.member.name), self.bot.loop)
        print("created")
        print(future.result())
    
    def delPrivateChannel(self):
        self.channel.delete()

    def getChannelID(self):
        return self.channelID


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="initplayers", guild_ids=guilds)
    async def initPlayers(self, ctx):
        global playerList
        playerRole = nextcord.utils.get(ctx.guild.roles, name="player")

        for member in playerRole.members:
            print(member)
            playerList.append(Player(member, self.bot))
        await ctx.send("Players Initialized and Channels Created.")
    
    @slash_command(name="deleteplayers", guild_ids=guilds)
    async def deletePlayers(self, ctx):
        global playerList
        
        for player in playerList:
            player.delPrivateChannel()
        await ctx.send("Channels Deleted!")

def setup(bot):
    bot.add_cog(PlayerCog(bot))
