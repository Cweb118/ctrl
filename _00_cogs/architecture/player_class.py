import nextcord
from nextcord import guild
from nextcord.ext import tasks
from _02_global_dicts import resource_dict
from _00_cogs.architecture.inventory_class import Inventory
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.building_classes.__building_parent_class import Building

class StateError(Exception):
    pass
class Player():
    def __init__(self, member, memberID = None, guildID = None, inventory = None, starter_location = None, allegiance = None):
        self._username = member.display_name
        self._member = member

        if self._member != None:
            self._username = member.display_name
            self._memberID = member.id
            self._guildID = member.guild.id
        elif memberID != None and guildID != None:
            self._username = None
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
        if inventory == None:
            self._inventory = Inventory(self, r_cap=100, u_cap=10, b_cap=10) #Inventory Instance
        else:
            self._inventory = inventory
        self.location = starter_location #Location Instance (needs to lack _!)
        self._stats = {
            #instance:quantity
            resource_dict['Influence']:20
        }
        self._statcaps = {
            #instance:cap
            resource_dict['Influence']:20
        }
        self._allegiance = allegiance
    def __reduce__(self):
        return(self.__class__, (None, self.memberID, self.guildID, self._inventory))


    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        if self._member == None or self._guild == None:
            return

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
                card = Building(*kit)
            if card:
                inv.cards[card_type].append(card)
            else:
                can_add = False
        return can_add, card

    def modStat(self, stat, quantity): #stat here is an INSTANCE (of resouce!)
        new_val = self._stats[stat] + quantity
        can_add = False
        if self._statcaps[stat]:
            if new_val >= 0:
                if new_val <= self._statcaps[stat]:
                    can_add = True
        if can_add == True:
            self._stats[stat] = new_val
        return can_add

    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self._channel.delete()
    
    def delPrivateChannel(self):
        self.__delPrivateChannel.start()

    def reinstate(self, bot):
        self._guild = bot.get_guild(self._guildID)
        self._member = self._guild.get_member(self._memberID)
        self._username = self._member.display_name


    def __str__(self):
        if self._username == None:
            raise StateError("Player Object was not initialized before use.")
        return self._username

    def report(self):
        report = "-----"+str(self)+"'s Stats-----\n\n"
        for stat in self._stats.keys():
            report += str(stat)+": "+str(self._stats[stat])+"/"+str(self._statcaps[stat])+"\n"
        return report


    #ACCESSOR

    @property
    def member(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._member

    @property
    def guild(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._guild

    @property
    def channel(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._channel
    @property
    def memberID(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._memberID
    @property
    def guildID(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._guildID
    @property
    def inventory(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._inventory

    #left for legacy support
    def getChannelID(self):
        if self._member == None or self._guild == None:
            raise StateError("Player Object was not initialized before use.")
        return self._channel.id
