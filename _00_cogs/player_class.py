import asyncio
from asyncio.tasks import Task
import nextcord
import time
from nextcord import slash_command
from nextcord import player
from nextcord import guild
from nextcord.ext import commands, tasks

guilds = [588095612436742173, 778448646642728991]
playerList = []

class Player():
    def __init__(self, member):
        self.member = member
        self.guild = member.guild
        self.channel = ""
        self.createPrivateChannel.start()
    
    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        overwrites = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self.member: nextcord.PermissionOverwrite(read_messages=True)
        }
        topic =  "Private Discussion"
        self.channel = await self.guild.create_text_channel(name=self.member.name, topic=topic, overwrites=overwrites)

    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self.channel.delete()
    
    def delPrivateChannel(self):
        self.__delPrivateChannel.start()

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
            playerList.append(Player(member))
        await ctx.send("Players Initialized and Channels Created.")
    
    @slash_command(name="deleteplayers", guild_ids=guilds)
    async def deletePlayers(self, ctx):
        global playerList
        
        for player in playerList:
            player.delPrivateChannel()
        await ctx.send("Channels Deleted!")

def setup(bot):
    bot.add_cog(PlayerCog(bot))
