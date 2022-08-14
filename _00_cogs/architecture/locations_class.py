import operator
from sys import path_hooks

from _02_global_dicts import theJar
import nextcord
import time, asyncio
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus
from .channels_class import Channel

class Region():
    def __init__(self, name, guild, districts = []):
        self.name = name
        theJar['regions'][name] = self
        self.districts = districts
        self.guild = guild
        self.channel = None
    
    #This is essentially the create channel.
    async def __init__(self):
        return #Remove to enable channel creation.
        playerRole = nextcord.utils.get(self.guild.roles, name="player")

        category = nextcord.utils.get(self.guild.categories, name=self.name)

        if not category:
            category = await self.guild.create_category(self.name)

        self.channel = await Channel(self.guild, self.name, self.name).init()

        #Remove?
        #await self.channel.addPlayer(playerRole)
    
    #saves channel and guild id for retrieval on reconstruction.
    def __getstate__(self):
        if self.channel:
            return (self.name, self.districts, self.guild.id, self.channel.channel.id)
        else:
            return (self.name, self.districts, self.guild.id, None)
        #return (self.name, self.districts, self.guild.id, self.channel)

    def __setstate__(self, state):
        self.name, self.districts, self.guild, self.channel = state
    
    def reconstruct(self, bot):
        self.guild = bot.get_guild(self.guild)
        if self.channel != None:
            self.channel.reconstruct(self.guild)
    

    #TODO: New one incoming, james will review and delete later
    #def __reduce__(self):
    #    districtKeys = []
    #    for district in self.districts:
    #    districtKeys.append(district.name)
    #    return(self.__class__, (self.name, None, self.guild.id))

    def addDistrict(self, district):
        self.districts.append(district)

    def __str__(self):
        return self.name

    def report(self):
        report = "-----"+str(self)+"-----\n\n"
        report += "--Districts:\n"
        for district in self.districts:
            report += "-"+str(district)+"\n"

        return report


    # @tasks.loop(seconds=1, count=1)
    # async def createChannel(self):
    #     playerRole = nextcord.utils.get(self.guild.roles, name="player")

    #     category = nextcord.utils.get(self.guild.categories, name=self.name)

    #     if not category:
    #         category = await self.guild.create_category(self.name)

    #     self.channel = await Channel(self.guild, self.name, self.name).init()

    #     #Remove?
    #     #await self.channel.addPlayer(playerRole)


