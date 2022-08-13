import asyncio
import nextcord
from nextcord import guild
from nextcord.ext import tasks
from _02_global_dicts import theJar
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus
from .channels_class import Channel

class Player():
    def __init__(self, member, memberID = None, guildID = None, inventory = None, starter_location = None, faction = None):
        #flag to see if the player has been cast as a character once before
        self.cast = False

        self.member = member
        self.username = member.name
        self.memberID = member.id
        self.guildID = member.guild.id
        self.guild = member.guild

        self.channel = None
        self.interfaceChannel = None
        self.createPrivateChannel.start()

        if inventory == None:
            self.inventory = Inventory(self, r_cap=100, u_cap=20, b_cap=10) #Inventory Instance
        else:
            self.inventory = inventory
        self.location = starter_location #Location Instance (needs to lack _!)
        self._stats = {
            #instance:quantity
            'Influence':20
        }
        self._statcaps = {
            #instance:cap
            'Influence':20
        }
        self.faction = faction
        self.reps = {}
        self.squads = []

        self.interfaceDirty = False

    def __getstate__(self):
        return (self.cast, self.username, self.memberID, self.guildID, self.channel, self.interfaceChannel, self.inventory, self.location, self._stats, self._statcaps, self.faction, self.reps, self.squads, self.interfaceDirty)
    def __setstate__(self, state):
        self.cast, self.username, self.memberID, self.guildID, self.channel, self.interfaceChannel, self.inventory, self.location, self._stats, self._statcaps, self.faction, self.reps, self.squads, self.interfaceDirty = state
    
    def reconstruct(self, bot):
        self.guild = bot.get_guild(self.guildID)
        self.member = self.guild.get_member(self.memberID)
        self.interfaceChannel.reconstruct(self.guild)
        self.channel.reconstruct(self.guild)

    @tasks.loop(seconds=1, count=1)
    async def createPrivateChannel(self):
        if self.member == None or self.guild == None:
            return

        interfaceOverwrites = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
            self.member: nextcord.PermissionOverwrite(read_messages=True)
        }
        overwrites = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            self.member: nextcord.PermissionOverwrite(read_messages=True)
        }
        topic = "Private Discussion"

        interfaceName = self.member.name.replace(' ', '-').lower() + '_interface'
        channelName = self.member.name.replace(' ', '-').lower()

        self.interfaceChannel = await Channel(self.guild, interfaceName, 'Interface', can_talk=False).init()
        self.channel = await Channel(self.guild, channelName, 'Players').init()

        await asyncio.gather(self.channel.addPlayer(self.member), self.interfaceChannel.addPlayer(self.member))

        interfaceMessages = await self.interfaceChannel.channel.history(limit=None, oldest_first=True).flatten()

        self.infoMessage = None
        #self.squadsMessage = None
        self.unitsMessage = None
        self.buildingsMessage = None

        for interfaceMessage in interfaceMessages:
            if interfaceMessage.author.id == theJar['client']:
                if self.infoMessage == None:
                    self.infoMessage = interfaceMessage
                #elif self.squadsMessage == None:
                    #self.squadsMessage = interfaceMessage
                elif self.unitsMessage == None:
                    self.unitsMessage = interfaceMessage
                elif self.buildingsMessage == None:
                    self.buildingsMessage = interfaceMessage
                    break

        if (self.infoMessage == None):
            self.infoMessage = await Menus.playerInfoMenu.send(self.interfaceChannel.channel, state={'player': self.member.id})
        else:
            self.infoMessage = await Menus.playerInfoMenu.update(self.infoMessage, newState={'player': self.member.id})

        #if (self.squadsMessage == None):
            #self.squadsMessage = await Menus.squadsMenu.send(self.interfaceChannel.channel, state={'player': self._member.id})
        
        if (self.unitsMessage == None):
            self.unitsMessage = await Menus.cardsMenu.send(self.interfaceChannel.channel, state={'player': self.member.id, 'card_type': 'unit'})
        else:
            self.unitsMessage = await Menus.cardsMenu.update(self.unitsMessage, newState={'player': self.member.id, 'card_type': 'unit'})
        
        if (self.buildingsMessage == None):
            self.buildingsMessage = await Menus.cardsMenu.send(self.interfaceChannel.channel, state={'player': self.member.id, 'card_type': 'building'})
        else:
            self.buildingsMessage = await Menus.cardsMenu.update(self.buildingsMessage, newState={'player': self.member.id, 'card_type': 'building'})

        self.interfaceDirty = False

    def updateInterface(self):
        self.interfaceDirty = True
    
    async def doInterfaceUpdate(self):
        self.interfaceDirty = False

        allUpdates = []

        if hasattr(self, 'infoMessage') and self.infoMessage:
            self.infoMessage = await Menus.playerInfoMenu.update(self.infoMessage, newState={'player': self.member.id})

        #allUpdates.append(Menus.squadsMenu.update(self.squadsMessage, newState={'player': self._member.id}))
        if hasattr(self, 'unitsMessage') and self.unitsMessage:
            self.unitsMessage = await Menus.cardsMenu.update(self.unitsMessage, newState={'player': self.member.id, 'card_type': 'unit'})
        if hasattr(self, 'buildingsMessage') and self.buildingsMessage:
            self.buildingsMessage = await Menus.cardsMenu.update(self.buildingsMessage, newState={'player': self.member.id, 'card_type': 'building'})

    def modStat(self, stat, quantity):
        new_val = self._stats[stat] + quantity
        can_add = False
        if self._statcaps[stat]:
            if new_val >= 0:
                if new_val <= self._statcaps[stat]:
                    can_add = True
        if can_add == True:
            self._stats[stat] = new_val
        return can_add

    def modStatCap(self, stat, quantity):
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
        if other_faction_title == self.faction:
            rep = 3
        else:
            rep = theJar['factions'][self.faction].repCheck(other_faction_title)
        return rep

    @tasks.loop(seconds=1, count=1)
    async def __delPrivateChannel(self):
        await self.channel.delete()
        await self.interfaceChannel.delete()
    
    def delPrivateChannel(self):
        self.__delPrivateChannel.start()

    def __str__(self):
        return self.username

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

        inv_report, inv_title, inv_fields = self.inventory.report()
        fields += inv_fields
        return report, title, fields

    #ACCESSOR

    # @property
    # def member(self):
    #     return self._member

    # @property
    # def guild(self):
    #     return self._guild

    # @property
    # def channel(self):
    #     return self._channel
    # @property
    # def memberID(self):
    #     return self._memberID
    # @property
    # def guildID(self):
    #     return self._guildID
    # @property
    # def inventory(self):
    #     return self._inventory

    # #left for legacy support
    # def getChannelID(self):
    #     return self._channel.id
