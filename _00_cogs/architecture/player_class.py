import nextcord
from nextcord import guild
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
#from _00_cogs.mechanics.unit_classes.__building_parent_class import Building

class Player():
    def __init__(self, member, memberID = None, guildID = None, invDict = None):
        self._username = member.display_name
        self._member = member
        self._invDict = invDict

        if self._member != None:
            self._memberID = member.id
            self._guildID = member.guild.id
        elif memberID != None and guildID != None:
            self._memberID = memberID
            self._guildID = guildID
        else:
            raise TypeError("Player must be constructed with a member object or memberID and guildID.")

        if member != None:
            self._guild = member.guild
        else:
            self._guild = None

        self._channel = ""
        self.createPrivateChannel.start()
        """
        if invDict == None:
            self._inventory = Inventory(member)
        else:
            self._inventory = None
        """
        self._inventory = Inventory(self, r_cap=1000, u_cap=100, b_cap=100) #Inventory Instance
        self._location = "" #Location instance

    def __reduce__(self):
        return(self.__class__, (None, self.memberID, self.guildID, {"cards" : self._inventory.cards, "resources" : self._inventory.resources}))


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

        channelNames = (channel.name for channel in self.guild.channels)
        if (self.member.name).lower().replace(" ", "-") not in channelNames:
            self._channel = await self.guild.create_text_channel(name=self.member.name, topic=topic, overwrites=overwrites, category=category)

    def addCard(self, card_kit, card_type):
        inv = self._inventory
        can_add = inv.capMathCard(card_type)
        if can_add == True:
            card = None
            kit = [self]+card_kit
            if card_type == 'unit':
                card = Unit(*kit)
            elif card_type == 'building':
                #card = Building(*kit)
                print("no")
            if card:
                inv.cards[card_type].append(card)
            else:
                can_add = False
        return can_add

    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self._channel.delete()
    
    def delPrivateChannel(self):
        self.__delPrivateChannel.start()

    def reinstate(self, bot):
        self._guild = bot.get_guild(self._guildID)
        self._member = self._guild.get_member(self._memberID)
        #self._inventory = Inventory(self._member, cards=self._invDict["cards"], resources=self._invDict["resources"])


    def __str__(self):
        return self._username


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
