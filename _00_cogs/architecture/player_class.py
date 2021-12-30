import nextcord
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory
class Player():
    def __init__(self, member, memberID, guildID):
        self._member = member
        self._memberID = memberID
        self._guildID = guildID

        if member != None:
            self._guild = member.guild
        else:
            self._guild = None

        self._channel = ""
        #self.createPrivateChannel.start()
        self._inventory = Inventory(member)
    
    def __reduce__(self):
        return(self.__class__, (None, self.memberID, self.guildID))


    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        
        category = nextcord.utils.get(self._guild.categories, name='Players')
        overwrites = {
            self._guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self._member: nextcord.PermissionOverwrite(read_messages=True)
        }
        topic =  "Private Discussion"
        channelNames = (channel.name for channel in self._guild.channels)
        if (self._member.name).lower().replace(" ", "-") not in channelNames:
            self._channel = await self._guild.create_text_channel(name=self._member.name, topic=topic, overwrites=overwrites)

    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self._channel.delete()
    
    def delPrivateChannel(self):
        self.__delPrivateChannel.start()

    def reinstate(self, bot):
        self._guild = bot.get_guild(self._guildID)
        self._member = self._guild.get_member(self._memberID)

    #ACCESSOR

    @property
    def member(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._member

    @property
    def guild(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._guild
    
    @property
    def channel(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._channel
    @property
    def memberID(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._memberID
    @property
    def guildID(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._guildID 
    @property
    def inventory(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._inventory
    
    #left for legacy support
    def getChannelID(self):
        if self._member == None or self._guild == None:
            raise Exception("Player Object was not initialized before use.")
        return self._channel.id
