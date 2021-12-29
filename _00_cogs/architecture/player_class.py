import nextcord
from nextcord.ext import tasks

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

