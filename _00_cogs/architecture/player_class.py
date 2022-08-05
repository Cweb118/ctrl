import asyncio
import nextcord
from nextcord import guild
from nextcord.ext import tasks
from _02_global_dicts import theJar
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus
from .channels_class import Channel

class StateError(Exception):
    pass

class Player():
    def __init__(self, member, memberID = None, guildID = None, inventory = None, starter_location = None, faction = None):
        #flag to see if the player has been cast as a character once before
        self.cast = False

        self._member = member

        #pickle stuff (rework soon):
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

        self._channel = None
        self.interfaceChannel = None
        self.createPrivateChannel.start()

        if inventory == None:
            self._inventory = Inventory(self, r_cap=100, u_cap=20, b_cap=10) #Inventory Instance
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
        self.faction = faction
        self.reps = {}
        self.squads = []

        self.interfaceDirty = False

    def __getstate__(self):
        return ()
    def __setstate__(self, state):
        pass
    #pickle
    #def __reduce__(self):
    #    return(self.__class__, (None, self.memberID, self.guildID, self._inventory))
    
    def reinstate(self, bot):
        self._guild = bot.get_guild(self._guildID)
        self._member = self._guild.get_member(self._memberID)
        self._username = self._member.display_name


    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        if self._member == None or self._guild == None:
            return

        interfaceOverwrites = {
            self._guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
            self._member: nextcord.PermissionOverwrite(read_messages=True)
        }
        overwrites = {
            self._guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self._member: nextcord.PermissionOverwrite(read_messages=True)
        }
        topic = "Private Discussion"

        interfaceName = self._member.name.replace(' ', '-').lower() + '_interface'
        channelName = self._member.name.replace(' ', '-').lower()

        self.interfaceChannel = await Channel(self._guild, interfaceName, 'Interface', can_talk=False).init()
        self._channel = await Channel(self._guild, channelName, 'Players').init()

        await asyncio.gather(self._channel.addPlayer(self._member), self.interfaceChannel.addPlayer(self._member))

        interfaceMessages = await self.interfaceChannel.channel.history(limit=None, oldest_first=True).flatten()
        #self.squadsMessage = None
        self.unitsMessage = None
        self.buildingsMessage = None

        for interfaceMessage in interfaceMessages:
            if interfaceMessage.author.id == theJar['client']:
                #if self.squadsMessage == None:
                    #self.squadsMessage = interfaceMessage
                if self.unitsMessage == None:
                    self.unitsMessage = interfaceMessage
                elif self.buildingsMessage == None:
                    self.buildingsMessage = interfaceMessage
                    break

        #if (self.squadsMessage == None):
            #self.squadsMessage = await Menus.squadsMenu.send(self.interfaceChannel.channel, state={'player': self._member.id})
        
        if (self.unitsMessage == None):
            self.unitsMessage = await Menus.cardsMenu.send(self.interfaceChannel.channel, state={'player': self._member.id, 'card_type': 'unit'})
        
        if (self.buildingsMessage == None):
            self.buildingsMessage = await Menus.cardsMenu.send(self.interfaceChannel.channel, state={'player': self.member.id, 'card_type': 'building'})

        self.interfaceDirty = False

    def updateInterface(self):
        self.interfaceDirty = True
    
    async def doInterfaceUpdate(self):
        self.interfaceDirty = False

        allUpdates = []

        #allUpdates.append(Menus.squadsMenu.update(self.squadsMessage, newState={'player': self._member.id}))
        if self.unitsMessage:
            allUpdates.append(Menus.cardsMenu.update(self.unitsMessage, newState={'player': self.member.id, 'card_type': 'unit'}))
        if self.buildingsMessage:
            allUpdates.append(Menus.cardsMenu.update(self.buildingsMessage, newState={'player': self.member.id, 'card_type': 'building'}))

        await asyncio.gather(*allUpdates)  

    def modStat(self, stat, quantity): #stat here is an INSTANCE (of relevent resouce!)
        new_val = self._stats[stat] + quantity
        can_add = False
        if self._statcaps[stat]:
            if new_val >= 0:
                if new_val <= self._statcaps[stat]:
                    can_add = True
        if can_add == True:
            self._stats[stat] = new_val
        return can_add

    def modStatCap(self, stat, quantity): #stat here is an INSTANCE (of relevent resouce!)
        new_val = self._stats[stat] + quantity
        new_cap = self._statcaps[stat] + quantity
        can_add = False
        if self._statcaps[stat]:
            if new_val >= 0:
                can_add = True
        if can_add == True:
            self._stats[stat] = new_val
            self._statcaps[stat] = new_cap
        return can_add


    def addRep(self, other_faction_title, rep_change):
        rep_change = int(rep_change)
        try:
            self.reps[other_faction_title] += rep_change
        except:
            self.reps[other_faction_title] = 0
            self.reps[other_faction_title] += rep_change
        if self.reps[other_faction_title] > 3:
            self.reps[other_faction_title] = 3
        if self.reps[other_faction_title] > -3:
            self.reps[other_faction_title] = -3

    def relationCheck(self, other_faction_title):
        rep = self.faction.repCheck(other_faction_title)
        return rep

    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self._channel.delete()
        await self.interfaceChannel.delete()
    
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
        al_rep['title'] = "-- Faction:"
        al_rep['value'] = '- None'
        if self.faction:
            al_rep['value'] = "- "+str(self.faction)
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