class District():
    def __init__(self, name, region_name, size, paths = [], guild = None):
        print("District constructor running")
        self.name = name
        self.region = region_name
        self.paths = []
        self.players = []
        self.voice = None
        self.channel = None
        self.interfaceChannel = None
        self.guild = guild
        self.size = size
        self.civics = Civics(self)

        if guild:
            self.createChannel.start()

        sizes = {
            #inv_args: [r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None]
            'tiny': [self, 10, 10, 10, 10, 4, 1],
            'small': [self, 10, 10, 10, 10, 8, 2],
            'medium': [self, 10, 10, 10, 10, 16, 4],
            'large': [self, 10, 10, 10, 10, 24, 8],
            'huge': [self, 10, 10, 10, 10, 40, 14],
        }
        self.inventory = Inventory(*sizes[size])


        pathcaps = {
            'tiny': 2,
            'small': 3,
            'medium': 4,
            'large': 6,
            'huge': 9,
        }

        self.pathcap = pathcaps[size]

        if paths:
            for path in paths:
                district = theJar['districts'][path]
                self.setPath(district)

        theJar['regions'][region_name].addDistrict(self)
        theJar['districts'][name] = self

        self.interfaceDirty = False

    #This is the create channel location
    async def init(self):
        playerRole = nextcord.utils.get(self.guild.roles, name="player")
        #Wait a short period incase the region category was just made. Otherwise, it will not be able to find the category.
        await asyncio.sleep(.25)

        interfaceName = self.name.replace(' ', '-').lower() + '_interface'
        channelName = self.name.replace(' ', '-').lower()

        self.interfaceChannel = await Channel(self.guild, interfaceName, self.region, can_talk=False).init()
        self.channel = await Channel(self.guild, channelName, self.region).init()

        interfaceMessages = await self.interfaceChannel.channel.history(limit=None, oldest_first=True).flatten()
        self.interfaceMessage = None

        for interfaceMessage in interfaceMessages:
            if interfaceMessage.author.id == theJar['client']:
                self.interfaceMessage = interfaceMessage
                break

        if self.interfaceMessage == None:
            self.interfaceMessage = await Menus.districtMenu.send(self.interfaceChannel.channel, state={'district': self.name})
        else:
            self.interfaceMessage = await Menus.districtMenu.update(self.interfaceMessage, newState={'district': self.name})

        self.interfaceDirty = False

    def __getstate__(self):
        # vars left out:
        # self.voice = None
        # self.channel = None
        # self.interfaceChannel = None
        # self.guild = guild
        if self.voice:
            return (self.name,
            self.region,
            self.paths,
            self.players,
            self.size,
            self.civics,
            self.inventory,
            self.pathcap,
            self.interfaceDirty,
            self.channel, self.interfaceChannel, self.guild.id, self.voice.id)
        return(self.name,
        self.region,
        self.paths,
        self.players,
        self.size,
        self.civics,
        self.inventory,
        self.pathcap,
        self.interfaceDirty,
        self.channel, self.interfaceChannel, self.guild.id, self.voice)

    def __setstate__(self, state):
        self.name, self.region, self.paths, self.players, self.size, self.civics, self.inventory, self.pathcap, self.interfaceDirty, self.channel, self.interfaceChannel, self.guild, self.voice = state
    
    def reconstruct(self, bot):
        self.guild = bot.get_guild(self.guild)
        self.channel.reconstruct(self.guild)
        self.interfaceChannel.reconstruct(self.guild)

    # @tasks.loop(seconds=1, count=1)
    # async def createChannel(self):
    #     playerRole = nextcord.utils.get(self.guild.roles, name="player")
    #     #Wait a short period incase the region category was just made. Otherwise, it will not be able to find the category.
    #     await asyncio.sleep(.25)

    #     interfaceName = self.name.replace(' ', '-').lower() + '_interface'
    #     channelName = self.name.replace(' ', '-').lower()

    #     self.interfaceChannel = await Channel(self.guild, interfaceName, self.region, can_talk=False).init()
    #     self.channel = await Channel(self.guild, channelName, self.region).init()

    #     interfaceMessages = await self.interfaceChannel.channel.history(limit=None, oldest_first=True).flatten()
    #     self.interfaceMessage = None

    #     for interfaceMessage in interfaceMessages:
    #         if interfaceMessage.author.id == theJar['client']:
    #             self.interfaceMessage = interfaceMessage
    #             break

    #     if self.interfaceMessage == None:
    #         self.interfaceMessage = await Menus.districtMenu.send(self.interfaceChannel.channel, state={'district': self.name})
    #     else:
    #         self.interfaceMessage = await Menus.districtMenu.update(self.interfaceMessage, newState={'district': self.name})

    #     self.interfaceDirty = False

    # Ginger: Updates the interface message
    def updateInterface(self):
        self.interfaceDirty = True

    async def doInterfaceUpdate(self):
        self.interfaceDirty = False

        if hasattr(self, 'interfaceMessage'):
            self.interfaceMessage = await Menus.districtMenu.update(self.interfaceMessage, newState={'district': self.name})

    def setPath(self, target):
        can_path = True
        if len(target.paths) >= target.pathcap:
            can_path = False
        if len(self.paths) >= self.pathcap:
            can_path = False
        if can_path:
            if target not in self.paths:
                self.paths.append(target.name)
            if self not in target.paths:
                target.paths.append(self.name)

    def moveCheck(self, player):
        can_move = False
        if self.name in theJar['districts'][player.location].paths:
            can_move = player.modStat('Influence', -1)
        return can_move


    def canChat(self, player):
        #call within but just prior to player move and unit move iff player is not present
        can_chat = False
        can_interface = False
        local_card_list = []
        for unit in player.inventory.slots['unit']:
            print(unit, unit.location)
            if unit.location.name == self.name:
                can_interface = True
                local_card_list.append(unit)
        for building in player.inventory.slots['building']:
            if building.location.name == self.name:
                can_interface = True
                local_card_list.append(building)
        for card in local_card_list:
            print('Local Card List: '+str(local_card_list))
            if 'Recon' in card.certs:
                can_chat = True
        return can_chat, can_interface


    async def movePlayer(self, player):
        #If player is already in a location, check if they can move. Otherwise, set it to true.
        if player.location:
            player_loc = theJar['districts'][player.location]
            can_move = self.moveCheck(player)
            #If player is in location AND can move, remove them from the current location's player list.
            if can_move:
                player_loc.players.remove(player)
                player_loc.updateInterface()
                player_loc.civics.delPlayer(player)
        else:
            can_move = True

        if can_move:
            await self._movePlayer(player)
            return str(player) + " has moved to " + str(self)
        return "Error: " + str(player) + " is unable to move to " + str(self)
    
    async def _movePlayer(self, player):
        #Check if player is already in a location. Player may not be in a region at the start of initialization.
        if player.location:
            player_loc = theJar['districts'][player.location]
            #if player is being moved to a different region, remove permissions from old region channel and category.
            if not player_loc.region == self.region:
                #Not sure how to adapt this to new channel system -cart
                category = nextcord.utils.get(self.guild.categories, name=player_loc.region)
                await category.set_permissions(player.member, read_messages=False)
        
            #remove player from old district channel (after checking to make sure this needs to happen)
            can_chat, can_interface = player_loc.canChat(player)
            if not can_chat:
                #remove from chat channel
                await player_loc.channel.removePlayer(player.member)
            if not can_interface:
                #remove from interface
                await player_loc.interfaceChannel.removePlayer(player.member)
        #This was just changed to make the player location a string instead of object- may break things -cart
        player.location = str(self)
        self.players.append(player)
        self.updateInterface()
        self.civics.addPlayer(player)
        await self.channel.addPlayer(player.member)
        await self.interfaceChannel.addPlayer(player.member)

    def __str__(self):
        return self.name

    def report(self):
        title = "-----"+str(self)+"-----\n"
        report = "*"+str(self.region)+"*\n\n"
        fields = []

        player_rep = {'inline':True}
        player_rep['title'] = "-- Players Present:"
        player_rep['value'] = ''
        for player in self.players:
            player_rep['value'] += "- "+str(player)+"\n"
        player_rep['value'] = player_rep['value'][:-1]
        if len(player_rep['value']) == 0:
            player_rep['value'] = '- ...'
        fields.append(player_rep)

        path_rep = {'inline':True}
        path_rep['title'] = "-- Paths:"
        path_rep['value'] = ''
        for district in self.paths:
            path_rep['value'] += "- "+str(district)+"\n"
        path_rep['value'] = path_rep['value'][:-1]
        fields.append(path_rep)

        inv_report, inv_title, inv_fields = self.inventory.report()

        fields += inv_fields
        return report, title, fields



