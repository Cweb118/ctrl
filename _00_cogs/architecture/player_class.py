import nextcord
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory

class Player():
    def __init__(self, member, memberID):
        self.member = member
        self._memberID = memberID #int
        self.guild = member.guild
        self.channel = ""
        self.createPrivateChannel.start()
        self.inventory = Inventory(self, rcap=999, u_cap=99, b_cap=99) #Inventory Instance
        self.location = "" #Location instance
    
    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        category = nextcord.utils.get(self.guild.categories, name='Players')
        overwrites = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self.member: nextcord.PermissionOverwrite(read_messages=True)
        }
        topic =  "Private Discussion"
        channelNames = (channel.name for channel in self.guild.channels)
        if (self.member.name).lower().replace(" ", "-") not in channelNames:
            self.channel = await self.guild.create_text_channel(name=self.member.name, topic=topic, overwrites=overwrites, category=category)


    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self.channel.delete()
    
    def delPrivateChannel(self):
        self.__delPrivateChannel.start()

    def getChannelID(self):
        return self.channel.id

