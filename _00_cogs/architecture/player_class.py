import asyncio
import nextcord
from nextcord import guild
from nextcord.ext import tasks
from _02_global_dicts import theJar
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus

class StateError(Exception):
    pass
class Player():
    def __init__(self, member, memberID = None, guildID = None, inventory = None, starter_location = None, allegiance = None):
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
        self.interfaceChannel = None #Channel ID

        self.createPrivateChannel.start()
        if inventory == None:
            self._inventory = Inventory(self, r_cap=100, u_cap=10, b_cap=10) #Inventory Instance
        else:
            self._inventory = inventory
        self.location = starter_location #Location Instance (needs to lack _!)
        self._stats = {
            #instance:quantity
            theJar['resources']['Influence']:20
        }
        self._statcaps = {
            #instance:cap
            theJar['resources']['Influence']:20
        }
        self.allegiance = allegiance
        self.squads = []

        self.interfaceDirty = False

    def __reduce__(self):
        return(self.__class__, (None, self.memberID, self.guildID, self._inventory))
    
    def reinstate(self, bot):
        self._guild = bot.get_guild(self._guildID)
        self._member = self._guild.get_member(self._memberID)
        self._username = self._member.display_name


    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        if self._member == None or self._guild == None:
            return

        # Ginger: Added Interface Channel
        interfaceCategory = nextcord.utils.get(self._guild.categories, name='Interface')
        category = nextcord.utils.get(self._guild.categories, name='Players')
        interfaceOverwrites = {
            self._guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
            self._member: nextcord.PermissionOverwrite(read_messages=True)
        }
        overwrites = {
            self._guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self._member: nextcord.PermissionOverwrite(read_messages=True)
        }
        topic =  "Private Discussion"

        foundInterface = False
        foundChannel = False

        for channel in interfaceCategory.channels:
            if channel.name.lower() == self._member.name.replace(' ', '-').lower() + '_interface':
                self.interfaceChannel = channel
                foundInterface = True
        
        for channel in category.channels:
            if channel.name.lower() == self._member.name.replace(' ', '-').lower():
                self._channel = channel
                foundChannel = True
                
        if not foundInterface:
            self.interfaceChannel = await self._guild.create_text_channel(name=self._member.replace(' ', '-').name + '_interface', overwrites=interfaceOverwrites, category=interfaceCategory)            

        if not foundChannel:
            self._channel = await self._guild.create_text_channel(name=self._member.replace(' ', '-').name, topic=topic, overwrites=overwrites, category=category)

        interfaceMessages = await self.interfaceChannel.history(limit=3).flatten()
        interfaceMessages.reverse()
        if (len(interfaceMessages) < 1):
            self.squadsMessage = await Menus.squadsMenu.send(self.interfaceChannel, state={'player': self._member.id})
        else:
            self.squadsMessage = interfaceMessages[0]
        
        if (len(interfaceMessages) < 2):
            self.unitsMessage = await Menus.cardsMenu.send(self.interfaceChannel, state={'player': self._member.id, 'card_type': 'unit'})
        else:
            self.unitsMessage = interfaceMessages[1]
        
        if (len(interfaceMessages) < 3):
            self.buildingsMessage = await Menus.cardsMenu.send(self.interfaceChannel, state={'player': self.member.id, 'card_type': 'building'})
        else:
            self.buildingsMessage = interfaceMessages[2]

        self.interfaceDirty = False

    def updateInterface(self):
        self.interfaceDirty = True
    
    async def doInterfaceUpdate(self):
        self.interfaceDirty = False

        allUpdates = []

        if hasattr(self, 'squadsMessage'):
            allUpdates.append(Menus.squadsMenu.update(self.squadsMessage, newState={'player': self._member.id}))

        if hasattr(self, 'unitsMessage'):
            allUpdates.append(Menus.cardsMenu.update(self.unitsMessage, newState={'player': self.member.id, 'card_type': 'unit'}))

        if hasattr(self, 'buildingsMessage'):
            allUpdates.append(Menus.cardsMenu.update(self.buildingsMessage, newState={'player': self.member.id, 'card_type': 'building'}))

        await asyncio.gather(*allUpdates)  

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

    def __str__(self):
        if self._username == None:
            raise StateError("Player Object was not initialized before use.")
        return self._username

    def report(self):
        report = ''
        fields = []
        title = "-----"+str(self)+"-----"

        al_rep = {'inline':True}
        al_rep['title'] = "-- Alliegence:"
        al_rep['value'] = '- None'
        if self._allegiance:
            al_rep['value'] = "- "+str(self._allegiance)
        fields.append(al_rep)

        stats_rep = {'inline':True}
        stats_rep['title'] = "-- Stats:"
        stats_rep['value'] = ''
        for stat in self._stats.keys():
            stats_rep['value'] += "- "+str(stat)+": "+str(self._stats[stat])+"/"+str(self._statcaps[stat])+"\n"
        stats_rep['value'] = stats_rep['value'][:-1]
        fields.append(stats_rep)

        return report, title, fields

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