class Civics():
    def __init__(self, location):
        self.location = location
        self.players = [x for x in location.players]
        self.squad_list = []
        self.squads_ranked = {}
        self.factions = []
        self.commanders = []
        self.occupance = None
        self.governors = []
        self.governance = None
        #Stand, Attack, Defend, Retreat [Target Location]
        self.faction_stances = {}
        for faction in theJar['factions'].keys():
            self.faction_stances[faction] = {'stance': None}

    def addSquad(self, squad):
        if squad not in self.squad_list:
            self.squad_list.append(squad)
            squad.setPriority(squad.priority)
            #^Runs squad.getRank which runs self.getCommander

    def delSquad(self, squad):
        if squad in self.squad_list:
            self.squad_list.remove(squad)
            self.squads_ranked[squad.faction][squad.priority].remove(squad)
            self.getCommander(squad.faction)

    def addPlayer(self, player):
        if player not in self.players:
            self.players.append(player)
            self.addFaction(player.faction)
            self.getCommander(player.faction)

    def delPlayer(self, player):
        if player in self.players:
            if player.location != self.location:
                remove = True
                #TODO: Make combatants
                for squad in self.squad_list:
                    if squad.owner==player:
                        remove = False
                self.players.remove(player)
                self.getCommander(player.faction)

    def addFaction(self, faction):
        if faction:
            if faction not in self.factions:
                self.factions.append(faction)
                self.faction_stances[faction] = {'stance':'Stand'}

    def delFaction(self, faction):
        if faction in self.factions:
            self.factions.remove(faction)
            self.faction_stances[faction] = {'stance':None}

    def getGovernor(self, faction):
        candidates = []
        for player in self.players:
            if player.faction == faction:
                candidates.append(player)
        for building in self.location.inventory.slots['building']:
            if building.owner.faction == faction:
                if building.owner not in candidates:
                    candidates.append(building.owner)
        metrics = []
        alg_building_count = 0
        for cand in candidates:
            inf = cand._statcaps['Influence']
            buildings = [x for x in cand.inventory.cards['building'] if x.location == self.location]
            metric = {'gov':cand, 'inf': inf, 'buildings': len(buildings)}
            metrics.append(metric)
            alg_building_count += len(buildings)
        metrics.sort(key=operator.itemgetter('inf','buildings'), reverse=True)
        if len(metrics) > 0:
            gov = metrics[0]
            try:
                old_gov = next(x for x in self.governors if x['faction']==faction)
                self.governors.remove(old_gov)
            except:
                pass
            self.governors.append({"gov":gov['gov'], 'faction':faction, 'inf':gov['inf'], 'buildings':alg_building_count})
        else:
            self.delFaction(faction)
        self.setGovernorRankings()

    def setGovernorRankings(self):
        self.governors.sort(key=operator.itemgetter('buildings','inf'))
        self.governance = theJar['factions'][self.governors[0]['faction']]

    def getCommander(self, faction):
        candidates = []
        for player in self.players:
            if player.faction == faction:
                candidates.append(player)
        metrics = []
        #squad_count = 0
        combatant_count = 0
        for cand in candidates:
            inf = cand._statcaps['Influence']
            #squads = [x for x in cand.squads if x.location == self.location]
            #metric = {'cmd':cand, 'inf': inf, 'squads': len(squads)}
            #squad_count += len(squads)

            combatants = [x for x in cand.inventory.slots['unit'] if x.location == self.location and 'Combat' in x.certs]
            metric = {'cmd':cand, 'inf': inf, 'squads': len(combatants)}
            combatant_count += len(combatants)
            metrics.append(metric)
        metrics.sort(key=operator.itemgetter('inf','squads'), reverse=True)
        if len(metrics) > 0:
            cmdr = metrics[0]
            try:
                old_cmdr = next(x for x in self.commanders if x['faction']==faction)
                self.commanders.remove(old_cmdr)
            except:
                pass
            self.commanders.append({"cmdr":cmdr['cmd'], 'faction':faction, 'inf':cmdr['inf'], 'combatants':combatant_count})
        else:
            self.delFaction(faction)
        self.setCommanderRankings()

    def setCommanderRankings(self):
        self.commanders.sort(key=operator.itemgetter('combatants','inf'))

        try:
            cmdr_faction = theJar['factions'][self.commanders[0]['faction']]
        except:
            cmdr_faction = None
        if cmdr_faction:
            if self.occupance:
                if cmdr_faction != self.occupance:
                    #if neutral to current occ, overtake
                    if cmdr_faction.repCheck(self.occupance.title) < 1:
                        self.occupance = cmdr_faction
            else:
                if self.governance:
                    if cmdr_faction != self.governance:
                        #if netural to current gov, overtake
                        if cmdr_faction.repCheck(self.governance.title) < 1:
                            self.occupance = cmdr_faction
                else:
                    #no gov or occ, overtake
                    self.occupance = cmdr_faction

    def setStance(self, player, stance, target=None):
        if not target:
            stance_dict = {'stance': stance}
        else:
            stance_dict = {'stance': stance, 'target': target}
        commanders = [x['cmdr'] for x in self.commanders]
        if player in commanders:
            faction = player.faction
            self.faction_stances[faction] = stance_dict
            #if stance == "Attack":
               # self.joinConflict(player.faction, target)
        else:
            print('Error: Player is not a commander!')

    def setRetreat(self, faction, alt_location):
        if alt_location != self.location:
            self.retreats[faction] = alt_location

    def refresh(self):
        self.faction_stances = {}
        for faction in theJar['factions'].keys():
            self.faction_stances[faction] = {'stance':None}
        self.conflicts = []
        self.retreats = {}

    def strReport(self):
        counts = {}
        print(self.factions)
        for faction in self.factions:
            print(faction)
            fc = 0
            f_units = [x for x in self.location.inventory.slots['unit'] if x.owner.faction == faction]
            f_buildings = [x for x in self.location.inventory.slots['building'] if x.owner.faction == faction]
            f_cards = f_units+f_buildings
            for card in f_cards:
                print(card)
                if 'Combat' in card.certs:
                    fc += 1
            counts[faction] = fc
        title = '----------'+str(self.location)+' Strength----------'
        report = ''
        for count in counts.keys():
            report += '- '+count+': '+str(counts[count])+'\n'
        return report, title


    def report(self):
        fields = []
        title = "-----"+str(self.location)+" Civics-----"
        report = ''
        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] =  "\n- Location: "+str(self.location)+\
                             "\n- Players: "+str([str(x) for x in self.players])+\
                             "\n- Squads: "+str(self.squads_ranked)+\
                             "\n- Factions: "+str(self.factions)+\
                             "\n- Commanders: "+str([str(x['cmdr']) for x in self.commanders])+\
                             "\n- Occupance: "+str(self.occupance)+\
                             "\n- Governors: "+str([str(x['gov']) for x in self.governors])+\
                             "\n- Governance: "+str(self.governance)+\
                             "\n- Faction Stances: "+str(self.faction_stances)
        #info_rep['value'] += "\n- Units: "
        #for unit in self.units:
        #    value = unit.title
        #    info_rep['value'] += str(value)+"\n"
        #info_rep['value'] = info_rep['value'][:-2]
        fields.append(info_rep)
        return report, title, fields
